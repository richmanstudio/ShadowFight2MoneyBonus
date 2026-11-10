#!/usr/bin/env python3
"""Offline SF2 archive verifier and currency editor. Python 3.10+, stdlib only."""
import argparse
import copy
import hashlib
import json
import plistlib
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
import xml.etree.ElementTree as ET

BUNDLE = 'com.nekki.shadowfight'
SUFFIX = 'wqO+Qchj|r*QXg7o_KNmLYvpGHdSwqxwlQI2vy618KaD^Pwt-h3H8*uJ'
USERDATA = 'Container/Documents/userdata/'
MAX_TOTAL = 2 * 1024**3
MAX_XML = 32 * 1024**2

class SaveError(ValueError):
    pass

def md5_upper(data):
    return hashlib.md5(data).hexdigest().upper()

def normalize_xml(data):
    """Keep original lexical XML; never reserialize with ElementTree."""
    parse_xml(data)
    return ''.join(line.strip() for line in data.decode('utf-8-sig').splitlines())

def save_hash(data, device_value):
    salt = device_value + BUNDLE + SUFFIX
    first = md5_upper(normalize_xml(data).encode('utf-8'))
    return md5_upper((first + salt).encode('utf-8')).encode('ascii')

def parse_xml(data):
    if len(data) > MAX_XML:
        raise SaveError('XML exceeds the 32 MiB tool limit.')
    if b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper():
        raise SaveError('DTD/entity declarations are unsupported.')
    try:
        return ET.fromstring(data.decode('utf-8-sig'))
    except (ET.ParseError, UnicodeError) as e:
        raise SaveError('Invalid UTF-8 XML.') from e

def active_warrior(root):
    current = root.find('CurrentUser')
    if current is None or current.get('ID') is None:
        raise SaveError('CurrentUser.ID is missing.')
    warriors = [w for w in root.findall('./Warriors/Warrior')
                if w.get('ID') == current.get('ID')]
    if len(warriors) != 1:
        raise SaveError('Active Warrior is missing or ambiguous.')
    return warriors[0]

def archive_layout(z):
    seen = set()
    total = 0
    for info in z.infolist():
        path = PurePosixPath(info.filename)
        if path.is_absolute() or '..' in path.parts or '\\' in info.filename:
            raise SaveError('Unsafe archive path.')
        if info.flag_bits & 1:
            raise SaveError('ZIP-level encrypted entries are unsupported.')
        if not info.is_dir():
            if info.filename in seen:
                raise SaveError('Duplicate file entry in archive.')
            seen.add(info.filename)
        total += info.file_size
    if total > MAX_TOTAL:
        raise SaveError('Archive exceeds the 2 GiB uncompressed tool limit.')
    names = [name for name in seen if name.endswith(USERDATA + 'users.xml')]
    if len(names) != 1:
        raise SaveError('Expected exactly one Container/Documents/userdata/users.xml.')
    prefix = names[0][:-len(USERDATA + 'users.xml')]
    return prefix, prefix + USERDATA

def strings(value):
    if isinstance(value, dict):
        for item in value.values():
            yield from strings(item)
    elif isinstance(value, (list, tuple)):
        for item in value:
            yield from strings(item)
    elif isinstance(value, bytes):
        yield value.decode('utf-8', errors='ignore')
    elif isinstance(value, str):
        yield value

def candidates(z, prefix):
    """Find candidates locally; their presence alone is not verification."""
    values = set()
    pattern = re.compile(r'(?i)\b[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}\b|\b[0-9a-f]{16,64}\b')
    for info in z.infolist():
        if not info.filename.startswith(prefix + 'Container/Library/Preferences/'):
            continue
        if not info.filename.endswith('.plist') or info.file_size > 8 * 1024**2:
            continue
        try:
            value = plistlib.loads(z.read(info))
        except (plistlib.InvalidFileException, ValueError, TypeError, OverflowError):
            continue
        for text in strings(value):
            for found in pattern.findall(text):
                values.update([found, found.upper(), found.lower()])
    return sorted(values)

def verified_device(z, prefix, base, explicit=None):
    raw = z.read(base + 'users.xml')
    parse_xml(raw)
    try:
        stored = z.read(base + 'users.xml.hash')
    except KeyError as e:
        raise SaveError('Original users.xml.hash is missing. Export a fresh intact save.') from e
    if not re.fullmatch(rb'[0-9A-F]{32}', stored):
        raise SaveError('Expected an uppercase 32-byte ASCII .hash without a newline.')
    first = md5_upper(normalize_xml(raw).encode('utf-8'))
    pool = [explicit] if explicit is not None else candidates(z, prefix)
    matches = [device for device in pool if md5_upper(
        (first + device + BUNDLE + SUFFIX).encode('utf-8')).encode('ascii') == stored]
    if len(matches) != 1:
        raise SaveError('Original hash could not be reproduced uniquely. No output was created. '
                        'Use a fresh intact export; do not guess the identifier or overwrite the hash.')
    return matches[0]

def currency_value(value):
    if not re.fullmatch(r'[0-9]{1,30}', value):
        raise SaveError('Currency must contain 1 to 30 ASCII digits, without signs or separators.')
    return str(int(value))

