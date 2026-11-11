# Редактор для Windows — Shadow Fight 2

> **Впервые используешь iMazing?** Начни с [простой инструкции для игроков](START_HERE.md) или [English beginner's guide](START_HERE_EN.md). Здесь подробности о программе и её дополнительных настройках.

[← README](../README.md) · [English README](../README.en.md) · [Полный гайд](GUIDE.md)

## Windows: установка и запуск

Графический редактор `gui.py` входит в этот репозиторий. Он использует ту же логику проверки и изменения сохранений, что и `sf2save.py`. Сеть не нужна; Python не отправляет данные сохранения сторонним сервисам.

**Вариант 1 — Windows .exe:** откройте [Releases](https://github.com/richmanstudio/ShadowFight2MoneyBonus/releases) и скачайте `SF2-Save-Editor-Windows.exe`, если файл опубликован в Assets релиза. Запустите его на Windows 10/11. Это неподписанная сборка из GitHub Actions; Windows может предупреждать о неизвестном издателе. Не отключайте защиту системы ради запуска: изучите исходный код и загрузите программу только из официального репозитория.

**Вариант 2 — исходный Python-код:**

1. Скачайте ZIP репозитория через **Code → Download ZIP**, распакуйте.
2. Установите Python 3.10+ с компонентом Tcl/Tk (`tkinter`).
3. Откройте PowerShell в папке репозитория и выполните:

```powershell
python gui.py
```

Если Python установлен только через launcher, выполните `py gui.py`. Пакеты через `pip` не нужны.

## Пошаговый процесс / Step by step

> [!IMPORTANT]
> **ПЕРВЫЙ запуск после импорта:** включите авиарежим, отдельно выключите Wi-Fi, откройте SF2 без интернета. **Сыграйте бой либо купите обычный предмет за внутриигровую валюту**, затем полностью закройте игру. После этого включите интернет. **Перед каждым следующим запуском отключать связь не нужно.** Повторяйте процедуру только после очередного импорта изменённого сохранения. Это пользовательское подтверждение на одном iPhone, не универсальная гарантия от облачного отката.
>
> **FIRST launch AFTER importing:** enable Airplane Mode, turn Wi-Fi off separately, start SF2 offline, **complete a battle or buy a normal item using in-game currency**, and fully close the game before reconnecting. **Normal later launches do not require Airplane Mode.** Repeat this once after each new modified-save import. This is a one-device report, not a universal cloud-sync guarantee.

1. Сделайте резервную копию iPhone. В iMazing экспортируйте **текущее, нетронутое** сохранение SF2 (`original.imazingapp`), скопируйте его в надёжное место. **Не работайте с единственной копией.**
2. Нажмите **Выбрать / Browse** и укажите этот исходный архив.
3. Нажмите **Проверить файл и HASH / Verify archive and HASH**. Проверка должна закончиться успешно. Если исходный хеш не воспроизведён, дальнейшее изменение заблокировано.
4. Укажите новые значения в полях **Money / Bonus**, отметьте валюты, которые хотите менять.
5. Нажмите **Сохранить как / Save as** для выбора нового имени. Оно не должно совпадать с исходным или с уже существующим файлом.
6. Нажмите **Создать .imazingapp / Build .imazingapp**. Программа пересчитает обе пары XML/HASH и повторно проверит готовый архив.
7. Закройте игру на iPhone, импортируйте полученный файл через iMazing (**Manage Apps → Restore App Data**). Завершите экран настройки устройства. **Один раз** запустите SF2 без интернета (авиарежим + Wi-Fi выключен), сыграйте бой или купите обычный предмет за игровую валюту, **полностью закройте игру**, затем включите интернет. Повторять офлайн-процедуру нужно только после следующего импорта.

Проверенный хеш не гарантирует совместимость любой версии игры. Если возникла ошибка, используйте [TROUBLESHOOTING.md](TROUBLESHOOTING.md) и исходный резервный файл.

## English quick instructions

1. Make a full phone backup and export a **fresh, untouched** `.imazingapp` from the original Shadow Fight 2 through iMazing.
2. In the app, **Browse** to the original and click **Verify archive and HASH**.
3. Enter your desired **Money** and/or **Bonus** values.
4. Select a **new output path** and click **Build .imazingapp**.
5. After importing through iMazing's **Restore App Data**, **launch offline once** (Airplane Mode on, Wi-Fi off), complete a battle or buy a normal item using in-game currency, and fully close SF2 before reconnecting. You can use the internet normally on later launches; repeat this procedure only after another import.

Use the language toggle in the upper-right corner to switch between Russian and English.

## Сферы и энергия / Orbs & Energy

В окне редактора добавлен отдельный блок **«Сферы зачарования и энергия»**. В нём можно:

- указать количество **зелёных** (`ForgeMaterial1`), **красных** (`ForgeMaterial2`) и **фиолетовых** (`ForgeMaterial3`) сфер;
- отметить галочкой только те сферы, которые нужно изменить; остальные значения сохраняются;
- включить **«Добавить бесконечную энергию / Add unlimited energy»** — это создаёт предмет `Unlimited_Energy` в сохранении;
- сохранить новую копию `.imazingapp` с автоматическим пересчётом двух XML/HASH-пар.

**Статус:** владелец подтвердил работу сфер и энергии на своём iPhone. Это единичный результат, а не гарантия на всех устройствах. Проверка HASH подтверждает целостность файлов, но не универсальную совместимость. Не перезаписывайте резервную копию.

**English:** In the GUI, choose one or more of **Green/Red/Purple orbs**, enter their values and tick the individual checkboxes. Enable **Add unlimited energy** to insert the `Unlimited_Energy` item. The project owner reports a successful in-game test on one iPhone. Other devices are not yet verified; always keep your original archive.

## Дизайн и технические детали

- Два языка: русский и английский.
- Офлайн: `tkinter`, `sf2save.py`; никаких дополнительных библиотек при запуске из Python.
- Проверки и обработка файлов выполняются в фоновом потоке, чтобы окно не зависало.
- Отказ от перезаписи исходника и готового файла.
- Исходные значения отображаются только после успешной проверки XML/HASH.
- Графическая оболочка не обходит проверки — использует `sf2save.patch_archive()` и повторную `sf2save.inspect_archive(..., verify=True)`.

## Безопасность

Не отправляйте чужим людям архивы, plist-файлы или идентификаторы устройства. Не публикуйте личные сохранения в GitHub Issues. Отказ от редактирования при несовпадении исходного хеша — предусмотренная мера безопасности, а не неисправность приложения.

[Официальный гайд iMazing](https://imazing.com/guides/how-to-export-backup-and-transfer-ios-apps-data-and-settings)
