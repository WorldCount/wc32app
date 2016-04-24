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


import socket
import datetime
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
        self.complete_list = """
print
    текст
"""
        self.help = [
            '[success][b]print[/success] [warn]Текст[/warn][/b] - выводит форматированый текст',
        ]

    # Метод: запуск выполнения команды
    def run(self, *args):
        return '%s' % ' '.join(args[0])


# Класс: команда вывода текущей даты и времени
class DateTimeCommand(WCClearCommand):

    """
    Класс команды вывода текущей даты и времени на PyQt5
    @author WorldCount
    @version 3
    @date 2016/04/23
    """

    # Конструктор
    def __init__(self):
        super(DateTimeCommand, self).__init__()
        self.name = 'date'
        self.desc = 'Выводит на экран текущую дату и время'
        self.complete_list = """
date
"""
        self.help = [
            '[success][b]date[/b][/success] - выводит дату и время',
        ]

    # Метод: запуск выполнения команды
    def run(self, *args):
        now_date = datetime.datetime.now()
        return '[warn]%s[/warn]' % now_date.strftime('%d.%m.%Y %H:%M:%S')


# Класс: команды вывода текущего хоста
class HostCommand(WCClearCommand):

    """
    Класс команды вывода текущего хоста на PyQt5
    @author WorldCount
    @version 3
    @date 2016/04/23
    """

    # Конструктор
    def __init__(self):
        super(HostCommand, self).__init__()
        self.name = 'host'
        self.desc = 'Выводит на экран текущий ip-адресс хоста'
        self.complete_list = """
host
"""
        self.help = [
            '[success][b]host[/b][/success] - выводит текущий ip-адресс хоста',
        ]

    # Метод: запуск выполнения команды
    def run(self, *args):
        host = socket.gethostbyname(socket.gethostname())
        return '[warn]%s[/warn]' % host
