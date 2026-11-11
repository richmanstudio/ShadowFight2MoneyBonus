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

- **[Stable v1.0.0 — coins and gems](https://github.com/richmanstudio/ShadowFight2MoneyBonus/releases/tag/v1.0.0)**: user-confirmed on a specific SF2 and iOS version.
- **[Test v1.1.0-beta.1 — also orbs and unlimited energy](https://github.com/richmanstudio/ShadowFight2MoneyBonus/releases/tag/v1.1.0-beta.1)**: the new features are **experimental**, not yet verified in the iOS game.

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
5. The **beta** also offers green, red and purple enchantment orbs, plus **Add unlimited energy**. These are **not yet confirmed in the iOS game**. For a first try, start with coins/gems only.
6. Click **Save as**, select a **new filename** such as **`modified.imazingapp`**, then **Build .imazingapp**.

You now have two files: the original safe backup and the newly modified copy.

## Step 4 — Put the save back on your iPhone

1. Completely close Shadow Fight 2 on the phone.
2. In iMazing, open **Manage Apps → Device → Shadow Fight 2 → Restore App Data**.
3. Choose **`modified.imazingapp`** — not the original file.
4. Follow iMazing's instructions. Your iPhone might restart, show a restore completion message, or request your Apple Account sign-in again.
5. Let iOS finish restoring the game before launching it.

Do not uninstall the game or erase your phone yourself.

## Step 5 — Play OFFLINE on EVERY launch

**Not just the first time.** Before **every** launch with a modified save:

1. Turn on **Airplane Mode**.
2. Make sure **Wi-Fi is OFF separately** — iOS may leave Wi-Fi on while Airplane Mode is active.
3. Check that cellular internet is also unavailable.
4. Open Shadow Fight 2 and stay offline until you fully close the game.

This reduces the chance of the game offering or restoring a **cloud save over your modified local progress**. It does **not** guarantee that all checks are avoided or restore overwritten data.

Now check your coins, gems, level, equipment and map.

## Common questions

**“Your game data may be corrupted”** — Don't delete the original. The save or hash may not match, or there may be a version-specific issue. [Troubleshooting](TROUBLESHOOTING_EN.md).

**My balance changed back** — Make sure you imported the new file, and check whether cloud progress was offered or selected.

**Can I do this using only an iPhone?** — No. This method requires Windows and iMazing.

**Does iMazing cost money?** — Some features may require a license; check iMazing's current terms.

**Are orbs and infinite energy guaranteed?** — No. Those are experimental options in the beta release.

**How do I report a bug?** — Use [GitHub Issues](https://github.com/richmanstudio/ShadowFight2MoneyBonus/issues). Include the game, iOS and iMazing versions and an error message, **not your personal `.imazingapp`, XML, plist, device IDs or passwords**.

---

Want technical details? [Advanced guide (Russian)](GUIDE.md) · [How hashes work](HASH.md) · [Source code](../sf2save.py).

*Unofficial project. Not affiliated with Nekki, Apple or iMazing. Compatibility with other game or iOS versions is not guaranteed.*
