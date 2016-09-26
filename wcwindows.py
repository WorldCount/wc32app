#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Окна приложения
"""

import os
from PyQt5.QtWidgets import (QMainWindow, QDesktopWidget)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (Qt, QSettings)


__date__ = "07.04.2016"
__author__ = "WorldCount"
__email__ = "world.count@yandex.ru"
__copyright__ = "Copyright 2016, Scr1pt1k.Ru"
__python_version__ = "3"


# Класс: главное окно
class WCWindow(QMainWindow):

    """
    Класс главного окна на PyQt5
    @author WorldCount
    @version 3
    @date 2016/04/07
    """

    # Конструктор
    def __init__(self, parent=None, config_name=None, config_dir=None):
        super(WCWindow, self).__init__(parent)
        self._parent = parent
        self._path = os.path.dirname(__file__)
        self._config_name = config_name
        self._config_dir = config_dir
        self._name = self.__class__.__name__

        # Минимальный размер окна
        self.setMinimumSize(400, 200)

        # Пути к конфигурации
        if not self._config_name:
            self._config_name = '%s.ini' % self._name.lower()

        if not self._config_dir:
            self._config_dir = self._path

        self._config_path = os.path.join(self._config_dir, self._config_name)

        # Настройки окна
        self.settings = QSettings(self._config_path, QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)

        # Инициализируем настройки окна
        self._init_ui()

    # Инициализация: настройки окна
    def _init_ui(self):
        self.setWindowTitle(self._name)
        self.setWindowIcon(QIcon(os.path.join(self._path, 'style/icon', 'w.png')))

        # Если есть сохраненые настройки окна
        if os.path.exists(self._config_path):
            pos = self.load_pos()

            # Если данные загрузились
            if pos:
                screen = QDesktopWidget().screenGeometry()

                if pos.width() == screen.width():
                    self.setWindowState(Qt.WindowMaximized)
                else:
                    self.setGeometry(pos)

    # Метод: сохраняет позицию окна
    def save_pos(self):
        self.settings.setValue('pos/geometry', self.geometry())

    # Метод: загружает позицию окна
    def load_pos(self):
        return self.settings.value('pos/geometry')

    # Обработчик: евент закрытия окна
    def closeEvent(self, event):
        self.hide()
        self.save_pos()
        event.accept()
