# Help — Shadow Fight 2 save editor

[← English home](../README.en.md) · [Beginner's guide](START_HERE_EN.md) · [Русский](TROUBLESHOOTING.md)

**Having trouble? Don't delete the original save, reinstall the game or erase your iPhone.** First, keep a copy of your original `original.imazingapp` and your phone backup.

## “Your game data may be corrupted”

This means the game could not accept the save. It **does not always mean the same thing**.

1. Make sure you exported **your own untouched** save from the same installation of the original Shadow Fight 2.
2. In the editor, run **Verify archive and HASH** on the original file. If verification fails, **stop** and make a fresh export rather than guessing.
3. Only change coins/gems for your first try. Start with modest values; the upper limit on iOS has not been confirmed.
4. Export to a new file so your original is kept safely.
5. Restore through iMazing. **For the first launch only**, enable Airplane Mode, turn Wi-Fi off, enter SF2, complete a battle or buy an ordinary item with in-game currency, **fully close the game**, then reconnect.

If the unmodified original also fails after restore, the problem may be the restore process or game version, not just the edited hash.

## The game loaded my old money or progress

You may have restored the wrong file, imported an older snapshot, or selected cloud progress. Check your new output filename and your save's original export date. Never accept a cloud/local conflict prompt without checking the progress being offered.

**After each modified-save import (first launch only):** switch on Airplane Mode, separately disable Wi-Fi, play one battle or buy a normal item with in-game currency, fully close SF2, then reconnect. Normal subsequent launches do not require going offline. This is based on the owner's one-device experience; cloud save behavior can differ on other versions. Always keep your original backup.

## “Original hash could not be reproduced uniquely”

The editor couldn't confirm the original save checksum using the information in the file. This can happen if the save has already been edited, the original `.hash` is missing, or the version/layout is different.

**Don't** delete `.hash` files, reuse another person's device ID, or make up your own hash. Export a fresh untouched save.

## The orbs / Unlimited Energy option doesn't work

These features are included in **v1.1.0**. The owner reports that orb editing and unlimited energy worked on their iPhone, but compatibility with other iOS/game versions is unknown. If you have problems, restore your original backup. No cross-device guarantee is offered.

## The editor cannot open on Windows

The app is a **Windows `.exe`**, not an iPhone app. Download it from [the official Releases page](https://github.com/richmanstudio/ShadowFight2MoneyBonus/releases) under **Assets**. The executable isn't code-signed; do not disable system protection if you don't trust the file. You can inspect the source and run `python gui.py` with Python 3.10+ instead.

## iMazing asks for backup, restart, or Apple Account sign-in

The app-data restore may include an iPhone backup or restart, and iOS may ask you to sign in again afterward. Follow [iMazing's official documentation](https://imazing.com/guides/how-to-export-backup-and-transfer-ios-apps-data-and-settings). Don't erase or uninstall anything manually.

## Is iMazing free?

Our editor is free. iMazing is a **separate program**; some export and restore features may require a paid license.

## Still stuck?

[Create a GitHub issue](https://github.com/richmanstudio/ShadowFight2MoneyBonus/issues) with your **iOS version, Shadow Fight 2 version, iMazing version, editor version and exact error message**.

**Never upload** personal `.imazingapp`, `users.xml`, plist, device identifiers, iPhone backups or Apple Account credentials.

---

[Back to the beginner's guide](START_HERE_EN.md)
