#!/usr/bin/env python3
"""Shadow Fight 2 Save Editor — offline bilingual desktop interface.

Python 3.10+; tkinter and sf2save.py are the only runtime dependencies.
Run: python gui.py
"""
from __future__ import annotations

import queue
import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

import sf2save

BG = "#101317"
PANEL = "#1B2026"
FIELD = "#252C33"
FG = "#F4F2E9"
MUTED = "#A7B0B7"
ACCENT = "#D6BC83"
SUCCESS = "#A6D79A"
DANGER = "#F2A4A4"

STRINGS = {
    "ru": {
        "window": "Shadow Fight 2 — редактор сохранений",
        "eyebrow": "SHADOW FIGHT 2  /  iOS SAVE TOOL",
        "title": "Редактор сохранений",
        "subtitle": "Монеты и кристаллы. Ваш прогресс. Без джейлбрейка.",
        "lang": "ENGLISH",
        "source": "01  ИСХОДНОЕ СОХРАНЕНИЕ",
        "source_hint": "Выберите свой нетронутый экспорт .imazingapp из iMazing.",
        "browse": "Выбрать",
        "verify": "Проверить файл и HASH",
        "balance": "02  БАЛАНС И ИЗМЕНЕНИЯ",
        "forging": "03  СФЕРЫ ЗАЧАРОВАНИЯ И ЭНЕРГИЯ",
        "forging_hint": "Три цвета сфер и предмет Unlimited_Energy. Для iOS эти опции экспериментальные.",
        "orb_green": "Зелёные сферы",
        "orb_red": "Красные сферы",
        "orb_purple": "Фиолетовые сферы",
        "enable_orb_green": "Изменить зелёные",
        "enable_orb_red": "Изменить красные",
        "enable_orb_purple": "Изменить фиолетовые",
        "energy": "Добавить бесконечную энергию",
        "energy_hint": "Для проверки требуется собственная резервная копия и импорт через iMazing.",
        "balance_hint": "Значения загрузятся после успешной проверки исходного хеша.",
        "money": "Монеты (Money)",
        "bonus": "Кристаллы (Bonus)",
        "level": "Уровень",
        "not_loaded": "Не проверено",
        "modify_money": "Изменить монеты",
        "modify_bonus": "Изменить кристаллы",
        "output": "04  НОВЫЙ ПАКЕТ",
        "output_hint": "Исходный файл не перезаписывается. Выберите НОВОЕ имя.",
        "save_as": "Сохранить как",
        "build": "Создать .imazingapp",
        "idle": "Выберите исходный пакет. Все операции выполняются локально.",
        "checking": "Проверка исходного XML и контрольной суммы…",
        "working": "Создание нового пакета и повторная проверка…",
        "verified": "Исходный HASH подтверждён. Прогресс найден.",
        "finished": "Готово! Новый пакет проверен. Импортируйте его через iMazing.",
        "error": "Ошибка",
        "success": "Пакет создан",
        "generated": "Файл успешно создан и проверен:\n{path}\n\nПеред импортом сохраните резервную копию iPhone.",
        "need_file": "Выберите исходный файл .imazingapp.",
        "need_verify": "Сначала проверьте исходный пакет.",
        "need_output": "Укажите путь к новому .imazingapp.",
        "need_change": "Отметьте хотя бы одну валюту для изменения.",
        "same_path": "Выходной файл должен отличаться от исходного.",
        "disclaimer": "Только локальное сохранение. Резервная копия обязательна. Никакого подключения к сети.",
        "filetype": "Данные приложения iMazing",
    },
    "en": {
        "window": "Shadow Fight 2 — Save Editor",
        "eyebrow": "SHADOW FIGHT 2  /  iOS SAVE TOOL",
        "title": "Save Editor",
        "subtitle": "Coins and gems. Your progress. No jailbreak.",
        "lang": "РУССКИЙ",
        "source": "01  ORIGINAL SAVE",
        "source_hint": "Select a fresh, unmodified .imazingapp export from iMazing.",
        "browse": "Browse",
        "verify": "Verify archive and HASH",
        "balance": "02  BALANCE & CHANGES",
        "forging": "03  ENCHANTMENT ORBS & ENERGY",
        "forging_hint": "Three orb colors and Unlimited_Energy item. Experimental on iOS.",
        "orb_green": "Green orbs",
        "orb_red": "Red orbs",
        "orb_purple": "Purple orbs",
        "enable_orb_green": "Edit green",
        "enable_orb_red": "Edit red",
        "enable_orb_purple": "Edit purple",
        "energy": "Add unlimited energy",
        "energy_hint": "Test with your own backup and import through iMazing.",
        "balance_hint": "Values appear after the original save hash is verified.",
        "money": "Coins (Money)",
        "bonus": "Gems (Bonus)",
        "level": "Level",
        "not_loaded": "Not verified",
        "modify_money": "Edit coins",
        "modify_bonus": "Edit gems",
        "output": "04  NEW ARCHIVE",
        "output_hint": "Your original is never overwritten. Choose a NEW filename.",
        "save_as": "Save as",
        "build": "Build .imazingapp",
        "idle": "Select an original archive. All processing stays on this computer.",
        "checking": "Verifying original XML and checksum…",
        "working": "Building archive and verifying the result…",
        "verified": "Original HASH verified. Existing progress detected.",
        "finished": "Success! Output verified. Import the archive using iMazing.",
        "error": "Error",
        "success": "Archive created",
        "generated": "Archive created and verified:\n{path}\n\nBack up your iPhone before restoring app data.",
        "need_file": "Select an original .imazingapp archive.",
        "need_verify": "Verify the original archive first.",
        "need_output": "Choose an output .imazingapp path.",
        "need_change": "Select at least one currency to edit.",
        "same_path": "Output must not be the original file.",
        "disclaimer": "Local saves only. Keep a backup. No network access.",
        "filetype": "iMazing app data",
    },
}


