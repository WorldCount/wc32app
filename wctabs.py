#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget


__author__ = 'WorldCount'


"""
Вкладки
"""


# Класс: Пустая вкладка
class WCClearTab(QWidget):

    """
    Пустая вкладка
    @author WorldCount
    @version 3
    @date 2016/10/27
    """

    def __init__(self, pos=None, parent=None):
        super(WCClearTab, self).__init__(parent)
        self._p = parent
        self._pos = pos
        self.name = 'WCClearTab'
        self.toolbar_list = []

        self._init_ui()

    # Инициализация: Настройка вкладки
    def _init_ui(self):
        pass

    # Метод: Возвращает позицию окна
    def get_pos(self):
        return self._pos