def patch_xml(data, money=None, bonus=None):
    before = parse_xml(data)
    warrior = active_warrior(before)
    changes = {k: currency_value(v) for k, v in [('Money', money), ('Bonus', bonus)] if v is not None}
    if not changes:
        raise SaveError('Specify --money and/or --bonus.')
    text = data.decode('utf-8-sig')
    count = 0
    def replace(match):
        nonlocal count
        tag = match.group()
        entry = ET.fromstring(tag[:-1] + '/>')
        if entry.get('ID') != warrior.get('ID'):
            return tag
        count += 1
        for key, value in changes.items():
            tag, n = re.subn(r'\b' + key + r'="[^"]*"', key + '="' + value + '"', tag)
            if n != 1:
                raise SaveError('Unsupported or ambiguous attribute formatting: ' + key)
        return tag
    result = re.sub(r'<Warrior\b[^>]*>', replace, text)
    if count != 1:
        raise SaveError('Expected exactly one active Warrior opening tag.')
    modified = (b'\xef\xbb\xbf' if data.startswith(b'\xef\xbb\xbf') else b'') + result.encode('utf-8')
    expected = copy.deepcopy(before)
    active_warrior(expected).attrib.update(changes)
    if ET.tostring(expected) != ET.tostring(parse_xml(modified)):
        raise SaveError('Unexpected XML change; output refused.')
    return modified

def inspect_archive(path, verify=False, device=None):
    with zipfile.ZipFile(path) as z:
        prefix, base = archive_layout(z)
        raw = z.read(base + 'users.xml')
        warrior = active_warrior(parse_xml(raw))
        result = {k: warrior.get(k) for k in ['Money', 'Bonus', 'Level', 'Experience', 'CurrentZone', 'DenominationDigits']}
        result['xml_sha256'] = hashlib.sha256(raw).hexdigest()
        if verify:
            if z.testzip() is not None:
                raise SaveError('Archive CRC check failed.')
            found = verified_device(z, prefix, base, device)
            result['original_hash_verified'] = True
            result['calculated_hash'] = save_hash(raw, found).decode()
            backup = base + 'users_backup.xml'
            if backup in z.namelist():
                expected = save_hash(z.read(backup), found)
                result['backup_hash_verified'] = (backup + '.hash' in z.namelist()
                                                   and z.read(backup + '.hash') == expected)
        return result

def patch_archive(source, output, money=None, bonus=None, device=None):
    source, output = Path(source), Path(output)
    if source.resolve() == output.resolve() or output.exists():
        raise SaveError('Choose a NEW output filename; source/existing files are never overwritten.')
    if output.suffix.lower() != '.imazingapp':
        raise SaveError('Output filename must end in .imazingapp.')
    with zipfile.ZipFile(source) as z:
        prefix, base = archive_layout(z)
        if z.testzip() is not None:
            raise SaveError('Source archive CRC check failed.')
        found = verified_device(z, prefix, base, device)
        raw = z.read(base + 'users.xml')
        modified = patch_xml(raw, money, bonus)
        digest = save_hash(modified, found)
        changes = {base + name: modified for name in ['users.xml', 'users_backup.xml']}
        changes.update({base + name: digest for name in ['users.xml.hash', 'users_backup.xml.hash']})
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix='sf2-', dir=output.parent) as tmp:
            staged = Path(tmp) / 'verified.imazingapp'
            with zipfile.ZipFile(staged, 'w') as target:
                target.comment = z.comment
                for info in z.infolist():
                    target.writestr(copy.copy(info), changes.get(info.filename, z.read(info)))
                for name in changes.keys() - set(z.namelist()):
                    target.writestr(name, changes[name], compress_type=zipfile.ZIP_DEFLATED)
            with zipfile.ZipFile(staged) as check:
                if check.testzip() is not None:
                    raise SaveError('Output archive CRC check failed.')
                if set(check.namelist()) != set(z.namelist()) | set(changes):
                    raise SaveError('Unexpected archive entries.')
                for info in z.infolist():
                    if check.read(info.filename) != changes.get(info.filename, z.read(info)):
                        raise SaveError('Unexpected change to archive content.')
                for name, data in changes.items():
                    if check.read(name) != data:
                        raise SaveError('Output verification failed.')
                for name in ['users.xml', 'users_backup.xml']:
                    if save_hash(check.read(base + name), found) != check.read(base + name + '.hash'):
                        raise SaveError('XML/hash mismatch in output.')
            with output.open('xb') as final, staged.open('rb') as prepared:
                shutil.copyfileobj(prepared, final)
        return {'output': str(output), 'source_unchanged': True,
                'original_hash_verified': True, 'output_hash_verified': True,
                'updated_entries': sorted(changes),
                'sha256': hashlib.sha256(output.read_bytes()).hexdigest()}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for name in ['inspect', 'verify', 'patch']:
        p = sub.add_parser(name)
        p.add_argument('archive', type=Path)
        if name != 'inspect':
            p.add_argument('--device-value', help='Optional explicit value; still checked against original hash.')
        if name == 'patch':
            p.add_argument('--output', type=Path, required=True)
            p.add_argument('--money')
            p.add_argument('--bonus')
    args = parser.parse_args(argv)
    try:
        if args.command == 'patch':
            result = patch_archive(args.archive, args.output, args.money, args.bonus, args.device_value)
        else:
            result = inspect_archive(args.archive, args.command == 'verify', getattr(args, 'device_value', None))
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    except (SaveError, OSError, zipfile.BadZipFile, KeyError, RuntimeError) as e:
        print('Error: ' + str(e), file=sys.stderr)
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
