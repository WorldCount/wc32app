#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Виджеты
"""

import win32api
from PyQt5.QtWidgets import (QWidget, QProgressBar, QLabel, QStyleOption, QStyle, QStatusBar, QMenuBar, QMenu, QAction,
                             QToolBar, QLCDNumber, QTabWidget)
from PyQt5.QtGui import (QPainter, QPen)
from PyQt5.QtCore import (Qt, QTimer)


__date__ = "14.04.2016"
__author__ = "WorldCount"
__email__ = "world.count@yandex.ru"
__copyright__ = "Copyright 2016, Scr1pt1k.Ru"
__python_version__ = ""


# Класс: надпись
class WCLabel(QLabel):

    """
    Класс надписи на PyQt5
    @author WorldCount
    @version 3
    @date 2016/04/15
    """

    # Конструктор
    def __init__(self, *args):
        super(WCLabel, self).__init__(*args)


# Класс: надпись
class WCClearLabel(QLabel):
    """
    Класс надписи на PyQt5
    @author WorldCount
    @version 3
    @date 2016/07/07
    """

    # Конструктор
    def __init__(self, *args):
        super(WCClearLabel, self).__init__(*args)


# Класс: флаг с раскладкой клавиатуры
class WCFlagUserKeyboard(QLabel):

    """
    Класс флага с раскладкой клавиатуры на PyQt5
    @author WorldCount
    @version 3
    @date 2016/04/15
    """

    # Конструктор
    def __init__(self, *args):
        super(WCFlagUserKeyboard, self).__init__(*args)
        self.lang = win32api.GetKeyboardLayout()
        # Инициализация
        self._init_ui()

    # Конструктор: настройки виджета
    def _init_ui(self):
        self.setFixedSize(32, 32)
        self.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.setText(self.get_flag())

    # Метод: обновляет флаг
    def update_flag(self):
        self.setText(self.get_flag())

    # Метод: возвращает флаг
    def get_flag(self):
        flag = 'XX'
        if self.lang == 67699721:
            flag = 'EN'
        elif self.lang == 68748313:
            flag = 'RU'
        return flag


# Класс: пример шрифта
class WCFontExample(QWidget):

    """
    Класс примера шрифта на PyQt5
    @author WorldCount
    @version 3
    @date 2016/04/14
    """

    # Конструктор
    def __init__(self, parent=None):
        super(WCFontExample, self).__init__(parent)
        self._parent = parent
        self._text = 'AaZz АаЯя'
        self._font = self.font()

    # Метод: меняет шрифт
    def chahge_font(self, font):
        if font:
            self._font = font
            self.repaint()

    # Метод: выполняет отрисовку
    def draw(self, event, painter):
        pen = QPen(self.palette().color(4), 1, Qt.DashLine)
        fon = self.palette().color(2)
        color = self.palette().color(8)
        painter.setPen(pen)
        painter.setBrush(fon)
        painter.drawRect(0, 0, self.width() - 1, self.height() - 1)
        painter.setPen(color)
        painter.setFont(self._font)
        painter.drawText(event.rect(), Qt.AlignCenter, self._text)

    # Обработчик: отрисовывает виджет
    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.draw(event, painter)
        painter.end()


# Класс: пустой виджет
class WCWidget(QWidget):

    """
    Класс пустого виджета на PyQt5
    @author WorldCount
    @version 3
    @date 2016/07/07
    """

    # Конструктор
    def __init__(self, parent):
        super(WCWidget, self).__init__(parent)

    # Обработчик: отрисовывает виджет
    def paintEvent(self, event):
        opt = QStyleOption(QStyleOption.Version)
        opt.initFrom(self)
        painter = QPainter()
        painter.begin(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)


# Класс: прогрессбар
class WCProgressBar(QProgressBar):

    """
    Класс прогрессбара на PyQt5
    @author WorldCount
    @version 3
    @date 2016/04/14
    """

    # Конструктор
    def __init__(self, parent=None, total=100, text_visible=True):
        super(WCProgressBar, self).__init__(parent)
        self._parent = parent
        self._total = total
        self._text_visible = text_visible
        self._flag = False
        self._half = 0
        self._active_half = False
        self._style = self.styleSheet()
        # Инициализация
        self._init_ui()
        self._init_widget()
        self._init_connect()

    # Конструктор: настройки виджета
    def _init_ui(self):
        self.setMinimum(0)
        self.set_maximum(self._total)
        self.setAlignment(Qt.AlignCenter)
        self.setTextVisible(self._text_visible)

    # Конструктор: компоненты виджета
    def _init_widget(self):
        self._flag = True
        self._timer = QTimer()

    # Конструктор: слушатели
    def _init_connect(self):
        self._timer.timeout.connect(self._progress_run)

    # Метод: устанавливает максимальное значение
    def set_maximum(self, value):
        if type(value) == int:
            self.setMaximum(value)
            self._half = value / 2

    # Метод: перезагружает стили статуса
    def reload_style(self):
        self.style().unpolish(self)
        self.style().polish(self)

    # Метод: запускает бесконечный прогресс
    def run(self):
        self._timer.start(50)

    # Метод: останавливает бесконечный прогресс
    def stop(self):
        self._timer.stop()
        self.setValue(self.maximum())
        self.setInvertedAppearance(False)
        self._flag = True

    # Метод: устанавливает значение
    def set_value(self, value):
        if type(value) == int:
            max_value = self.maximum()

            if not self._active_half and value >= self._half:
                self.setProperty('half', True)
                self.reload_style()
                self._active_half = True

            if value >= max_value:
                self.setProperty('half', False)
                self.reload_style()
                self._active_half = False

            self.setValue(value)

    # Обработчик: работа прогресса
    def _progress_run(self):
        current_value = self.value()
        max_value = self.maximum()

        if current_value == max_value:
            if self._flag:
                self.setInvertedAppearance(True)
            else:
                self.setInvertedAppearance(False)

            self._flag = not self._flag
            current_value = 0

        if current_value < max_value:
            self.set_value(current_value + 1)


# Класс: Статусбар
class WCStatusBar(QStatusBar):

    """
    Класс статусбара на PyQt5
    @author WorldCount
    @version 3
    @date 2016/10/22
    """

    def __init__(self, *args):
        super(WCStatusBar, self).__init__(*args)


# Класс: Менюбар
class WCMenuBar(QMenuBar):

    """
    Класс менюбара на PyQt5
    @author WorldCount
    @version 3
    @date 2016/10/22
    """

    def __init__(self, *args):
        super(WCMenuBar, self).__init__(*args)


# Класс: Меню
class WCMenu(QMenu):

    """
    Класс меню на PyQt5
    @author WorldCount
    @version 3
    @date 2016/10/22
    """

    def __init__(self, *args):
        super(WCMenu, self).__init__(*args)


# Класс: Экшен
class WCAction(QAction):

    """
    Класс экшена на PyQt5
    @author WorldCount
    @version 3
    @date 2016/10/27
    """

    def __init__(self, *args):
        super(WCAction, self).__init__(*args)


# Класс: Тулбар
class WCToolbar(QToolBar):

    """
    Класс тулбара на PyQt5
    @author WorldCount
    @version 3
    @date 2016/10/27
    """

    def __init__(self, *args):
        super(WCToolbar, self).__init__(*args)


# Класс: Цифровой дисплей
class WCLCDNumber(QLCDNumber):

    """
    Класс цифрового дисплея на PyQt5
    @author WorldCount
    @version 3
    @date 2016/10/27
    """

    def __init__(self, *args):
        super(WCLCDNumber, self).__init__(*args)


# Класс: Бар с вкладками
class WCTabWidget(QTabWidget):

    """
    Класс бара с вкладками на PyQt5
    @author WorldCount
    @version 3
    @date 2016/10/27
    """

    def __init__(self, *args):
        super(WCTabWidget, self).__init__(*args)
