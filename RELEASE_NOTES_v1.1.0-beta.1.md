# ShadowFight2MoneyBonus v1.1.0-beta.1

**Test build — experimental features need in-game confirmation on iOS.**

This release extends the proven coins/gems editor with additional fields present in Shadow Fight 2 save XML.

## New

- **Three enchantment orbs:** Edit `ForgeMaterial1` (green), `ForgeMaterial2` (red), and `ForgeMaterial3` (purple) under `Warrior/Currencies`. The editor can add `ForgeMaterial3` if its attribute is missing in an existing `Currencies` element.
- **Unlimited Energy:** Add one `Unlimited_Energy` inventory item to `Warrior/Items`. Re-running the tool does not duplicate the item.
- **Windows GUI:** Added individual orb fields and checkboxes, plus an Unlimited Energy switch. Russian/English localization retained.
- **CLI:** New optional flags `--orb-green`, `--orb-red`, `--orb-purple`, `--unlimited-energy`.
- **Preservation:** Changes are applied only to the active character's requested attributes/items. Main and backup XML and their hashes are rebuilt; unrelated archived data is preserved.
- Expanded automated tests for individual materials, missing `ForgeMaterial3`, combined edits, idempotent energy, invalid values and refusal on missing `Currencies` or `Items`.

## First test with your own save

1. Back up your iPhone and keep a separate copy of your original `.imazingapp`.
2. Use `SF2-Save-Editor-Windows.exe` from this beta release, or run `python gui.py` (Python 3.10+).
3. Verify the **original unmodified archive**. If the original hash fails verification, stop.
4. Try small amounts and optionally tick **Add unlimited energy**. Export a **new** archive.
5. Recheck the output, restore through iMazing, then launch SF2 **fully offline**. Use Airplane Mode and separately turn off Wi-Fi before each launch; keep the game offline throughout the session.
6. Check whether energy/orbs actually work. If not, restore the original archive and open an issue with only non-sensitive versions/errors. **Never upload your personal XML, plist or .imazingapp.**

## CLI example

```powershell
python sf2save.py patch "D:\SF2\original.imazingapp" --output "D:\SF2\experimental.imazingapp" --orb-green 100000 --orb-red 50000 --orb-purple 10000 --unlimited-energy
python sf2save.py verify "D:\SF2\experimental.imazingapp"
```

## What is and isn't verified

**Automated:** ZIP integrity, original and output hash consistency, synthetic fixture XML correctness, structural and data preservation, GUI import, and Windows executable build.

**Not yet verified in game on iOS:** Unlimited Energy actually activating; all three orb balances changing after restore and staying consistent.

The previously documented coins/gems flow remains supported. This is a **pre-release** until the new features are verified on a real iPhone. No server-side purchases or online resources are modified.

[README (RU)](README.md) · [README (EN)](README.en.md) · [GUI guide](docs/GUI.md) · [Validation](docs/VALIDATION.md)

Unofficial tool; not affiliated with Nekki, Apple or iMazing.