class SaveEditor(tk.Tk):
    def __init__(self):
        super().__init__()
        self.locale = "ru"
        self.events = queue.Queue()
        self.original = tk.StringVar()
        self.destination = tk.StringVar()
        self.money = tk.StringVar()
        self.bonus = tk.StringVar()
        self.edit_money = tk.BooleanVar(value=True)
        self.edit_bonus = tk.BooleanVar(value=True)
        self.orbs = {
            key: tk.StringVar(value="0")
            for key in ("ForgeMaterial1", "ForgeMaterial2", "ForgeMaterial3")
        }
        self.edit_orbs = {
            key: tk.BooleanVar(value=False) for key in self.orbs
        }
        self.unlimited_energy = tk.BooleanVar(value=False)
        self.verified_path: Path | None = None
        self.busy = False
        self.localized = {}
        self.configure(bg=BG)
        self.geometry("900x820")
        self.minsize(760, 660)
        self._build()
        self._translate()
        self.after(120, self._poll)

    def _text(self, key):
        return STRINGS[self.locale][key]

    def _label(self, parent, key, *, font=("Segoe UI", 11), color=FG, **options):
        widget = tk.Label(parent, text="", bg=parent["bg"], fg=color, font=font, **options)
        self.localized[key + ":" + str(id(widget))] = (widget, key)
        return widget

    def _button(self, parent, key, command, accent=False):
        widget = tk.Button(
            parent, text="", command=command, font=("Segoe UI Semibold", 10),
            fg=BG if accent else FG, bg=ACCENT if accent else FIELD,
            activebackground="#EEE0B7" if accent else "#37414C",
            activeforeground=BG if accent else FG, relief="flat", bd=0,
            padx=16, pady=12, cursor="hand2",
        )
        self.localized[key + ":" + str(id(widget))] = (widget, key)
        return widget

    def _field(self, parent, variable):
        return tk.Entry(
            parent, textvariable=variable, bg=FIELD, fg=FG,
            insertbackground=FG, relief="flat", highlightthickness=1,
            highlightbackground="#3A424C", highlightcolor=ACCENT,
            font=("Consolas", 11), bd=0,
        )

    def _section(self, key, hint):
        frame = tk.Frame(self.body, bg=PANEL, padx=22, pady=18)
        frame.pack(fill="x", pady=(0, 12))
        self._label(frame, key, font=("Segoe UI Semibold", 12), color=ACCENT).pack(anchor="w")
        self._label(frame, hint, color=MUTED, font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 14))
        return frame

    def _build(self):
        header = tk.Frame(self, bg=BG, padx=30, pady=23)
        header.pack(fill="x")
        self._label(header, "eyebrow", color=ACCENT, font=("Segoe UI Semibold", 10)).pack(anchor="w")
        controls = tk.Frame(header, bg=BG)
        controls.pack(fill="x", pady=(10, 0))
        self._label(controls, "title", font=("Segoe UI Semibold", 25)).pack(side="left")
        self.language = self._button(controls, "lang", self._toggle_language)
        self.language.pack(side="right")
        self._label(header, "subtitle", color=MUTED).pack(anchor="w", pady=(4, 0))

        scroll_host = tk.Frame(self, bg=BG)
        scroll_host.pack(fill="both", expand=True)
        self.scrollbar = tk.Scrollbar(scroll_host)
        self.scrollbar.pack(side="right", fill="y")
        self.body_canvas = tk.Canvas(scroll_host, bg=BG, highlightthickness=0,
                                     yscrollcommand=self.scrollbar.set)
        self.body_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.configure(command=self.body_canvas.yview)
        self.body = tk.Frame(self.body_canvas, bg=BG, padx=30)
        self.body_window = self.body_canvas.create_window((0, 0),
                            window=self.body, anchor="nw")
        self.body.bind("<Configure>", lambda _e: self.body_canvas.configure(
            scrollregion=self.body_canvas.bbox("all")))
        self.body_canvas.bind("<Configure>", lambda e: self.body_canvas.itemconfigure(
            self.body_window, width=e.width))
        self.body_canvas.bind("<MouseWheel>", lambda e: self.body_canvas.yview_scroll(
            -int(e.delta / 120), "units"))

        section = self._section("source", "source_hint")
        row = tk.Frame(section, bg=PANEL)
        row.pack(fill="x")
        self.source_field = self._field(row, self.original)
        self.source_field.pack(side="left", fill="x", expand=True, ipady=10)
        self.pick_source = self._button(row, "browse", self._choose_source)
        self.pick_source.pack(side="left", padx=(8, 0))
        self.verify_btn = self._button(section, "verify", self._verify, accent=True)
        self.verify_btn.pack(anchor="w", pady=(12, 0))

        section = self._section("balance", "balance_hint")
        line = tk.Frame(section, bg=PANEL)
        line.pack(fill="x", pady=(0, 10))
        self.current_value = tk.Label(
            line, text="", bg=PANEL, fg=SUCCESS, font=("Segoe UI", 10), anchor="w"
        )
        self.current_value.pack(side="left", fill="x", expand=True)
        self.level_value = tk.Label(
            line, text="", bg=PANEL, fg=MUTED, font=("Segoe UI", 10)
        )
        self.level_value.pack(side="right")

        columns = tk.Frame(section, bg=PANEL)
        columns.pack(fill="x")
        for col, label, var, checked in [
            (0, "money", self.money, self.edit_money),
            (1, "bonus", self.bonus, self.edit_bonus),
        ]:
            area = tk.Frame(columns, bg=PANEL)
            area.grid(row=0, column=col, sticky="ew", padx=(0, 16 if col == 0 else 0))
            self._label(area, label, color=MUTED, font=("Segoe UI", 10)).pack(anchor="w")
            self._field(area, var).pack(fill="x", ipady=9, pady=(6, 8))
            cb = tk.Checkbutton(
                area, text="", variable=checked, bg=PANEL, fg=FG,
                selectcolor=FIELD, activebackground=PANEL, activeforeground=FG,
                font=("Segoe UI", 10), bd=0, highlightthickness=0,
            )
            self.localized[("modify_money" if col == 0 else "modify_bonus") + ":cb"] = (
                cb, "modify_money" if col == 0 else "modify_bonus"
            )
            cb.pack(anchor="w")
        columns.columnconfigure(0, weight=1)
        columns.columnconfigure(1, weight=1)

        forge = self._section("forging", "forging_hint")
        orb_row = tk.Frame(forge, bg=PANEL)
        orb_row.pack(fill="x")
        for col, (key, title, edit_key) in enumerate([
            ("ForgeMaterial1", "orb_green", "enable_orb_green"),
            ("ForgeMaterial2", "orb_red", "enable_orb_red"),
            ("ForgeMaterial3", "orb_purple", "enable_orb_purple"),
        ]):
            area = tk.Frame(orb_row, bg=PANEL)
            area.grid(row=0, column=col, sticky="ew",
                      padx=(0, 12 if col < 2 else 0))
            self._label(area, title, color=MUTED,
                        font=("Segoe UI", 10)).pack(anchor="w")
            self._field(area, self.orbs[key]).pack(fill="x", ipady=9, pady=(6, 8))
            cb = tk.Checkbutton(
                area, text="", variable=self.edit_orbs[key], bg=PANEL, fg=FG,
                selectcolor=FIELD, activebackground=PANEL, activeforeground=FG,
                font=("Segoe UI", 10), bd=0, highlightthickness=0)
            self.localized[edit_key + ":cb"] = (cb, edit_key)
            cb.pack(anchor="w")
            orb_row.columnconfigure(col, weight=1)

        energy_box = tk.Frame(forge, bg=PANEL)
        energy_box.pack(fill="x", pady=(14, 0))
        cb_energy = tk.Checkbutton(
            energy_box, text="", variable=self.unlimited_energy, bg=PANEL, fg=FG,
            selectcolor=FIELD, activebackground=PANEL, activeforeground=FG,
            font=("Segoe UI Semibold", 11), bd=0, highlightthickness=0)
        self.localized["energy:cb"] = (cb_energy, "energy")
        cb_energy.pack(anchor="w")
        self._label(energy_box, "energy_hint", color=MUTED,
                    font=("Segoe UI", 9)).pack(anchor="w", pady=(4, 0))

        section = self._section("output", "output_hint")
        output_row = tk.Frame(section, bg=PANEL)
        output_row.pack(fill="x")
        self.output_field = self._field(output_row, self.destination)
        self.output_field.pack(side="left", fill="x", expand=True, ipady=10)
        self.pick_output = self._button(output_row, "save_as", self._choose_output)
        self.pick_output.pack(side="left", padx=(8, 0))
        self.build_btn = self._button(section, "build", self._generate, accent=True)
        self.build_btn.pack(anchor="w", pady=(12, 0))

        footer = tk.Frame(self, bg=BG, padx=30, pady=15)
        footer.pack(fill="x", side="bottom")
        self.status = tk.Label(
            footer, text="", bg=BG, fg=MUTED, font=("Segoe UI", 10),
            anchor="w", justify="left", wraplength=760,
        )
        self.status.pack(fill="x")
        self._label(footer, "disclaimer", color=MUTED, font=("Segoe UI", 9)).pack(
            anchor="w", pady=(10, 0)
        )

    def _translate(self):
        self.title(self._text("window"))
        for widget, key in self.localized.values():
            widget.configure(text=self._text(key))
        if self.verified_path is None:
            self.current_value.configure(text=self._text("not_loaded"))
        if not self.busy:
            self.status.configure(text=self._text("idle"))

    def _toggle_language(self):
        self.locale = "en" if self.locale == "ru" else "ru"
        self._translate()

    def _set_busy(self, value):
        self.busy = value
        state = tk.DISABLED if value else tk.NORMAL
        for widget in (self.verify_btn, self.build_btn, self.pick_source, self.pick_output):
            widget.configure(state=state)

    def _choose_source(self):
        name = filedialog.askopenfilename(
            title=self._text("browse"),
            filetypes=[(self._text("filetype"), "*.imazingapp"), ("All files", "*.*")]
        )
        if name:
            self.original.set(name)
            self.verified_path = None
            self.current_value.configure(text=self._text("not_loaded"))
            p = Path(name)
            self.destination.set(str(p.with_name(p.stem + "_modified.imazingapp")))

    def _choose_output(self):
        name = filedialog.asksaveasfilename(
            title=self._text("save_as"), defaultextension=".imazingapp",
            filetypes=[(self._text("filetype"), "*.imazingapp")],
            initialfile="modified.imazingapp",
        )
        if name:
            self.destination.set(name)

    def _worker(self, kind, action):
        def run():
            try:
                self.events.put((kind, True, action()))
            except Exception as exc:
                self.events.put((kind, False, str(exc)))
        threading.Thread(target=run, daemon=True).start()

    def _verify(self):
        value = self.original.get().strip()
        if not value:
            messagebox.showerror(self._text("error"), self._text("need_file"))
            return
        self.verified_path = None
        self._set_busy(True)
        self.status.configure(text=self._text("checking"), fg=ACCENT)
        path = Path(value)
        self._worker("verify", lambda: (path, sf2save.inspect_archive(path, verify=True)))

    def _generate(self):
        source = Path(self.original.get().strip())
        if self.verified_path is None or self.verified_path != source:
            messagebox.showerror(self._text("error"), self._text("need_verify"))
            return
        destination = self.destination.get().strip()
        if not destination:
            messagebox.showerror(self._text("error"), self._text("need_output"))
            return
        target = Path(destination)
        if target.resolve() == source.resolve():
            messagebox.showerror(self._text("error"), self._text("same_path"))
            return
        if not (self.edit_money.get() or self.edit_bonus.get()
                or any(v.get() for v in self.edit_orbs.values())
                or self.unlimited_energy.get()):
            messagebox.showerror(self._text("error"), self._text("need_change"))
            return
        money = self.money.get().strip() if self.edit_money.get() else None
        bonus = self.bonus.get().strip() if self.edit_bonus.get() else None
        forge_materials = {
            key: self.orbs[key].get().strip()
            for key in self.orbs if self.edit_orbs[key].get()
        }
        try:
            if money is not None:
                sf2save.currency_value(money)
            if bonus is not None:
                sf2save.currency_value(bonus)
            for value in forge_materials.values():
                sf2save.currency_value(value)
        except sf2save.SaveError as exc:
            messagebox.showerror(self._text("error"), str(exc))
            return

        self._set_busy(True)
        self.status.configure(text=self._text("working"), fg=ACCENT)

        def work():
            result = sf2save.patch_archive(
                source, target, money=money, bonus=bonus,
                unlimited_energy=self.unlimited_energy.get(),
                forge_materials=forge_materials)
            validation = sf2save.inspect_archive(target, verify=True)
            if not validation.get("original_hash_verified") or not validation.get("backup_hash_verified"):
                raise sf2save.SaveError("Output XML/hash verification failed.")
            return result

        self._worker("patch", work)

    def _poll(self):
        try:
            while True:
                kind, ok, payload = self.events.get_nowait()
                self._set_busy(False)
                if not ok:
                    self.status.configure(text=payload, fg=DANGER)
                    messagebox.showerror(self._text("error"), payload)
                    continue
                if kind == "verify":
                    path, result = payload
                    if Path(self.original.get().strip()) != path:
                        continue
                    self.verified_path = path
                    self.money.set(result.get("Money") or "")
                    self.bonus.set(result.get("Bonus") or "")
                    for key in self.orbs:
                        self.orbs[key].set(result.get(key) or "0")
                        self.edit_orbs[key].set(False)
                    self.unlimited_energy.set(bool(result.get("Unlimited_Energy")))
                    self.current_value.configure(text=self._text("verified"), fg=SUCCESS)
                    self.level_value.configure(
                        text=f'{self._text("level")}: {result.get("Level") or "?"}'
                    )
                    self.status.configure(text=self._text("verified"), fg=SUCCESS)
                elif kind == "patch":
                    self.status.configure(text=self._text("finished"), fg=SUCCESS)
                    messagebox.showinfo(
                        self._text("success"),
                        self._text("generated").format(path=payload["output"]),
                    )
        except queue.Empty:
            pass
        self.after(120, self._poll)


def main():
    SaveEditor().mainloop()


if __name__ == "__main__":
    main()
