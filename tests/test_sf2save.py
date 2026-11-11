import hashlib
import plistlib
import tempfile
import unittest
import zipfile
from pathlib import Path
import sf2save as s

DEVICE = '00000000-0000-4000-8000-000000000001'
BASE = s.USERDATA
XML = (b'\xef\xbb\xbf<?xml version="1.0" encoding="utf-8"?>\r\n'
       b'<Root>\r\n  <CurrentUser ID="1" />\r\n  <Warriors>\r\n'
       b'    <Warrior ID="1" Money="123" Bonus="2" Level="36" Experience="100">\r\n'
       b'      <Items><Item Name="Fists" Count="1" /></Items>\r\n'
       b'    </Warrior>\r\n  </Warriors>\r\n</Root>')

def fixture(path, xml=XML, bad_hash=False, prefix='', duplicate=False, missing_backup=False):
    data = {
        prefix + BASE + 'users.xml': xml,
        prefix + BASE + 'users.xml.hash': b'0' * 32 if bad_hash else s.save_hash(xml, DEVICE),
        prefix + 'Container/Library/Preferences/com.nekki.shadowfight.plist':
            plistlib.dumps({'user_id': 'sf2;Android;' + DEVICE}),
        prefix + '.lock': b'opaque metadata must remain byte-identical',
        prefix + BASE + 'localSettings.bin': b'\x00\xffbinary unchanged',
    }
    if not missing_backup:
        data[prefix + BASE + 'users_backup.xml'] = xml
        data[prefix + BASE + 'users_backup.xml.hash'] = s.save_hash(xml, DEVICE)
    with zipfile.ZipFile(path, 'w') as z:
        z.comment = b'archive comment'
        for name, value in data.items():
            z.writestr(name, value)
        if duplicate:
            z.writestr(prefix + BASE + 'users.xml', xml)
    return path

class SaveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.src = fixture(self.root / 'original.imazingapp')
        self.out = self.root / 'patched.imazingapp'

    def tearDown(self):
        self.tmp.cleanup()

    def test_md5_known_vector(self):
        self.assertEqual(s.md5_upper(b'abc'), '900150983CD24FB0D6963F7D28E17F72')

    def test_fixed_synthetic_hash_vector(self):
        self.assertEqual(s.save_hash(XML, DEVICE), b'514A5F2D6F16D37FBE063D8EEFEDBD74')

    def test_discovers_value_and_verifies_original(self):
        result = s.inspect_archive(self.src, True)
        self.assertTrue(result['original_hash_verified'])
        self.assertTrue(result['backup_hash_verified'])
        self.assertNotIn(DEVICE, str(result))

    def test_patch_preserves_source_progress_binary_and_metadata(self):
        original = self.src.read_bytes()
        s.patch_archive(self.src, self.out, money='10000000', bonus='1000')
        self.assertEqual(original, self.src.read_bytes())
        with zipfile.ZipFile(self.src) as old, zipfile.ZipFile(self.out) as new:
            self.assertEqual(old.comment, new.comment)
            self.assertEqual(new.read('.lock'), old.read('.lock'))
            self.assertEqual(new.read(BASE + 'localSettings.bin'), old.read(BASE + 'localSettings.bin'))
            expected = XML.replace(b'Money="123"', b'Money="10000000"').replace(b'Bonus="2"', b'Bonus="1000"')
            self.assertEqual(new.read(BASE + 'users.xml'), expected)
            self.assertEqual(new.read(BASE + 'users_backup.xml'), expected)
        self.assertTrue(s.inspect_archive(self.out, True)['backup_hash_verified'])

    def test_patch_one_currency_only(self):
        s.patch_archive(self.src, self.out, bonus='20')
        self.assertEqual(s.inspect_archive(self.out)['Money'], '123')

    def test_bad_original_hash_refuses_output(self):
        fixture(self.src, bad_hash=True)
        with self.assertRaises(s.SaveError):
            s.patch_archive(self.src, self.out, bonus='20')
        self.assertFalse(self.out.exists())

    def test_wrong_explicit_device_refuses_output(self):
        with self.assertRaises(s.SaveError):
            s.patch_archive(self.src, self.out, bonus='20', device='wrong')
        self.assertFalse(self.out.exists())

    def test_existing_output_not_overwritten(self):
        self.out.write_bytes(b'keep me')
        with self.assertRaises(s.SaveError):
            s.patch_archive(self.src, self.out, bonus='20')
        self.assertEqual(self.out.read_bytes(), b'keep me')

    def test_source_path_not_overwritten(self):
        before = self.src.read_bytes()
        with self.assertRaises(s.SaveError):
            s.patch_archive(self.src, self.src, bonus='20')
        self.assertEqual(before, self.src.read_bytes())

    def test_nested_archive_root(self):
        fixture(self.src, prefix='Shadow Fight 2/')
        s.patch_archive(self.src, self.out, bonus='20')
        self.assertTrue(s.inspect_archive(self.out, True)['backup_hash_verified'])

    def test_missing_backup_pair_is_created(self):
        fixture(self.src, missing_backup=True)
        s.patch_archive(self.src, self.out, bonus='20')
        self.assertTrue(s.inspect_archive(self.out, True)['backup_hash_verified'])

    def test_duplicate_file_refused(self):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            fixture(self.src, duplicate=True)
        with self.assertRaises(s.SaveError):
            s.patch_archive(self.src, self.out, bonus='20')

    def test_unsafe_archive_path_refused(self):
        with zipfile.ZipFile(self.src, 'a') as z:
            z.writestr('../outside', b'no')
        with self.assertRaises(s.SaveError):
            s.patch_archive(self.src, self.out, bonus='20')

    def test_invalid_numeric_input_refused(self):
        for value in ['-1', '1.5', '1 000', '١٢٣', '9' * 31]:
            with self.subTest(value=value), self.assertRaises(s.SaveError):
                s.patch_archive(self.src, self.out, bonus=value)
        self.assertFalse(self.out.exists())

    def test_dtd_and_malformed_xml_refused(self):
        for data in [b'<Root>', b'<!DOCTYPE Root><Root />']:
            with self.assertRaises(s.SaveError):
                s.normalize_xml(data)


