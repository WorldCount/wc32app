#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Рабочие функции
"""

__date__ = "15.04.2016"
__author__ = "WorldCount"
__email__ = "world.count@yandex.ru"
__copyright__ = "Copyright 2016, Scr1pt1k.Ru"
__python_version__ = "3"


import ctypes

_dll = ctypes.windll.LoadLibrary("user32.dll")


# Возвращает раскладку пользователя
def get_user_language():
    lang = getattr(_dll, "GetKeyboardLayout")
    val = lang(0)

    if val == 67699721:
        return 'en'
    elif val == 68748313:
        return 'ru'
    else:
        return None