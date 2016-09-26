#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Всплывающие сообщения
"""


import os
import sys
from PyQt5.QtWidgets import (QDialog, QLabel, QHBoxLayout, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import (QApplication, QDesktopWidget)
from PyQt5.QtCore import (Qt, QTimer, QSize)
from PyQt5.QtGui import (QPixmap, QPalette, QBrush)
from PyQt5.QtMultimedia import QSound
from .wcbuttons import WCPushButton


__date__ = "12.04.2016"
__author__ = "WorldCount"
__email__ = "world.count@yandex.ru"
__copyright__ = "Copyright 2016, Scr1pt1k.Ru"
__python_version__ = "3"


# Виды иконок для WCToolTipMessages
_ERROR = 1
_SUCCESS = 2
_WARN = 3
_INFO = 4
_WORK = 5


# Класс: всплывающее сообщение
class WCMessage(QDialog):

    """
    Класс всплывающего сообщения
    @author WorldCount
    @version 3
    @date 2016/07/07
    """

    # Конструктор
    def __init__(self, parent=None, flags=None):
        if flags:
            super(WCMessage, self).__init__(parent, flags)
        else:
            super(WCMessage, self).__init__(parent)
        self._parent = parent
        self._path = os.path.dirname(__file__)
        # Таймер
        self._timer = QTimer()


# Класс: сообщение с закрытием по таймеру
class WCMessageBoxTimer(WCMessage):

    """
    Класс сообщения с закрытием по таймеру на PyQt5
    @author WorldCount
    @version 3
    @date 2016/04/12
    """

    # Конструктор
    def __init__(self, message, seconds=None, parent=None):
        super(WCMessageBoxTimer, self).__init__(parent)
        self._message = message
        self._seconds = seconds if seconds else 10
        # Ширина виджетов
        self._width = 298
        # Таймер
        self._timer_message = 'Окно будет автоматически закрыто через <b>%s</b> сек.'
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
        # Слои
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
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
        vbox.addWidget(self._image)
        vbox.addWidget(self._text)
        vbox.addWidget(self._timer_text)
        hbox.addWidget(self._btn_ok)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

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


# Класс: всплывающее сообщение в виде тултипа
class WCToolTipMessages(WCMessage):

    """
    Класс всплывающего сообщения в виде тултипа на PyQt5
    @author WorldCount
    @version 3
    @date 2016/07/07
    """

    # Конструктор
    def __init__(self, parent=None, flags=Qt.FramelessWindowHint):
        super(WCToolTipMessages, self).__init__(parent, flags)
        # Секунд до закрытия
        self._seconds = 10
        # Смещение виджета в сторону от экрана
        self._offset = 2
        # Инициализация виджетов
        self._init_ui()
        self._init_object()
        self._init_widget()
        self._init_connect()

    # Конструктор: настройки виджета
    def _init_ui(self):
        width, height = 230, 130
        # Делаем рассчет где расположить виджет
        screen = QDesktopWidget().screenGeometry()
        desktop = QApplication.desktop()
        taskbar_height = desktop.screenGeometry().height() - desktop.availableGeometry().height()
        self.move(screen.width() - width - self._offset, screen.height() - height - taskbar_height - self._offset)
        self.setFixedSize(width, height)

    # Конструктор: инициализация объектов
    def _init_object(self):
        self._icon_size = QSize(24, 24)
        # Буфер обмена
        self._clipboard = QApplication.clipboard()
        # Звуковое уведомление
        sound_file = os.path.join(self._path, 'style/sound', 'notify.wav')
        self._sound = QSound(sound_file)
        # Иконки
        self._icon_work = QPixmap(os.path.join(self._path, 'style/icon', 'work.png'))
        self._icon_success = QPixmap(os.path.join(self._path, 'style/icon', 'success.png'))
        self._icon_info = QPixmap(os.path.join(self._path, 'style/icon', 'info.png'))
        self._icon_warn = QPixmap(os.path.join(self._path, 'style/icon', 'warning.png'))
        self._icon_error = QPixmap(os.path.join(self._path, 'style/icon', 'error.png'))

    # Конструктор: компоненты виджета
    def _init_widget(self):
        # Слои
        vbox = QVBoxLayout()
        vbox_widget = QVBoxLayout()
        vbox_widget.setSpacing(0)
        hbox = QHBoxLayout()
        hbox.setSpacing(7)
        # Иконка
        self._icon = QLabel('')
        self._icon.setFixedSize(self._icon_size)
        self._icon.setPixmap(self._icon_work)
        # Заголовок
        self._title = QLabel('')
        self._title.setObjectName('title')
        self._title.setTextFormat(Qt.RichText)
        self._title.setFixedSize(172, 24)
        self._title.setAlignment(Qt.AlignVCenter)
        # Сообщение
        self._text = QLabel('')
        self._text.setObjectName('text')
        self._text.setTextFormat(Qt.RichText)
        self._text.setTextInteractionFlags(Qt.LinksAccessibleByMouse | Qt.TextSelectableByMouse)
        self._text.setFixedSize(202, 70)
        self._text.setAlignment(Qt.AlignLeft)

        # Расскидываем по слоям
        hbox.addWidget(self._icon)
        hbox.addWidget(self._title)
        hbox.addStretch()
        vbox_widget.addLayout(hbox)
        vbox_widget.addStretch()
        vbox_widget.addWidget(self._text)
        vbox_widget.addStretch()
        vbox.addLayout(vbox_widget)
        self.setLayout(vbox)

    # Конструктор: слушатели
    def _init_connect(self):
        self._timer.timeout.connect(self.timeout)
        self._text.mousePressEvent = self.text_click

    # Метод: запускает таймер и отображает окно
    def show_timer(self, title, text, seconds=5, play_sound=True, icon=_WORK):
        # Выбираем иконку
        self._icon.setPixmap(self.get_icon(icon))
        # Устанавливаем время отображения окна
        if seconds:
            self._seconds = seconds
        else:
            self._seconds = 10
        # Устанавливаем заголовок
        if title:
            self.set_title(title)
        # Устанавливаем текст
        if text:
            self.set_text(text)
        # Запускаем таймер
        self._timer.start(1000)
        # Проигрываем звук
        if play_sound:
            self._sound.play()
        # Отображаем окно
        self.show()

    # Метод: выбирает иконку
    def get_icon(self, icon):
        if icon == _WARN:
            icon = self._icon_warn
        elif icon == _INFO:
            icon = self._icon_info
        elif icon == _ERROR:
            icon = self._icon_error
        elif icon == _SUCCESS:
            icon = self._icon_success
        else:
            icon = self._icon_work
        return icon

    # Метод: устанавливает заголовок
    def set_title(self, text):
        if text:
            self._title.setText(text)

    # Метод: устанавливает текст
    def set_text(self, text):
        if text:
            self._text.setText(text)

    # Обработчик: обработка таймера
    def timeout(self):
        self._seconds -= 1
        if self._seconds == 0:
            self.hide()

    # Обработчик: двойной клик по окну
    def text_click(self, event):
        text = self._text.text().replace('<br>', '\n').replace('<b>', '').replace('</b>', '')
        self._clipboard.setText(text)
        self.hide()

    # Обработчик: клик по окну
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.text_click(event)
        return QWidget.mousePressEvent(self, event)


# Класс: всплывающее сообщение в виде тултипа c прозрачностью
class WCToolTipMessagesGrass(WCToolTipMessages):

    """
    Класс всплывающего сообщения в виде тултипа c прозрачностью на PyQt5
    @author WorldCount
    @version 3
    @date 2016/04/12
    """

    # Конструктор
    def __init__(self, parent=None):
        super(WCToolTipMessagesGrass, self).__init__(parent, Qt.FramelessWindowHint)

    # Конструктор: настройки виджета
    def _init_ui(self):
        super(WCToolTipMessagesGrass, self)._init_ui()
        # Делаем виджет прозрачным
        self.setAttribute(Qt.WA_TranslucentBackground, True)

    # Конструктор: компоненты виджета
    def _init_widget(self):
        # Слои
        vbox = QVBoxLayout()
        vbox_widget = QVBoxLayout()
        vbox_widget.setSpacing(0)
        hbox = QHBoxLayout()
        hbox.setSpacing(7)
        # Фон
        image = QPixmap(os.path.join(self._path, 'style/image', 'background.png'))
        background = QPalette()
        background.setBrush(QPalette.Window, QBrush(QPixmap(image)))
        # Иконка
        self._icon = QLabel('')
        self._icon.setFixedSize(self._icon_size)
        self._icon.setPixmap(self._icon_work)
        # Заголовок
        self._title = QLabel('')
        self._title.setObjectName('title')
        self._title.setTextFormat(Qt.RichText)
        self._title.setFixedSize(172, 24)
        self._title.setAlignment(Qt.AlignVCenter)
        # Сообщение
        self._text = QLabel('')
        self._text.setObjectName('text')
        self._text.setTextFormat(Qt.RichText)
        self._text.setTextInteractionFlags(Qt.LinksAccessibleByMouse | Qt.TextSelectableByMouse)
        self._text.setFixedSize(202, 70)
        self._text.setAlignment(Qt.AlignLeft)
        # Тело
        self._body = QWidget()
        self._body.setAutoFillBackground(True)
        self._body.setFixedSize(220, 130)
        self._body.setPalette(background)

        # Расскидываем по слоям
        hbox.addWidget(self._icon)
        hbox.addWidget(self._title)
        hbox.addStretch()
        vbox_widget.addLayout(hbox)
        vbox_widget.addStretch()
        vbox_widget.addWidget(self._text)
        vbox_widget.addStretch()
        self._body.setLayout(vbox_widget)
        vbox.addWidget(self._body)
        self.setLayout(vbox)