class NewFeatureTests(unittest.TestCase):
    """Synthetic XML/hash fixtures — no real player save is committed."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        # ForgeMaterial3 is intentionally absent in this fixture (like some live saves).
        self.xml = XML.replace(
            b'    </Warrior>',
            b'      <Currencies ForgeMaterial1="20" ForgeMaterial2="10" />\\r\\n'
            b'    </Warrior>'
        )
        self.src = fixture(self.root / 'original.imazingapp', xml=self.xml)
        self.out = self.root / 'modified.imazingapp'

    def tearDown(self):
        self.tmp.cleanup()

    def test_orbs_and_energy_in_one_archive(self):
        original_bytes = self.src.read_bytes()
        s.patch_archive(
            self.src, self.out, unlimited_energy=True,
            forge_materials={
                'ForgeMaterial1': '999', 'ForgeMaterial2': '888',
                'ForgeMaterial3': '777',
            }
        )
        self.assertEqual(original_bytes, self.src.read_bytes())
        inspected = s.inspect_archive(self.out, verify=True)
        self.assertTrue(inspected['original_hash_verified'])
        self.assertTrue(inspected['backup_hash_verified'])
        self.assertEqual(inspected['ForgeMaterial1'], '999')
        self.assertEqual(inspected['ForgeMaterial2'], '888')
        self.assertEqual(inspected['ForgeMaterial3'], '777')
        self.assertTrue(inspected['Unlimited_Energy'])
        with zipfile.ZipFile(self.src) as before, zipfile.ZipFile(self.out) as after:
            base = s.USERDATA
            original_tree = s.parse_xml(before.read(base + 'users.xml'))
            final_tree = s.parse_xml(after.read(base + 'users.xml'))
            old_warrior = s.active_warrior(original_tree)
            new_warrior = s.active_warrior(final_tree)
            self.assertEqual(old_warrior.attrib, new_warrior.attrib)
            self.assertEqual(new_warrior.find('Currencies').get('ForgeMaterial3'), '777')
            self.assertEqual(sum(i.get('Name') == 'Unlimited_Energy'
                                 for i in new_warrior.find('Items')), 1)
            self.assertEqual(after.read(base + 'users.xml'),
                             after.read(base + 'users_backup.xml'))
            for name in before.namelist():
                if name not in {
                        base + 'users.xml', base + 'users.xml.hash',
                        base + 'users_backup.xml', base + 'users_backup.xml.hash'}:
                    self.assertEqual(before.read(name), after.read(name))

    def test_green_only_does_not_add_third_material(self):
        s.patch_archive(self.src, self.out, forge_materials={'ForgeMaterial1': '12345'})
        data = s.inspect_archive(self.out, verify=True)
        self.assertEqual(data['ForgeMaterial1'], '12345')
        self.assertEqual(data['ForgeMaterial2'], '10')
        self.assertIsNone(data['ForgeMaterial3'])
        self.assertFalse(data['Unlimited_Energy'])

    def test_energy_only_and_idempotent(self):
        s.patch_archive(self.src, self.out, unlimited_energy=True)
        second = self.root / 'second.imazingapp'
        s.patch_archive(self.out, second, unlimited_energy=True)
        with zipfile.ZipFile(second) as z:
            root = s.parse_xml(z.read(s.USERDATA + 'users.xml'))
            items = s.active_warrior(root).find('Items')
            self.assertEqual(sum(item.get('Name') == 'Unlimited_Energy'
                                 for item in items), 1)
            self.assertTrue(s.inspect_archive(second, verify=True)['backup_hash_verified'])

    def test_missing_currencies_refuses_orb_patch(self):
        no_currencies = fixture(self.src, xml=XML)
        with self.assertRaises(s.SaveError):
            s.patch_archive(no_currencies, self.out,
                            forge_materials={'ForgeMaterial1': '20'})
        self.assertFalse(self.out.exists())

    def test_invalid_orb_values_refuse_output(self):
        with self.assertRaises(s.SaveError):
            s.patch_archive(self.src, self.out,
                            forge_materials={'ForgeMaterial2': '-1'})
        with self.assertRaises(s.SaveError):
            s.patch_archive(self.src, self.out,
                            forge_materials={'ForgeMaterial9': '100'})
        self.assertFalse(self.out.exists())

    def test_energy_requires_items_element(self):
        xml = self.xml.replace(b'<Items>', b'<Placeholder>').replace(
            b'</Items>', b'</Placeholder>')
        fixture(self.src, xml=xml)
        with self.assertRaises(s.SaveError):
            s.patch_archive(self.src, self.out, unlimited_energy=True)
        self.assertFalse(self.out.exists())

    def test_combined_currency_orbs_energy(self):
        s.patch_archive(self.src, self.out, money='555', bonus='333',
                        forge_materials={'ForgeMaterial3': '777'},
                        unlimited_energy=True)
        details = s.inspect_archive(self.out, verify=True)
        self.assertEqual(details['Money'], '555')
        self.assertEqual(details['Bonus'], '333')
        self.assertEqual(details['ForgeMaterial3'], '777')
        self.assertTrue(details['Unlimited_Energy'])

if __name__ == '__main__':
    unittest.main()
