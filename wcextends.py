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


# Класс: системное расширение
class SystemExtend(WCClearExtend):

    """
    Класс системного расширения для консоли на PyQt5
    @author WorldCount
    @version 3
    @date 2016/04/17
    """

    # Конструктор
    def __init__(self):
        super(SystemExtend, self).__init__()
        self.name = 'SystemExtend'
        self.styles = {'system': '#756e58',
                       'error': '#e14343',
                       'info': '#44aee3',
                       'warn': '#ed9d20',
                       'success': '#4cb24a',
                       'color': ''
                       }

        self.open_tags = {'[system]': '<span style = "color:%s;">' % self.styles['system'],
                          '[error]': '<span style = "color:%s;">' % self.styles['error'],
                          '[info]': '<span style = "color:%s;">' % self.styles['info'],
                          '[warn]': '<span style = "color:%s;">' % self.styles['warn'],
                          '[success]': '<span style = "color:%s;">' % self.styles['success'],
                          '[none]': '<span style = "color:%s;">' % self.styles['color'],
                          '[b]': '<span style = "font-weight:bold;">',
                          '[normal]': '<span style = "font-weight:normal;">',
                          '[upper]': '<span style = "text-transform: uppercase;">',
                          '[tab]': '&nbsp;&nbsp;&nbsp;&nbsp;'
                          }

        self.close_tags = {'[/system]': '</span>',
                           '[/error]': '</span>',
                           '[/info]': '</span>',
                           '[/warn]': '</span>',
                           '[/success]': '</span>',
                           '[/none]': '</span>',
                           '[/b]': '</span>',
                           '[/normal]': '</span>',
                           '[/upper]': '</span>',
                           '[/tab]': '</span>'
                           }
