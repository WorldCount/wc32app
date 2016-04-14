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


from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import (QPainter, QPen)
from PyQt5.QtCore import Qt


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
