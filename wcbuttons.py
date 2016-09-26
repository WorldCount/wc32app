#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Кнопки
"""

import os
from PyQt5.QtWidgets import (QPushButton, QHBoxLayout, QLabel, QFrame, QVBoxLayout)
from PyQt5.QtCore import (Qt, pyqtSignal)


__date__ = "07.04.2016"
__author__ = "WorldCount"
__email__ = "world.count@yandex.ru"
__copyright__ = "Copyright 2016, Scr1pt1k.Ru"
__python_version__ = "3"


# Класс: простая кнопка
class WCPushButton(QPushButton):

    """
    Класс простой кнопки на PyQt5
    @author WorldCount
    @version 3
    @date 2016/04/07
    """

    # Конструктор
    def __init__(self, *args):
        super(WCPushButton, self).__init__(*args)
        self._path = os.path.dirname(__file__)


# Класс: кнопка со статусом
class WCStatusButton(QFrame):

    """
    Класс кнопки со статусом на PyQt5
    @author WorldCount
    @version 3
    @date 2016/04/07
    """

    # Сигнал: клик по кнопке
    clicked = pyqtSignal()

    # Конструктор
    def __init__(self, parent=None):
        super(WCStatusButton, self).__init__(parent)
        self._parent = parent
        self._init_ui()
        self._init_widget()
        # Возможные состояния
        self._state = ['normal', 'on', 'off', 'wait']
        self._current_state = 0
        self._checkable = False
        self._checked = False

    # Конструктор: настройки виджета
    def _init_ui(self):
        self.setFixedSize(140, 40)
        self.setProperty('pressed', False)

    # Конструктор: компоненты виджета
    def _init_widget(self):
        vbox = QVBoxLayout()
        vbox.setContentsMargins(0, 0, 0, 0)
        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        # Текст кнопки
        self.text = QLabel('Название', self)
        self.text.setObjectName('text')
        self.text.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)
        self.text.setFixedSize(100, 30)
        # Статус кнопки
        self.status = QLabel('')
        self.status.setObjectName('status')
        self.status.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)
        self.status.setFixedSize(28, 28)
        # Композиция
        hbox.addWidget(self.text)
        hbox.addStretch()
        hbox.addWidget(self.status)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

    # Метод: меняет цвет статуса на "включено"
    def set_on_state(self):
        state_num = self._state.index('on')
        self._current_state = state_num
        self.status.setProperty('state', 'on')
        self.reload_status()

    # Метод: меняет цвет статуса на "выключено"
    def set_off_state(self):
        state_num = self._state.index('off')
        self._current_state = state_num
        self.status.setProperty('state', 'off')
        self.reload_status()

    # Метод: меняет цвет статуса на "ожидание"
    def set_wait_state(self):
        state_num = self._state.index('wait')
        self._current_state = state_num
        self.status.setProperty('state', 'wait')
        self.reload_status()

    # Метод: меняет цвет статуса на "нормальный"
    def set_normal_state(self):
        state_num = self._state.index('normal')
        self._current_state = state_num
        self.status.setProperty('state', 'normal')
        self.reload_status()

    # Метод: меняет статус по очереди
    def change_state(self):
        self._current_state += 1
        if self._current_state >= len(self._state):
            self._current_state = 0
        self.status.setProperty('state', self._state[self._current_state])
        self.reload_status()

    # Метод: меняет текст на кнопке
    def set_text(self, text):
        if text:
            self.text.setText(text)

    # Метод: перезагружает стили статуса
    def reload_status(self):
        self.style().unpolish(self.status)
        self.style().polish(self.status)

    # Метод: перезагружает стили текста
    def reload_text(self):
        self.style().unpolish(self.text)
        self.style().polish(self.text)

    # Метод: перезагружает стили кнопки
    def reload_self(self):
        self.style().unpolish(self)
        self.style().polish(self)

    # Метод: устанавливает работу кнопки в режиме нажатия
    def set_checkable(self, bool_value):
            self._checkable = bool(bool_value)

    # Метод: устанавливает нажатие кнопки
    def set_checked(self, bool_value):
        self._checked = bool(bool_value)

        if self._checked:
            self.setProperty('checked', True)
            self.text.setProperty('checked', True)
            self.status.setProperty('checked', True)
        else:
            self.setProperty('checked', False)
            self.text.setProperty('checked', False)
            self.status.setProperty('checked', False)
        self.reload_status()
        self.reload_text()
        self.reload_self()

    # Обработчик: отпускание кнопки мыши
    def mouseReleaseEvent(self, event):
        if not self._checkable:
            self.setProperty('pressed', False)
            self.text.setProperty('pressed', False)
            self.status.setProperty('pressed', False)
            self.reload_status()
            self.reload_text()
            self.reload_self()
        event.accept()

    # Обработчик: нажатие кнопки мыши
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self._checkable:
                self.set_checked(not self._checked)
            else:
                self.setProperty('pressed', True)
                self.text.setProperty('pressed', True)
                self.status.setProperty('pressed', True)
                self.reload_status()
                self.reload_text()
                self.reload_self()
            self.clicked.emit()
            event.accept()
        event.ignore()

    # Обработчик: наведение мыши
    def enterEvent(self, event):
        if self.text.isEnabled():
            self.status.setProperty('select', True)
            self.reload_status()
            event.accept()
        event.ignore()

    # Обработчик: покидание зоны мышкой
    def leaveEvent(self, event):
        if self.text.isEnabled():
            self.status.setProperty('select', False)
            self.reload_status()
            event.accept()
        event.ignore()
