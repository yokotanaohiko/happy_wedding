#!/usr/bin/env python
# -*- coding:utf-8 -*-

from jinja2 import Environment, PackageLoader, FileSystemLoader
import sqlite3
from PIL import Image
import numpy as np

num_width = 66
num_height = 66

# データベースから画像の情報を取得
conn = sqlite3.connect('image.sqlite')
c = conn.cursor()
c.execute('select * from rgbdata')
image_datas = c.fetchall()
image_pxs = np.array([ data[2:5] for data in image_datas])

# 画像から画像の情報を取得
im = Image.open('maka3.png')
if im.mode != 'RGB':
    im = im.convert('RGB')

px = im.load()
pxs = []
for iy,y in enumerate(np.linspace(1, im.size[1]-1, num_height)):
    if iy >= num_height:break
    for ix,x in enumerate(np.linspace(1,im.size[0]-1, num_width)):
        if ix >= num_width:break
        pxs.append(np.array(px[int(round(x)),int(round(y))]))

def px_to_image(px):
    distance = map(np.linalg.norm, np.subtract(image_pxs,px))
    return image_datas[np.argmin(distance)][1]
images = map(px_to_image, pxs)

env = Environment(loader=FileSystemLoader('./'))
template = env.get_template('index.tpl.html')

with open('index.html','w') as f:
    f.write( template.render({'images':images}).encode('utf-8'))
