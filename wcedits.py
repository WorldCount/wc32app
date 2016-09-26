#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Виджеты ввода
"""

from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import (Qt, QEvent, pyqtSignal)


__date__ = "14.04.2016"
__author__ = "WorldCount"
__email__ = "world.count@yandex.ru"
__copyright__ = "Copyright 2016, Scr1pt1k.Ru"
__python_version__ = ""


# Класс: строка ввода
class WCLineEdit(QLineEdit):

    """
    Класс строки ввода на PyQt5
    @author WorldCount
    @version 3
    @date 2016/04/07
    """

    # Сигнал: нажатие на [TAB]
    tab_pressed = pyqtSignal()

    # Конструктор
    def __init__(self, *args):
        super(WCLineEdit, self).__init__(*args)

    # Обработчик: событие
    def event(self, event):
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.tab_pressed.emit()
            self.focusNextChild()
            return True
        return QLineEdit.event(self, event)
