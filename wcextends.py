#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Расширения для консоли
"""

__date__ = "15.04.2016"
__author__ = "WorldCount"
__email__ = "world.count@yandex.ru"
__copyright__ = "Copyright 2016, Scr1pt1k.Ru"
__python_version__ = ""


# Класс: чистое расширение для консоли
class WCClearExtend(object):

    """
    Класс чистого расширения для консоли на PyQt5
    @author WorldCount
    @version 3
    @date 2016/04/15
    """

    # Конструктор
    def __init__(self):
        # Имя расширения
        self.name = 'undefined'
        # Стили
        self.styles = {}
        # Открывающие теги
        self.open_tags = {}
        # Закрывающие теги
        self.close_tags = {}