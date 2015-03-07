#!/usr/local/bin/python
# -*- coding:utf-8 -*-
u'''
写真を含むフォルダを引数とする。
フォルダ下の写真ファイルの平均のRGB値を取得し、データベースへ保存する。
ついでに、写真のサムネイルを作成し、thumbnailフォルダ下へ保存する。
'''
import os
import sys
import glob
import sqlite3
from PIL import Image
import numpy as np

inputdir = sys.argv[1]

conn = sqlite3.connect('./image.sqlite')
c = conn.cursor()

try:
    c.execute(u'''create table rgbdata
   (id integer primary key ,image_path text,red integer,green integer,blue integer) 
    ''')
except:
    pass

for image_file in glob.glob(inputdir+'/*.JPG'):
    im = Image.open(image_file)
    print image_file, im.size, im.format, im.mode
    if im.mode != 'RGB':
        im = im.convert('RGB')
        print im.size, im.format, im.mode

    # 画像データを保存
    px = im.load()
    pxs = []
    for x in range(0,im.size[0],5):
        for y in range(0,im.size[1],5):
            pxs.append(px[x,y])
    mean_rgb = np.mean(pxs, axis=0)
    rgb = tuple(map(int, mean_rgb))
    c = conn.cursor()
    c.execute(u'''insert into rgbdata values (NULL,'{0}',{1},{2},{3}) '''.format(
        os.path.splitext(os.path.basename(image_file))[0],
        rgb[0],
        rgb[1],
        rgb[2]
        ))
    conn.commit()
    c.close()

    # サムネイルを作成し、保存
    thumbnail_path = 'thumbnail/'+os.path.basename(image_file)
    if os.path.exists(thumbnail_path):
        continue
    thumbnail_size = (160,120)
    im.thumbnail(thumbnail_size)
    im.save(thumbnail_path)
