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
        # Пример использования команды
        self.help = []

    # Метод: Запуск выполнения команды
    def run(self):
        return False
