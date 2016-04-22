#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Команды для консоли
"""

__date__ = "15.04.2016"
__author__ = "WorldCount"
__email__ = "world.count@yandex.ru"
__copyright__ = "Copyright 2016, Scr1pt1k.Ru"
__python_version__ = ""


from .wcextends import WCClearExtend


# Класс: чистая команда дял консоли
class WCClearCommand(WCClearExtend):

    """
    Класс чистой команды для консоли на PyQt5
    @author WorldCount
    @version 3
    @date 2016/04/15
    """

    def __init__(self):
        super(WCClearCommand, self).__init__()
        # Список автозавершения команды
        self.complete_list = []
        # Описание команды
        self.desc = ''
        # Пример использования команды
        self.help = []

    # Метод: запуск выполнения команды
    def run(self, *args):
        return False

    # Метод: возвращает список автозавершения
    def get_complete_list(self):
        return self.complete_list


# Класс: команда вывода текста
class PrintCommand(WCClearCommand):

    """
    Класс команды вывода текста на PyQt5
    @author WorldCount
    @version 3
    @date 2016/04/15
    """

    # Конструктор
    def __init__(self):
        super(PrintCommand, self).__init__()
        self.name = 'print'
        self.desc = 'Выводит на экран форматированный текст'
        self.complete_list = ['print', 'текст']
        self.help = []

    # Метод: запуск выполнения команды
    def run(self, *args):
        return '%s' % ' '.join(args[0])
