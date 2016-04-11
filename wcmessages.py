#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Всплывающие сообщения
"""

__date__ = "12.04.2016"
__author__ = "WorldCount"
__email__ = "world.count@yandex.ru"
__copyright__ = "Copyright 2016, Scr1pt1k.Ru"
__python_version__ = "3"


import os
import sys
from PyQt5.QtWidgets import (QDialog, QLabel, QHBoxLayout, QVBoxLayout)
from PyQt5.QtCore import (Qt, QTimer)
from PyQt5.QtGui import (QPixmap)
from .wcbuttons import WCPushButton


# Класс: сообщение с закрытием по таймеру
class WCMessageBoxTimer(QDialog):

    """
    Класс сообщения с закрытием по таймеру на PyQt5
    @author WorldCount
    @version 3
    @date 2016/04/12
    """

    # Конструктор
    def __init__(self, message, seconds=None, parent=None):
        super(WCMessageBoxTimer, self).__init__(parent)
        self._parent = parent
        self._path = os.path.dirname(__file__)
        self._message = message
        self._seconds = seconds if seconds else 10
        # Ширина виджетов
        self._width = 298
        # Таймер
        self._timer_message = 'Окно будет автоматически закрыто через <b>%s</b> сек.'
        self._timer = QTimer()
        # Инициализация виджетов
        self._init_ui()
        self._init_widget()
        self._init_connect()
        # Запуск таймера
        self._timer.start(1000)

    # Конструктор: настройки виджета
    def _init_ui(self):
        self.setFixedSize(320, 420)
        self.setWindowFlags(Qt.SplashScreen)

    # Конструктор: компоненты виджета
    def _init_widget(self):
        self._hbox = QHBoxLayout()
        self._vbox = QVBoxLayout()
        # Картинка
        self._pict = QPixmap(os.path.join(self._path, 'style/image', 'oops.png'))
        self._image = QLabel()
        self._image.setObjectName('image')
        self._image.setPixmap(self._pict)
        self._image.setFixedSize(self._width, self._width)
        # Сообщение
        self._text = QLabel(self._message)
        self._text.setObjectName('message')
        self._text.setFixedSize(self._width, 30)
        self._text.setAlignment(Qt.AlignCenter)
        # Сообщение с таймером
        self._timer_text = QLabel(self._timer_message % self._seconds)
        self._timer_text.setObjectName('timer')
        self._timer_text.setFixedSize(self._width, 30)
        self._timer_text.setAlignment(Qt.AlignCenter)
        # Кнопка
        self._btn_ok = WCPushButton('Ясн ;)')
        self._btn_ok.setFixedSize(100, 30)

        # Расскидываем по слоям
        self._vbox.addWidget(self._image)
        self._vbox.addWidget(self._text)
        self._vbox.addWidget(self._timer_text)
        self._hbox.addWidget(self._btn_ok)
        self._vbox.addLayout(self._hbox)
        self.setLayout(self._vbox)

    # Конструктор: слушатели
    def _init_connect(self):
        self._btn_ok.clicked.connect(self.close)
        self._timer.timeout.connect(self.timeout)

    # Метод: отображает окно
    def show(self):
        self.exec_()

    # Обработчик: закрытие окна
    def close(self):
        if self._parent:
            self.close()
        else:
            sys.exit(0)

    # Обработчик: обработка таймера
    def timeout(self):
        self._seconds -= 1
        self._timer_text.setText(self._timer_message % self._seconds)

        if self._seconds == 0:
            self.close()
