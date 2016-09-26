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
from PyQt5.QtWidgets import (QWidget, QTextEdit, QLineEdit, QVBoxLayout, QHBoxLayout, QCompleter, QLabel)
from PyQt5.QtGui import (QIcon, QTextCursor, QColor)
from PyQt5.QtCore import (Qt, pyqtSignal, QEvent, QAbstractItemModel, QModelIndex)
from .wcwidgets import (WCFlagUserKeyboard, WCWidget, WCClearLabel)
from .wcbuttons import WCPushButton
from .wcedits import WCLineEdit
from .wcextends import (WCClearExtend, SystemExtend)
from .wccommands import (WCClearCommand, PrintCommand, DateTimeCommand, HostCommand)
import win32api


# Класс: часть команды
class CommandItem(object):

    def __init__(self, data, parent=None):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []

    def appendChild(self, item):
        self.childItems.append(item)

    def child(self, row):
        return self.childItems[row]

    def childCount(self):
        return len(self.childItems)

    def columnCount(self):
        return len(self.itemData)

    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None

    def parent(self):
        return self.parentItem

    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)

        return 0

    def __repr__(self):
        return 'CommandItem(%s)' % self.itemData


# Класс: модель команд
class CommandModel(QAbstractItemModel):

    def __init__(self, data, parent=None):
        super(CommandModel, self).__init__(parent)
        self.rootItem = CommandItem(("Command",))
        self.setupModelData(data.split('\n'), self.rootItem)

    def columnCount(self, parent=None, *args, **kwargs):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.rootItem.columnCount()

    def data(self, index, role=None):
        if not index.isValid():
            return None

        if role == Qt.EditRole:
            return self.rootItem.data(0)

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()
        return item.data(index.column())

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def headerData(self, section, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)

        return None

    def index(self, row, column, parent=None, *args, **kwargs):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()

    def parent(self, index=None):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self.rootItem:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def rowCount(self, parent=None, *args, **kwargs):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    def setupModelData(self, lines, parent):
        parents = [parent]
        indentations = [0]

        number = 0

        while number < len(lines):
            position = 0
            while position < len(lines[number]):
                if lines[number][position] != ' ':
                    break
                position += 1

            lineData = lines[number][position:].strip()

            if lineData:
                # Read the column data from the rest of the line.
                columnData = [s for s in lineData.split('+') if s]

                if position > indentations[-1]:
                    # The last child of the current parent is now the new
                    # parent unless the current parent has no children.

                    if parents[-1].childCount() > 0:
                        parents.append(parents[-1].child(parents[-1].childCount() - 1))
                        indentations.append(position)

                else:
                    while position < indentations[-1] and len(parents) > 0:
                        parents.pop()
                        indentations.pop()

                # Append a new item to the current parent's list of children.
                newtreeitem = CommandItem(columnData, parents[-1])
                parents[-1].appendChild(newtreeitem)

            number += 1


# Класс: автозавершение команд
class WCCommandCompleter(QCompleter):

    def splitPath(self, path):
        return path.split(' ')

    def pathFromIndex(self, index):
        result = []
        while index.isValid():
            result = [self.model().data(index, Qt.DisplayRole)] + result
            index = index.parent()
        r = ' '.join(result)
        return r


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
        # Список введенных команд
        self._save_command = []
        self._current_command_num = 0
        # Список команд
        self._command = """
cls
debug
command
    команда
exit
help
    команда
history
    clear
"""

        # Инициализация
        self._init_ui()
        self._init_connect()

    # Конструктор: настройки виджета
    def _init_ui(self):
        self.setFixedHeight(32)
        # Создаем комплитер
        self._completer = WCCommandCompleter()
        self._completer.setCaseSensitivity(Qt.CaseInsensitive)
        self._completer.setCompletionRole(Qt.DisplayRole)
        self._completer.setCompletionColumn(0)
        self.update_model()
        self.setCompleter(self._completer)

    # Конструктор: слушатели
    def _init_connect(self):
        pass

    # Метод: создает список автозавершения
    def update_model(self):
        model = CommandModel(self._command)
        self._completer.setModel(model)

    # Метод: возвращает количество слов
    def get_world_count(self):
        return self._word_count

    # Метод: добавляет команду
    def add_command(self, command):
        if command not in self._command:
            new_command = "%s %s" % (self._command, command)
            self._command = new_command
            self.update_model()

    # Метод: удаляет команду
    def remove_command(self, command):
        if command in self._command:
            new_command = self._command.replace(command, "")
            self._command = new_command
            self.update_model()

    # Метод: сохраняет введеную команду
    def save_command(self, command):
        if command not in self._save_command:
            self._save_command.append(command)
            self._current_command_num = len(self._save_command) - 1

    # Метод: очищает сохраненные команды
    def clear_history(self):
        self._save_command = []
        self._current_command_num = 0

    # Метод: возвращает список сохраненных команд
    def get_history(self):
        return self._save_command

    # Метод: обновляет данные по словам
    def update_word(self):
        all_text = self.text().split()
        self._word_count = len(all_text)
        self.change_word_count.emit(self.get_world_count())

    # Метод: очищает введенные данные
    def clear(self):
        super(WCCommandLine, self).clear()
        self.setCursorPosition(0)
        self._word_count = 0
        self.update_word()

    # Обработчик: завершение команды
    def complete(self):
        index = self._completer.currentIndex()
        self._completer.popup().setCurrentIndex(index)
        start = self._completer.currentRow()
        if not  self._completer.setCurrentRow(start + 1):
            self._completer.setCurrentRow(0)

    # Обработчик: нажатие клавиш
    def keyPressEvent(self, event):
        super(WCCommandLine, self).keyPressEvent(event)

        # [Space], [BackSpace], [Delete]
        if event.key() in [Qt.Key_Space, Qt.Key_Backspace, Qt.Key_Delete]:
            self.update_word()

        # [Ctrl] + [Space]
        if event.modifiers() and Qt.ControlModifier:
            if event.key() == Qt.Key_Space:
                self._completer.complete()

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
            self.complete()
            self._completer.popup().hide()
            return True

        return super(WCCommandLine, self).event(event)


