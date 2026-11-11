# Beginner's guide — Shadow Fight 2 on iPhone

[← Home](../README.en.md) · [Русская инструкция](START_HERE.md) · [Troubleshooting](TROUBLESHOOTING_EN.md)

**Want to change coins or gems in your own Shadow Fight 2 save, without writing code?** Follow these steps.

First, this is a **Windows PC tool**, **not an iPhone app**. You need a Windows computer, your iPhone, a cable and **iMazing**. You do **not** need to jailbreak your iPhone.

## What you need

| Item | Why |
|---|---|
| iPhone with the **original Shadow Fight 2** | Your game and your progress |
| Windows 10/11 PC | Run the save editor |
| iPhone cable | Connect your phone |
| **iMazing** | Export your game's data and put it back |
| **Our editor** | Change the values in your save |

iMazing is a separate product. Export/restore features **may require a paid license**. Our editor is free, but does not replace iMazing.

## Step 1 — Download the editor

Choose a version:

- **[Current v1.1.0 — coins, gems, all three orbs & unlimited energy](https://github.com/richmanstudio/ShadowFight2MoneyBonus/releases/tag/v1.1.0)**: all features have been reported working by the owner on one iPhone.
- **[Older v1.0.0 — coins & gems only](https://github.com/richmanstudio/ShadowFight2MoneyBonus/releases/tag/v1.0.0)**.

On the release page, find **Assets** and download **`SF2-Save-Editor-Windows.exe`**. You open this on **Windows**, not your phone.

The app is not digitally signed. If Windows displays an unknown-publisher warning, don't turn off protection to install it; verify the repository/source first and don't run files you don't trust.

## Step 2 — Back up your actual game progress

1. Finish your current battle and completely close Shadow Fight 2.
2. Install [iMazing](https://imazing.com/) on the PC.
3. Connect and unlock your iPhone. Approve the trust prompt if asked.
4. **Make a backup of your iPhone** in iMazing.
5. Go to **Manage Apps → Device → Shadow Fight 2 → Back Up / Back Up App Data**.
6. Save the exported file as **`original.imazingapp`** somewhere safe.

Menu wording can differ between iMazing versions. See the [official iMazing walkthrough](https://imazing.com/guides/how-to-export-backup-and-transfer-ios-apps-data-and-settings).

**Do not delete, replace or edit the original file.** It is your way back if something goes wrong. It contains your progress **as of the export**; future battles are not merged into it.

## Step 3 — Change the values

1. Open **`SF2-Save-Editor-Windows.exe`** on the PC.
2. Click **Browse** and select the untouched **`original.imazingapp`**.
3. Click **Verify archive and HASH**. In simple terms, this checks that your original save is intact and recognizable. If verification **fails, stop**.
4. Enter the desired **Coins (Money)** and/or **Gems (Bonus)**, ticking only the values you want to change.
5. **v1.1.0** also offers green, red and purple enchantment orbs, plus **Add unlimited energy**. The owner reports these worked on their iPhone, but other devices and versions have not been verified.
6. Click **Save as**, select a **new filename** such as **`modified.imazingapp`**, then **Build .imazingapp**.

You now have two files: the original safe backup and the newly modified copy.

## Step 4 — Put the save back on your iPhone

1. Completely close Shadow Fight 2 on the phone.
2. In iMazing, open **Manage Apps → Device → Shadow Fight 2 → Restore App Data**.
3. Choose **`modified.imazingapp`** — not the original file.
4. Follow iMazing's instructions. Your iPhone might restart, show a restore completion message, or request your Apple Account sign-in again.
5. Let iOS finish restoring the game before launching it.

Do not uninstall the game or erase your phone yourself.

## Step 5 — One OFFLINE launch after importing

**You do NOT need to go offline every time you open the game.** The project owner's successful procedure after each modified-save import was:

1. **Before opening the game for the first time**, turn on **Airplane Mode**.
2. Turn **Wi-Fi OFF separately** — iOS can leave Wi-Fi enabled in Airplane Mode. Cellular internet should also be unavailable.
3. **Open Shadow Fight 2 offline.**
4. **Finish one battle OR buy a normal item with in-game currency.** You do not need to spend real money. This gives the game a chance to write its updated save state.
5. **Fully close the game**, keeping the phone offline.
6. **Reconnect to the internet.** You can launch the game normally afterward.

**Repeat this process only after another modified-save import.**

This is a successful procedure **reported by one iPhone user**, not a guarantee of cloud-sync behavior across versions. If you see a local-vs-cloud save selection, check both carefully before choosing. Keep your untouched `original.imazingapp`.

## Common questions

**“Your game data may be corrupted”** — Don't delete the original. The save or hash may not match, or there may be a version-specific issue. [Troubleshooting](TROUBLESHOOTING_EN.md).

**My balance changed back** — Make sure you imported the new file, and check whether cloud progress was offered or selected.

**Can I do this using only an iPhone?** — No. This method requires Windows and iMazing.

**Does iMazing cost money?** — Some features may require a license; check iMazing's current terms.

**Do orbs and unlimited energy work?** — The owner reports success on one iPhone. Other phones and versions are not guaranteed. Keep a full backup.

**How do I report a bug?** — Use [GitHub Issues](https://github.com/richmanstudio/ShadowFight2MoneyBonus/issues). Include the game, iOS and iMazing versions and an error message, **not your personal `.imazingapp`, XML, plist, device IDs or passwords**.

---

Want technical details? [Advanced guide (Russian)](GUIDE.md) · [How hashes work](HASH.md) · [Source code](../sf2save.py).

*Unofficial project. Not affiliated with Nekki, Apple or iMazing. Compatibility with other game or iOS versions is not guaranteed.*
