#!/usr/local/bin/python
# -*- coding:utf-8 -*-

qt = 64
iqt = 256/qt
def colhash(color):
    return int(color[0]/qt)+int(color[1]/qt)*iqt+int(color[2]/qt)*iqt*iqt
