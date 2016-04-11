#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Приложение
"""

__date__ = "07.04.2016"
__author__ = "WorldCount"
__email__ = "world.count@yandex.ru"
__copyright__ = "Copyright 2016, Scr1pt1k.Ru"
__python_version__ = "3"


import os
from PyQt5.QtWidgets import QApplication


# Класс: чистое приложение
class WCClearApp(QApplication):

    """
    Класс чистого приложения на PyQt5
    @author WorldCount
    @version 3
    @date 2016/04/07
    """

    def __init__(self, args):
        super(WCClearApp, self).__init__(args)
        self._path = os.path.dirname(__file__)


# Класс: стилизированное приложение
class WCStyleApp(WCClearApp):

    """
    Класс стилизированного приложения на PyQt5
    @author WorldCount
    @version 3
    @date 2016/04/07
    """

    # Конструктор
    def __init__(self, args, style_path=None):
        super(WCStyleApp, self).__init__(args)
        self._style_path = style_path

        if not self._style_path:
            self._style_path = os.path.join(self._path, 'style', 'style.css')

        # Применяем стили, если они есть
        self.load_style()

    # Метод: загружает стили приложения
    def load_style(self):
        if os.path.exists(self._style_path):
            style = ''.join(open(self._style_path, 'r').readlines())
            self.setStyleSheet(style)

    # Метод: устанавливает путь к файлу стилей
    def set_style_path(self, path):
        if path:
            self._style_path = path
            return True
        return False
