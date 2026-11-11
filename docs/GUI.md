# Shadow Fight 2 Save Editor — графический интерфейс / GUI

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

1. Сделайте резервную копию iPhone. В iMazing экспортируйте **текущее, нетронутое** сохранение SF2 (`original.imazingapp`), скопируйте его в надёжное место. **Не работайте с единственной копией.**
2. Нажмите **Выбрать / Browse** и укажите этот исходный архив.
3. Нажмите **Проверить файл и HASH / Verify archive and HASH**. Проверка должна закончиться успешно. Если исходный хеш не воспроизведён, дальнейшее изменение заблокировано.
4. Укажите новые значения в полях **Money / Bonus**, отметьте валюты, которые хотите менять.
5. Нажмите **Сохранить как / Save as** для выбора нового имени. Оно не должно совпадать с исходным или с уже существующим файлом.
6. Нажмите **Создать .imazingapp / Build .imazingapp**. Программа пересчитает обе пары XML/HASH и повторно проверит готовый архив.
7. Закройте игру на iPhone, импортируйте полученный файл через iMazing (**Manage Apps → Restore App Data**). Завершите экран настройки устройства и проверьте прогресс и валюту в игре.

Проверенный хеш не гарантирует совместимость любой версии игры. Если возникла ошибка, используйте [TROUBLESHOOTING.md](TROUBLESHOOTING.md) и исходный резервный файл.

## English quick instructions

1. Make a full phone backup and export a **fresh, untouched** `.imazingapp` from the original Shadow Fight 2 through iMazing.
2. In the app, **Browse** to the original and click **Verify archive and HASH**.
3. Enter your desired **Money** and/or **Bonus** values.
4. Select a **new output path** and click **Build .imazingapp**.
5. Only after the success dialog, import the generated package through iMazing's **Restore App Data** and verify the game state.

Use the language toggle in the upper-right corner to switch between Russian and English.

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
