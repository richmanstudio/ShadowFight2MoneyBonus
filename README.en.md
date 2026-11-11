# ShadowFight2MoneyBonus

**Change coins and gems in the original Shadow Fight 2 on iPhone, without jailbreaking or replacing your own save.**

[Русский README](README.md) · [Detailed guide (Russian)](docs/GUIDE.md) · [Hash algorithm](docs/HASH.md) · [Troubleshooting](docs/TROUBLESHOOTING.md) · [GUI instructions](docs/GUI.md)

> **Compatibility evidence:** One owner-reported successful test on Shadow Fight 2 **2.46.0**, **iOS 27.2**, and Windows with iMazing. This is not a guarantee for other game or iOS versions. Always start by verifying the hash of your own untouched save.

## What it does

This project edits your **existing local app-data export** rather than providing somebody else's saved game or a modified IPA. It can:

- Read an exported `.imazingapp` archive.
- Verify the original `users.xml.hash` using the matching value found in the archive's local app preferences.
- Change the active character's `Money` (coins) and/or `Bonus` (gems).
- Update both `users.xml` and `users_backup.xml` with matching `.hash` files.
- Verify the new archive, while preserving all other files in the archive.
- Offer a **Windows graphical interface** (`gui.py`) or a Python command-line interface (`sf2save.py`).

The tool works **offline**, does not require your Apple Account password, and never sends your archive to a server. It does not directly connect to your phone: **iMazing performs the export and restore**.

It does not unlock paid content, impersonate purchases, or modify server-owned resources.

## Requirements

- Windows computer, iPhone with the original Shadow Fight 2.
- iMazing, installed separately (its relevant features may require a license).
- **For source-code usage:** Python 3.10+; the project itself uses only the Python standard library, including Tkinter for the GUI.
- **For a standalone Windows executable:** Download the `.exe` from [Releases](https://github.com/richmanstudio/ShadowFight2MoneyBonus/releases) when available. No Python install is needed for the bundled build.

**Before you do anything:** back up the iPhone, export a **fresh unmodified** app save, and keep that original archive somewhere safe. An exported snapshot will not include progress you make later.

## Option A: Windows GUI (recommended)

1. Download the source ZIP from GitHub and extract it (or download the Windows executable from a release).
2. With Python installed, launch `python gui.py` from the repository folder. For the standalone build, open the released `.exe`.
3. In iMazing, use **Manage Apps → Device → Shadow Fight 2 → Back Up / Export App Data**. Save a fresh `original.imazingapp` from your iPhone.
4. In the GUI, select that **untouched** `.imazingapp` file and press **Verify archive and HASH**. If verification fails, **stop**. Do not use an edited file as your supposed original.
5. Select the currencies you want to change and enter the desired numbers.
6. Choose a **different** output filename, such as `modified.imazingapp`. Click **Build .imazingapp**.
7. Only after successful output verification, close the game on your iPhone and use iMazing's **Restore App Data** feature to import the new archive. Follow the iOS recovery/setup screens and confirm that the level, inventory and currency are correct.

The editor does not overwrite an existing output file. Do not delete the original save.

[GUI instructions and screenshots guidance](docs/GUI.md)

## Option B: Command-line usage

Download and unzip the repository, then open PowerShell in the folder with `sf2save.py`.

**Inspect** the XML balance without verifying the hash:

```powershell
python sf2save.py inspect "D:\SF2\original.imazingapp"
```

**Verify** the original hash before editing:

```powershell
python sf2save.py verify "D:\SF2\original.imazingapp"
```

The JSON output must include `"original_hash_verified": true`. If a backup exists, review `backup_hash_verified` as well.

**Patch** the existing save into a separate output archive:

```powershell
python sf2save.py patch "D:\SF2\original.imazingapp" --output "D:\SF2\modified.imazingapp" --money 10000000 --bonus 1000
```

**Re-check** the new archive:

```powershell
python sf2save.py verify "D:\SF2\modified.imazingapp"
```

The values above are **examples**, not tested maximums. You can omit `--money` or `--bonus` if you want to change only one currency. On Windows, `py` may be used instead of `python`.

## How is the hash calculated?

A Shadow Fight 2 save is **not** protected by a plain MD5 of the file. For the tested format, a normalized XML representation is hashed and combined with a device-specific value, the app identifier and a constant suffix:

```text
first = UPPERCASE_HEX(MD5(UTF8(normalized_xml)))
hash  = UPPERCASE_HEX(MD5(UTF8(first + device_value + app_id + suffix)))
```

The implementation derives possible device values from the **local** Preferences plist and accepts a candidate only when it reproduces the **original untouched hash exactly**. Unknown or ambiguous values fail closed. The XML is not reserialized; the existing textual format is preserved except for the chosen numeric attributes.

[Technical method, normalization caveats and research credit](docs/HASH.md)

## What remains unchanged?

The active character's level, experience, items, fight history and other XML attributes are preserved. All unrelated archive entries, including plist and binary data, keep their original contents. Both resulting save XML files are consistent; your **original** archive and its earlier backup remain unchanged.

Please note that importing an app-data snapshot rolls back any gameplay since that snapshot. Export your newest progress and stop playing until restore is complete.

## Troubleshooting

- **“Your game data may be corrupted”**: Check the original save hash first, then verify the output. Missing hashes or hashes carried over from an edited save can trigger integrity failures. The same message can have other causes.
- **“Original hash could not be reproduced uniquely”**: Your archive may not contain a matching original XML/hash pair, device identifier or supported XML format. Export a fresh untouched save; do **not** guess a device ID.
- **Balances revert**: Confirm which archive was imported, whether a backup or cloud save was chosen, and whether the game has server-side state.
- **Unexpected money display in later chapters**: Some currencies use scaling/denomination values. Do not change those fields without validating the result.
- **Python or Tkinter unavailable**: Install Python from python.org with Tcl/Tk support, or use a Windows executable from a release.

[Full troubleshooting guide (Russian)](docs/TROUBLESHOOTING.md)

## Verification & tests

Unit tests use **synthetic fixtures**, not personal account data. The CI matrix runs tests on Windows and Linux using Python 3.10 and 3.13:

```powershell
python -m unittest discover -s tests -v
```

A passing test suite confirms the tool's logic, **not** universal in-game compatibility. Read [validation scope](docs/VALIDATION.md).

## Privacy and responsible use

Never upload actual `.imazingapp` files, `users.xml`, `.plist`, Apple credentials or device identifiers to a public GitHub issue. They may expose private account or device information. For bug reports, include only your app/iOS/iMazing version, a redacted error and a synthetic sample where possible.

This is an unofficial research/utility project, not affiliated with Nekki, Apple or iMazing. Use it only with saves you own, and understand the game or platform rules that may apply. This repository ships no copyrighted game assets or pirated IPA files.

## Credits and license

- [Original hash-algorithm investigation](https://github.com/moltinginstar/sf2mod/blob/main/WRITEUP.md), performed on Android; the source of the constant and general formula.
- [iMazing's official app-data export/restore guide](https://imazing.com/guides/how-to-export-backup-and-transfer-ios-apps-data-and-settings).
- [MIT License](LICENSE).