# Класс: панель дисплея
class WCDisplayPanel(WCWidget):

    """
    Класс панели дисплея консоли
    @author WorldCount
    @version 4
    @date 2016/07/07
    """

    # Конструктор
    def __init__(self, parent):
        super(WCDisplayPanel, self).__init__(parent)
        self._parent = parent
        self._path = os.path.dirname(__file__)
        # Связь с дисплеем
        self._display = None
        # Найденные элементы через поиск
        self._search_data = []
        # Инициализация
        self._init_ui()
        self._init_widget()
        self._init_connect()

    # Конструктор: компоненты виджета
    def _init_ui(self):
        self.setFixedHeight(40)

    # Конструктор: компоненты виджета
    def _init_widget(self):
        hbox = QHBoxLayout()
        hbox.setContentsMargins(5, 0, 0, 0)

        self.search = WCLineEdit(self)
        self.search.setPlaceholderText('Поиск...')
        self.search.setFixedWidth(140)
        self.search.setFixedHeight(32)
        self.btn_search = WCPushButton('Искать')
        self.btn_search.setFixedHeight(32)
        hbox.addWidget(self.search)
        hbox.addWidget(self.btn_search)
        hbox.addStretch()
        self.setLayout(hbox)

        # Переопределяем обработчки клика по полю
        self.search.mousePressEvent = lambda x: self.search.selectAll()

    # Конструктор: слушатели
    def _init_connect(self):
        self.btn_search.clicked.connect(self.run_search)

    # Метод: связывает панель с дисплеем
    def binding(self, display):
        if isinstance(display, WCDisplay):
            self._display = display

    # Метод: отвязывает дисплей от панели
    def unbinding(self):
        self._display = None

    # Метод: поиск по тексту
    def run_search(self):
        if self._display == None:
            return

        self._max_data = None
        self._current_select = 0
        self._first_select = True

        text = self.search.text()
        self._search_data = self._display.search(text)
        data_size = len(self._search_data)

        self._display.set_select_all(self._search_data)

    # Обработчик: нажатие клавиш
    def keyPressEvent(self, event):
        if self.focusWidget() == self.search and (event.key() in [16777220, 16777221]):
            self.run_search()

        QWidget.keyPressEvent(self, event)


