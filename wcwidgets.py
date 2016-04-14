#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Виджеты
"""

__date__ = "14.04.2016"
__author__ = "WorldCount"
__email__ = "world.count@yandex.ru"
__copyright__ = "Copyright 2016, Scr1pt1k.Ru"
__python_version__ = ""


from PyQt5.QtWidgets import (QWidget, QProgressBar)
from PyQt5.QtGui import (QPainter, QPen, QColor, QPalette)
from PyQt5.QtCore import (Qt, QTimer)


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
        self._style = self.styleSheet()
        # Инициализация
        self._init_ui()
        self._init_widget()
        self._init_connect()

    # Конструктор: настройки виджета
    def _init_ui(self):
        self.setMinimum(1)
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
        self._timer.start(10)

    # Метод: останавливает бесконечный прогресс
    def stop(self):
        self._timer.stop()
        self.setValue(self.maximum())
        self.setInvertedAppearance(False)
        self._flag = True

    # Обработчик: работа прогресса
    def _progress_run(self):
        current_value = self.value()
        max_value = self.maximum()

        if current_value == self._half:
            self.setProperty('half', True)
            self.reload_style()

        if current_value == max_value:
            self.setProperty('half', False)
            self.reload_style()

            if self._flag:
                self.setInvertedAppearance(True)
            else:
                self.setInvertedAppearance(False)

            self._flag = not self._flag
            current_value = 0

        if current_value < max_value:
            self.setValue(current_value + 1)
