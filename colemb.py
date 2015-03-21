#!/usr/bin/env python
# -*- coding:utf-8 -*-

from jinja2 import Environment, PackageLoader, FileSystemLoader
import sqlite3


qt = 64
iqt = 256/qt
conn = sqlite3.connect('image.sqlite')
c = conn.cursor()
c.execute('''
select hash, count(id) from rgbdata where penalty <= 1000 group by hash
        ''')
image_data = c.fetchall()

# ヒストグラムを作成
hist = [0]*(iqt**3)
for img in image_data:
    hist[img[0]]=img[1]

data = []
for index,h in enumerate(hist):
    r = (index%iqt)*qt
    g = ((index/iqt)%iqt)*qt
    b = (index/(iqt*iqt))*qt
    data.append([r,g,b,h])

env = Environment(loader=FileSystemLoader('./'))
template = env.get_template('pallet.tpl.html')

with open('pallet.html','w') as f:
    f.write( template.render({'datas':data}).encode('utf-8'))