# Класс: дисплей
class WCDisplay(QTextEdit):

    """
    Класс дисплея консоли
    @author WorldCount
    @version 4
    @date 2016/04/15
    """

    # Сигнал: изменение шрифта
    font_change = pyqtSignal(int)

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
        # Шрифт по умолчанию
        self._default_font_size = None
        self._styles = {}
        self._open_tags = {}
        self._close_tags = {}
        self._load_extends = {}
        # Инициализация
        self._init_ui()

    # Конструктор: компоненты виджета
    def _init_ui(self):
        self.setReadOnly(True)
        system_extend = SystemExtend()
        self.add_extend(system_extend)

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

    # Метод: возвращает размер шрифта
    def get_font_size(self):
        return self.document().defaultFont().pixelSize()

    # Метод: устанавливает размер шрифта
    def set_font_size(self, size):
        font = self.document().defaultFont()
        font.setPixelSize(size)
        self.document().setDefaultFont(font)
        self.font_change.emit(size)

    # Метод: сбрасывает шрифт к начальным значениям
    def reset_font(self):
        if not self._default_font_size is None:
            self.set_font_size(self._default_font_size)

    # Метод: устанавливает значение начального размера шрифта
    def set_default_font_value(self, size):
        self._default_font_size = size

    # Метод: увеличивает размер шрифта
    def zoomIn(self, int_range=1):
        size = self.get_font_size()

        if self._default_font_size is None:
            self.set_default_font_value(size)

        if size < 100:
            self.set_font_size(size + 1)

    # Метод: уменьшает размер шрифта
    def zoomOut(self, int_range=1):
        size = self.get_font_size()

        if self._default_font_size is None:
            self.set_default_font_value(size)

        if size > 1:
            self.set_font_size(size - 1)

    # Метод: ишет данные в тексте
    def search(self, text):
        self.textCursor().clearSelection()
        self.moveCursor(QTextCursor.Start)
        data = []
        color = QColor('#272b30').lighter(130)
        font_color = QColor('#ffffff')

        while (self.find(text)):
            section = QTextEdit.ExtraSelection()
            section.format.setBackground(color)
            section.format.setForeground(font_color)
            section.cursor = self.textCursor()
            data.append(section)
        self.clear_select()
        return data

    # Метод: выделяет найденные данные в тексте
    def set_select_all(self, list_select):
        self.setExtraSelections(list_select)

    # Метод: выделяет текст
    def set_select(self, select):
        self.setTextCursor(select.cursor)

    # Метод: очищает выделение
    def clear_select(self):
        cursor = self.textCursor()
        cursor.clearSelection()
        self.moveCursor(QTextCursor.End)

    # Метод: очищает все выделения
    def clear_all_selection(self):
        cursor = self.textCursor()
        cursor.select(QTextCursor.Document)
        section = QTextEdit.ExtraSelection()
        section.cursor = cursor
        self.setExtraSelections([section])

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

    # Обработчик: контекстное меню
    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        if not menu:
            return QTextEdit.contextMenuEvent(event)

        menu.setObjectName('menu')
        actions = menu.actions()
        for action in actions:
            action_text = action.text()

            if 'Copy' in action_text:
                action.setText('Копировать\tCtrl+C')
            elif 'Select All' in action_text:
                action.setText('Выделить все\tCtrl+A')

        menu.exec(event.globalPos())

    # Обработчик: колесико мышки
    def wheelEvent(self, event):
        if (event.modifiers() & Qt.ControlModifier):
            delta = event.angleDelta().y()
            if delta > 0:
                self.zoomIn(1)
            else:
                self.zoomOut(1)
        event.accept()


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
        # Панель для дисплея
        self.panel = WCDisplayPanel(self)
        self.panel.binding(self.display)
        # Строка ввода
        self.cmd_line = WCCommandLine(self)
        # Расскладка
        self.flag = WCFlagUserKeyboard()
        # Раскидываем по слоям
        vbox.addWidget(self.panel)
        vbox.addWidget(self.display)
        hbox.addWidget(self.cmd_line)
        hbox.addWidget(self.flag)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.cmd_line.setFocus()

    # Конструктор: команды
    def _init_command(self):
        cmd_print = PrintCommand()
        cmd_date = DateTimeCommand()
        cmd_host = HostCommand()

        self.add_command(cmd_print)
        self.add_command(cmd_date)
        self.add_command(cmd_host)
        #self.remove_command(cmd_print)

    # Конструктор: слушатели
    def _init_connect(self):
        self.lang_change.connect(self.lang_flag_update)

    # Метод: добавляет текст на экран
    def add_message(self, message, type_message=None):
        self.display.add_message(message, type_message)

    # Метод: добавляет текст на экран c меткой времени
    def add_message_with_time(self, message, type_message=None):
        self.display.add_message_with_time(message, type_message)

    # Метод: очищает экран
    def clear_display(self):
        self.display.clear()

    # Метод: парсит команду
    def parse_command(self, echo=True):
        text = self.cmd_line.text().strip().lower()

        if echo:
            self.add_message_with_time('[system]%s ~>[/system]' % text)

        self.cmd_line.save_command(text)
        cmd_list = text.split()
        self.cmd_line.clear()
        return cmd_list

    # Метод: выводит историю команд
    def get_history(self):
        history = self.cmd_line.get_history()
        for num, cmd in enumerate(history):
            text = '[error]%d.[/error] [success]%s[/success]' % (num + 1, cmd)
            self.add_message(text)

    # Метод: очищает историю команд
    def clear_history(self):
        self.cmd_line.clear_history()
        self.add_message('[success]История команд очищена![/success]')

    # Метод: выводит список команд
    def get_all_command(self, filter_str=None):
        command_dict = {'cls': 'Очищает экран', 'debug': 'Выводит отладочную информацию',
                        'exit': 'Выходит из приложения', 'help': 'Выводит справку по команде',
                        'command': 'Выводит список доступных команд',
                        'history': 'Управление списком сохраненных команд'}

        for command in self._extends_command:
            cmd_name = command
            cmd_desc = self._extends_command[command].desc

            if cmd_name not in command_dict.keys():
                command_dict.update({cmd_name: cmd_desc})

        if filter_str:
            keys = sorted([key for key in command_dict.keys() if key.startswith(filter_str)])
        else:
            keys = sorted(list(command_dict.keys()))

        if len(keys) > 0:
            for key in keys:
                text = '[b][success]%s[/success][/b] - %s' % (key, command_dict[key])
                self.add_message(text)
        else:
            self.add_message('[error]Команды не найдены![/error]')

    # Метод: выводит справку по командам
    def help(self, *args):
        if args[0] == 'help':
            self.add_message('Для вывода справки по команде введите:', self.display._INFO)
            self.add_message('[b]help [warn][команда][/warn][/b]', self.display._SUCCESS)
            self.display.add_clear_message()
            self.add_message('Для получения списка доступных команд введите:', self.display._INFO)
            self.add_message('[b]command[/b]', self.display._SUCCESS)
        else:
            cmd_name = args[0][0]

            if cmd_name == 'command':
                self.add_message('[success][b]command[/b][/success] - выводит список доступных команд.')
                _text = '[b][success][b]command[/b][/success] [warn][текст][/warn][/b] ' \
                        '- выводит список команд начинающихся с текста.'
                self.add_message(_text)
            elif cmd_name == 'exit':
                self.add_message('[success][b]exit[/b][/success] - выход из приложения.')
            elif cmd_name == 'cls':
                self.add_message('[success][b]cls[/b][/success] - очищает экран.')
            elif cmd_name == 'debug':
                self.add_message('[success][b]debug[/b][/success] - [error]команда только для отладки.[/error]')
            elif cmd_name == 'help':
                self.add_message('[success][b]help[/b][/success] - выводит справку.')
                _text = '[b][success][b]help[/b][/success] [warn][команда][/warn][/b] - выводит справку по команде.'
                self.add_message(_text)
            elif cmd_name == 'history':
                self.add_message('[success][b]history[/b][/success] - выводит список сохраненных команд.')
                _text = '[b][success][b]history clear[/b][/success][/b] - очищает список сохраненных команд.'
                self.add_message(_text)
            elif cmd_name in self._command_list:
                for help_line in self._extends_command[cmd_name].help:
                    self.add_message(help_line)
            else:
                self.add_message('Команда "%s" не найдена!' % cmd_name, self.display._ERROR)

    # Метод: запускает команды
    def run_command(self, command):
        len_cmd = len(command)
        if len_cmd > 0:
            cmd_name = command[0]
            args = command[1:]

            # очистка экрана
            if cmd_name == 'cls':
                self.clear_display()
            # выход из приложения
            elif cmd_name == 'exit':
                if self._parent:
                    self._parent.close()
                else:
                    self.close()
            # отладка
            elif cmd_name == 'debug':
                self._debug()
            elif cmd_name == 'command':
                if len_cmd > 1:
                    self.get_all_command(args[0])
                else:
                    self.get_all_command()
            # помощь по команде
            elif cmd_name == 'help':
                if len_cmd > 1:
                    self.help(args)
                else:
                    self.help(cmd_name)
            # история команд
            elif cmd_name == 'history':
                if len_cmd > 1 and args[0] == 'clear':
                    self.clear_history()
                else:
                    self.get_history()
            # конманды добавленные расширением
            elif cmd_name in self._command_list:
                cmd_object = self._extends_command[cmd_name]
                res = cmd_object.run(args)
                if type(res) in [str, int]:
                    self.add_message(res)
                else:
                    for line in res:
                        self.add_message(line)
            else:
                self.add_message("Ошибка! Неизвестная команда: '%s'" % cmd_name, self.display._ERROR)

            if cmd_name != 'cls':
                self.display.add_clear_message()
        else:
            return

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

    # Метод: служит для отладки
    def debug(self):
        pass

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
            commands = self.parse_command()
            self.run_command(commands)

        QWidget.keyPressEvent(self, event)
