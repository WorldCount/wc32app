#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Консоль
"""

__date__ = "15.04.2016"
__author__ = "WorldCount"
__email__ = "world.count@yandex.ru"
__copyright__ = "Copyright 2016, Scr1pt1k.Ru"
__python_version__ = "3"


import os
from PyQt5.QtWidgets import (QWidget, QTextEdit, QLineEdit, QVBoxLayout, QHBoxLayout, QCompleter)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtCore import (Qt, pyqtSignal, QStringListModel, QEvent)
from .wcwidgets import WCFlagUserKeyboard
import win32api


class WCCommandCompleter(QCompleter):

    def __init__(self, parent):
        super(WCCommandCompleter, self).__init__()
        self.setWidget(parent)

    # Метод: обновляет данные в модели
    def update_model(self, complete_list):
        model = QStringListModel(complete_list, self)
        self.setModel(model)

    # Обработчик: выводит совпадения
    def update(self, prefix):
        self.setCompletionPrefix(prefix)
        if prefix.strip() != '':
            self.complete()


# Класс: командная строка
class WCCommandLine(QLineEdit):

    """
    Класс дисплея консоли
    @author WorldCount
    @version 4
    @date 2016/04/15
    """

    change_word_count = pyqtSignal(int)
    text_changed = pyqtSignal(object)

    # Конструктор
    def __init__(self, *args):
        super(WCCommandLine, self).__init__(*args)
        # Количество слов
        self._word_count = 0
        # Последнее слово
        self._last_word = ''
        self._prefix = ''
        # Список введенных команд
        self._save_command = []
        self._current_command_num = 0
        # Список команд
        self._command_list = [['cls'], ['debug'], ['command'], ['exit']]
        # Текущий список команд
        self._current_command_list = self._command_list[:]
        # Текущий список завершения
        self._current_complete = []
        # Инициализация
        self._init_ui()
        self._init_connect()

    # Конструктор: настройки виджета
    def _init_ui(self):
        self.setFixedHeight(32)
        # Создаем список автозавершения
        self.create_complete_list()
        # Создаем комплитер
        self._completer = WCCommandCompleter(self)
        self.update_completer()

    # Конструктор: слушатели
    def _init_connect(self):
        self._completer.activated.connect(self._complete_text)
        self.textChanged.connect(self._text_change)
        self.text_changed.connect(self._completer.update)

    # Метод: возвращает количество слов
    def get_world_count(self):
        return self._word_count

    # Метод: обновляет данные комплитера
    def update_completer(self):
        self._completer.update_model(self._current_complete)

    # Метод: добавляет команду
    def add_command(self, command):
        complete_list = command.get_complete_list
        if complete_list not in self._command_list:
            self._command_list.append(complete_list)

    # Метод: удаляет команду
    def remove_command(self, command):
        complete_list = command.get_complete_list
        if complete_list in self._command_list:
            self._command_list.remove(complete_list)

    # Метод: сохраняет введеную команду
    def save_command(self, command):
        if command not in self._save_command:
            self._save_command.append(command)
            self._current_command_num = len(self._save_command) - 1

    # Метод: создает список автозавершения
    def create_complete_list(self):
        res_cmd = []
        res_complete = []
        if self._last_word == '':
            for cmd in self._command_list:
                try:
                    cmd_name = cmd[0]
                    if cmd_name not in res_complete:
                        res_complete.append(cmd_name)
                    res_cmd.append(cmd)
                except Exception:
                    continue
        else:
            for cmd in self._current_command_list:
                try:
                    if self._last_word == cmd[self._word_count - 1]:
                        offset = cmd[self._word_count]
                        if offset not in res_complete:
                            res_complete.append(offset)
                        res_cmd.append(cmd)
                except Exception:
                    continue

        self._current_command_list = res_cmd[:]
        self._current_complete = res_complete[:]

    # Метод: обновляет данные по словам
    def update_word(self):
        all_text = self.text().split()
        try:
            self._last_word = all_text[-1].strip()
        except IndexError:
            self._last_word = ''
        # Сигнал с количеством слов
        self._word_count = len(all_text)
        self.change_word_count.emit(self.get_world_count())
        # Обновляем список слов автозавершения
        self.create_complete_list()
        self.update_completer()

    # Обработчик: комплитер активировался
    def _complete_text(self, text):
        cur_pos = self.cursorPosition()
        form_text = self.text()
        before_text = form_text[:cur_pos]
        after_text = form_text[cur_pos:]
        try:
            prefix_len = len(before_text.split()[-1].strip())
        except IndexError:
            prefix_len = 0
        ins_text = '%s%s %s' % (before_text[:cur_pos - prefix_len], text, after_text)
        self.setText(ins_text)
        self.setCursorPosition(cur_pos - prefix_len + len(text) + 2)
        self.update_word()

    # Обработчик: текст изменился
    def _text_change(self, text):
        text = self.text()[:self.cursorPosition()]
        try:
            self._prefix = text.split()[-1].strip()
        except IndexError:
            self._prefix = ''
        self.text_changed.emit(self._prefix)

    # Обработчик: нажатие клавиш
    def keyPressEvent(self, event):
        super(WCCommandLine, self).keyPressEvent(event)

        # [Space], [BackSpace], [Delete]
        if event.key() in [Qt.Key_Space, Qt.Key_Backspace, Qt.Key_Delete]:
            self.update_word()

        # стрелка вверх
        if event.key() == 16777235:
            if len(self._save_command) > 0:
                self._current_command_num -= 1

                if self._current_command_num > len(self._save_command) - 1:
                    self._current_command_num = len(self._save_command) - 1

                if self._current_command_num < 0:
                    self._current_command_num = 0

                self.setText(self._save_command[self._current_command_num])
                self.end(True)

        # стрелка вниз
        if event.key() == 16777237:
            if len(self._save_command) > 0:
                self._current_command_num += 1

                if self._current_command_num > len(self._save_command) - 1:
                    self._current_command_num = len(self._save_command) - 1

                if self._current_command_num < 0:
                    self._current_command_num = 0

                self.setText(self._save_command[self._current_command_num])
                self.end(True)

    # Обработчик: события
    def event(self, event):
        # Нажатие [TAB]
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self._complete_text(self._completer.currentCompletion())
            return True

        return super(WCCommandLine, self).event(event)


# Класс: дисплей
class WCDisplay(QTextEdit):

    """
    Класс дисплея консоли
    @author WorldCount
    @version 4
    @date 2016/04/15
    """

    # Конструктор
    def __init__(self, parent=None):
        super(WCDisplay, self).__init__(parent)
        self._parent = parent
        self._path = os.path.dirname(__file__)
        # Инициализация
        self._init_ui()

    # Конструктор: компоненты виджета
    def _init_ui(self):
        self.setReadOnly(True)


# Класс: консоль
class WCConsole(QWidget):

    """
    Класс консоли
    @author WorldCount
    @version 4
    @date 2016/04/15
    """

    # Сигнал: смена языка
    lang_change = pyqtSignal()

    # Конструктор
    def __init__(self, parent=None):
        super(WCConsole, self).__init__(parent)
        self._parent = parent
        self._path = os.path.dirname(__file__)
        self._name = self.__class__.__name__
        # Инициализация
        self._init_ui()
        self._init_widget()
        self._init_connect()

    # Конструктор: настройки виджета
    def _init_ui(self):
        self.setWindowTitle(self._name)
        self.setWindowIcon(QIcon(os.path.join(self._path, 'style/icon', 'w.png')))

    # Конструктор: компоненты виджета
    def _init_widget(self):
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)
        # Дисплей
        self.display = WCDisplay(self)
        # Строка ввода
        self.cmd_line = WCCommandLine(self)
        # Расскладка
        self.flag = WCFlagUserKeyboard()
        # Раскидываем по слоям
        vbox.addWidget(self.display)
        hbox.addWidget(self.cmd_line)
        hbox.addWidget(self.flag)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    # Конструктор: слушатели
    def _init_connect(self):
        self.lang_change.connect(self.lang_flag_update)

    # Метод: добавляет текст на экран
    def add_message(self, text):
        self.display.append(text)

    # Метод: очищает экран
    def clear_display(self):
        self.display.clear()

    # Метод: парсит команду
    def parse_command(self):
        text = self.cmd_line.text().strip()
        self.cmd_line.save_command(text)
        cmd_list = text.split(' ')
        self.cmd_line.clear()
        return cmd_list

    # Обработчик: смена раскладки клавиатуры
    def lang_flag_update(self):
        lang = win32api.GetKeyboardLayout()
        if lang == 67699721:
            self.flag.setText('RU')

        if lang == 68748313:
            self.flag.setText('EN')

    # Обработчик: нажатие клавиш
    def keyPressEvent(self, event):
        super(WCConsole, self).keyPressEvent(event)

        if event.modifiers() in [Qt.ShiftModifier | Qt.AltModifier, Qt.ShiftModifier | Qt.ControlModifier]:
            self.lang_change.emit()

        if self.focusWidget() == self.cmd_line and (event.key() in [16777220, 16777221]):
            command = self.parse_command()
            self.add_message(str(command))

        QWidget.keyPressEvent(self, event)
