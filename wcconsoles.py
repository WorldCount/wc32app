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
import datetime
from PyQt5.QtWidgets import (QWidget, QTextEdit, QLineEdit, QVBoxLayout, QHBoxLayout, QCompleter)
from PyQt5.QtGui import (QIcon)
from PyQt5.QtCore import (Qt, pyqtSignal, QStringListModel, QEvent, QRect)
from .wcwidgets import WCFlagUserKeyboard
from .wcextends import (WCClearExtend, SystemExtend)
from .wccommands import (WCClearCommand, PrintCommand)
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
        self._command_list = [['cls'], ['debug', 'info'], ['command'], ['exit']]
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
        self._completer.setCaseSensitivity(Qt.CaseInsensitive)
        self._completer.setCompletionMode(QCompleter.PopupCompletion)
        self.update_completer()

    # Конструктор: слушатели
    def _init_connect(self):
        self._completer.activated.connect(self._complete_text)
        self.textChanged.connect(self._text_change)
        self.text_changed.connect(self._completer.update)

    # Метод: возвращает список команд
    def get_command(self):
        res = []
        for cmd in self._current_command_list:
            res.append(cmd[0])
        return res

    # Метод: возвращает количество слов
    def get_world_count(self):
        return self._word_count

    # Метод: обновляет данные комплитера
    def update_completer(self):
        self._completer.update_model(self._current_complete)

    # Метод: добавляет команду
    def add_command(self, command):
        if command not in self._command_list:
            self._command_list.append(command)
            self.update_word()

    # Метод: удаляет команду
    def remove_command(self, command):
        if command in self._command_list:
            self._command_list.remove(command)
            self.update_word()

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
        if text == "":
            self.update_word()
        try:
            self._prefix = text.split()[-1].strip()
        except IndexError:
            self._prefix = ''
        self.text_changed.emit(self._prefix)

    # Обработчик: нажатие клавиш
    def keyPressEvent(self, event):
        #super(WCCommandLine, self).keyPressEvent(event)

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

        return super(WCCommandLine, self).keyPressEvent(event)

    # Обработчик: события
    def event(self, event):
        # Нажатие [TAB]
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            text = self._completer.currentCompletion()
            if text in self._current_complete:
                self._complete_text(text)
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

    # Виды сообщений
    _ERROR = 1
    _SUCCESS = 2
    _WARN = 3
    _INFO = 4
    _SYSTEM = 5

    # Конструктор
    def __init__(self, parent=None):
        super(WCDisplay, self).__init__(parent)
        self._parent = parent
        self._path = os.path.dirname(__file__)
        self._styles = {}
        self._open_tags = {}
        self._close_tags = {}
        self._load_extends = {}
        # Инициализация
        self._init_ui()

    # Конструктор: компоненты виджета
    def _init_ui(self):
        self.setReadOnly(True)
        sys_extend = SystemExtend()
        self.add_extend(sys_extend)

    # Метод: добавляет стили к общим
    def add_styles(self, styles):
        return self._update_data_to_dict(styles, self._styles)

    # Метод: удаляет стили из общих
    def remove_styles(self, styles):
        return self._remove_data_of_dict(styles, self._styles)

    # Метод: добавляет открывающие теги
    def add_open_tags(self, tags):
        return self._update_data_to_dict(tags, self._open_tags)

    # Метод: удаляет открывающие теги
    def remove_open_tags(self, tags):
        return self._remove_data_of_dict(tags, self._open_tags)

    # Метод: добавляет закрывающие теги
    def add_close_tags(self, tags):
        return self._update_data_to_dict(tags, self._close_tags)

    # Метод: удаляет закрывающие теги
    def remove_close_tags(self, tags):
        return self._remove_data_of_dict(tags, self._close_tags)

    # Метод: добавляет расширение
    def add_extend(self, extend_object):
        if extend_object in self._load_extends or not isinstance(extend_object, WCClearExtend):
            return False
        else:
            if len(extend_object.name) > 0:
                # добавляем расширение к загруженным
                added_extend = {extend_object.name: extend_object}
                self._load_extends.update(added_extend)
                # добавляем стили и теги
                self.add_styles(extend_object.styles)
                self.add_open_tags(extend_object.open_tags)
                self.add_close_tags(extend_object.close_tags)
                return True
            return False

    # Метод: удаляет расширение
    def remove_extend(self, extend_object):
        if isinstance(extend_object, WCClearExtend) and extend_object.name in self._load_extends.keys():
            # удаляем расширение из загруженных
            del self._load_extends[extend_object.name]
            # удаляем стили и теги
            self.remove_styles(extend_object.styles)
            self.remove_open_tags(extend_object.open_tags)
            self.remove_close_tags(extend_object.close_tags)
            return True
        return False

    # Метод: добавляет сообщение на дисплей
    def add_message(self, message, message_type=None):
        format_message = self._format_messages(message, message_type)
        parse_message = self._parse_text(format_message)
        self.append(parse_message)

    # Метод: добавляет сообщение на дисплей с меткой времени
    def add_message_with_time(self, message, message_type=None):
        now_date = datetime.datetime.now()
        format_message = self._format_messages(message, message_type)
        parse_message = self._parse_text(format_message)
        sys_message = self._format_messages('[%s]:' % now_date.strftime('%d.%m.%Y %H:%M:%S'), self._SYSTEM)
        self.append('%s %s' % (sys_message, parse_message))

    # Метод: добавляет на дисплей пустую строку
    def add_clear_message(self):
        self.append('')

    # Функция: форматирует сообщение
    def _format_messages(self, message, message_type=None):
        if message_type == self._ERROR:
            color = self._styles['error']
        elif message_type == self._INFO:
            color = self._styles['info']
        elif message_type == self._WARN:
            color = self._styles['warn']
        elif message_type == self._SUCCESS:
            color = self._styles['success']
        elif message_type == self._SYSTEM:
            color = self._styles['system']
        else:
            color = self._styles['color']
        return '<span style = "color:%s;">%s</span>' % (color, message)

    # Функция: парсит и заменяет теги
    def _parse_text(self, text):
        result_text = text
        # открытые теги
        for open_tag in self._open_tags.keys():
            format_text = result_text.replace(open_tag, self._open_tags[open_tag])
            if format_text:
                result_text = format_text
        # закрытые теги
        for close_tag in self._close_tags.keys():
            format_text = result_text.replace(close_tag, self._close_tags[close_tag])
            if format_text:
                result_text = format_text
        return result_text

    # Функция: Обновляет данные в словаре
    def _update_data_to_dict(self, update_data, dict_link):
        if len(update_data) > 0 and type(update_data) == dict:
            dict_link.update(update_data)
            return True
        return False

    # Функция: удаляет данные из словоря
    def _remove_data_of_dict(self, remove_data, dict_link):
        if len(remove_data) > 0 and type(remove_data) == dict:
            _keys = dict_link.keys()
            for del_key in remove_data.keys():
                if del_key in _keys:
                    del dict_link[del_key]
            return True
        return False


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
        # Список доступных команд
        self._command_list = []
        # Расширение команд
        self._extends_command = {}
        # Инициализация
        self._init_ui()
        self._init_widget()
        self._init_command()
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

    # Конструктор: команды
    def _init_command(self):
        cmd_print = PrintCommand()
        self.add_command(cmd_print)
        #self.remove_command(cmd_print)
        print(self.cmd_line.get_command())

    # Конструктор: слушатели
    def _init_connect(self):
        self.lang_change.connect(self.lang_flag_update)

    # Метод: добавляет текст на экран
    def add_message(self, message, type_message=None):
        self.display.add_message(message, type_message)

    # Метод: очищает экран
    def clear_display(self):
        self.display.clear()

    # Метод: парсит команду
    def parse_command(self):
        text = self.cmd_line.text().strip()
        self.cmd_line.save_command(text)
        #cmd_list = text.split(' ')
        self.cmd_line.clear()
        #return cmd_list
        self.add_message(text)

    # Метод: добавляет команду
    def add_command(self, command_object):
        if isinstance(command_object, WCClearCommand):
            if command_object.name not in self._command_list:
                self._command_list.append(command_object.name)
                self.cmd_line.add_command(command_object.complete_list)
                self.display.add_extend(command_object)
                self._extends_command.update({command_object.name: command_object})
                return True
        return False

    # Метод: удаляет команду
    def remove_command(self, command_object):
        if isinstance(command_object, WCClearCommand):
            if command_object.name in self._command_list:
                self._command_list.remove(command_object.name)
                self.cmd_line.remove_command(command_object.complete_list)
                self.display.remove_extend(command_object)
                if command_object.name in self._extends_command.keys():
                    del self._extends_command[command_object.name]
                return True
        return False

    # Метод: возвращает список команд в форматированном виде
    def show_command_list(self):
        _cmd = self.cmd_line.get_command()
        sorted(_cmd)
        format_line = '[system][b]Список доступных команд:[/b][/system] [success]%s[/success]'
        res = format_line % ('[warn],[/warn] '.join(_cmd))
        return res

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
            #self.add_message(str(command))

        QWidget.keyPressEvent(self, event)
