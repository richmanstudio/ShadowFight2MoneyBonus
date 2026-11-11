# ShadowFight2MoneyBonus v1.0.0

First public release of the offline **Shadow Fight 2 iOS save editor**, with a Windows desktop application and bilingual documentation.

## Included

- **Windows GUI** (`SF2-Save-Editor-Windows.exe`): browse for your own untouched `.imazingapp`, verify the existing hash, edit Money/Bonus, and export a new verified archive.
- **Python GUI** (`gui.py`): same functionality for users who prefer running from source (Python 3.10+, Tkinter).
- **CLI** (`sf2save.py`): `inspect`, `verify`, and `patch` commands, with no external runtime packages.
- **Russian + English documentation**: [Русский](README.md) / [English](README.en.md), [GUI walkthrough](docs/GUI.md), [hash algorithm](docs/HASH.md), [known limitations](docs/VALIDATION.md).
- Checks for the original save hash, XML validity, ZIP integrity, and both output XML/hash pairs. The original archive is never overwritten.

## Quick start (Windows)

1. Back up your iPhone; export a **fresh, untouched** SF2 save using iMazing.
2. Download the `.exe` below and launch it, or open `gui.py` with Python 3.10+.
3. Select the original `.imazingapp` and click **Verify archive and HASH**.
4. Choose the new coin/gem amounts and a **new output filename**.
5. Click **Build .imazingapp** and import the result with iMazing's **Restore App Data**.
6. **Only for the first launch after each import:** turn on Airplane Mode and separately turn Wi-Fi off. Start SF2 offline, **complete one battle or buy an ordinary item with in-game currency**, fully close the game, and then reconnect. Normal later launches do not require Airplane Mode. This is the project owner's reported successful procedure on one device, not a universal cloud-sync guarantee.

Windows may display an unknown-publisher warning because this open-source executable is not code-signed. Download only from this repository. You can review the source or run `python gui.py` instead.

## Validation scope

One owner-reported real-device success on original Shadow Fight 2 **2.46.0**, **iOS 27.2**, Windows + iMazing. Automated tests cover synthetic fixtures on Windows and Linux. Other game versions, iOS versions, phones and server-controlled resources are not guaranteed. Do not publish your personal app-data archives or device identifiers.

**This project is unofficial and is not affiliated with Nekki, Apple or iMazing.**
