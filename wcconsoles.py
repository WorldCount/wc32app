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
from PyQt5.QtWidgets import (QWidget, QTextEdit, QLineEdit, QVBoxLayout, QHBoxLayout, QLabel, QCompleter)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtCore import (Qt, pyqtSignal, QStringListModel)
from .wcwidgets import WCFlagUserKeyboard
import win32api


# Класс: командная строка
class WCCommandLine(QLineEdit):

    """
    Класс дисплея консоли
    @author WorldCount
    @version 4
    @date 2016/04/15
    """

    change_word_count = pyqtSignal(int)

    # Конструктор
    def __init__(self, *args):
        super(WCCommandLine, self).__init__(*args)
        # Количество слов
        self._word_count = 0
        # Последнее слово
        self._last_word = ''
        # Список команд
        self._command_list = [['cls'], ['debug', 'info'], ['command'], ['exit']]
        # Текущий список команд
        self._current_command_list = self._command_list[:]
        # Текущий список завершения
        self._current_complete = []
        # Инициализация
        self._init_ui()

    # Конструктор: настройки виджета
    def _init_ui(self):
        self.setFixedHeight(32)
        #
        self.create_complete_list()
        #
        self.model = QStringListModel()
        self._completer = QCompleter()
        self._completer.setCompletionMode(QCompleter.InlineCompletion)
        self._completer.setModel(self.model)
        self.set_data()
        #
        self.setCompleter(self._completer)

    # Метод: возвращает количество слов
    def get_world_count(self):
        return self._word_count

    #
    def set_data(self):
        print('set data:', self._current_complete)
        self.model.setStringList(self._current_complete)

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
                    if self._last_word == cmd[self._word_count]:
                        offset = cmd[self._word_count + 1]
                        if offset not in res_complete:
                            res_complete.append(offset)
                        res_cmd.append(cmd)
                except Exception:
                    continue

        self._current_command_list = res_cmd[:]
        self._current_complete = res_complete[:]

    # Обработчик: нажатие клавиш
    def keyPressEvent(self, event):
        super(WCCommandLine, self).keyPressEvent(event)

        if event.key() in [Qt.Key_Space, Qt.Key_Backspace, Qt.Key_Delete]:
            text = self.text().split()
            try:
                self._last_word = text[-1]
            except IndexError:
                self._last_word = ''
            self.create_complete_list()
            print(self._last_word, self._current_complete)
            print(self._current_command_list)
            self.set_data()
            self._word_count = len(text)
            self.change_word_count.emit(self._word_count)


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
        text = self.cmd_line.text()
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
