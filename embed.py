#!/usr/bin/env python
# -*- coding:utf-8 -*-

from jinja2 import Environment, PackageLoader, FileSystemLoader
import sqlite3
from PIL import Image
import numpy as np
from color_hash import colhash
import os
def pixelize(filename):
    num_width = 66
    num_height = 66

    # データベースから画像の情報を取得
    conn = sqlite3.connect('image.sqlite')
    c = conn.cursor()
    c.execute('select * from rgbdata')
    image_datas = c.fetchall()
    #image_pxs = np.array([ list(data[2:5])+[0.0] for data in image_datas])
    color_dict = {}
    for data in image_datas:
        if not color_dict.get(data[5]):
            color_dict[data[5]] = {}
            color_dict[data[5]]['name'] = []
            color_dict[data[5]]['pxs'] = []
        color_dict[data[5]]['pxs'].append(list(data[2:5])+[float(data[6])])
        color_dict[data[5]]['name'].append(data[1])
    # 画像から画像の情報を取得
    im = Image.open(filename)
    if im.mode != 'RGB':
        im = im.convert('RGB')

    px = im.load()
    pxs = []
    for iy,y in enumerate(np.linspace(1, im.size[1]-1, num_height)):
        if iy >= num_height:break
        for ix,x in enumerate(np.linspace(1,im.size[0]-1, num_width)):
            if ix >= num_width:break
            pxs.append(np.array(list(px[int(round(x)),int(round(y))])+[0.0]))

    def px_to_image(px):
        #distance = map(np.linalg.norm, np.subtract(image_pxs,px))
        
        distance = map(np.linalg.norm, np.subtract(color_dict[colhash(px)]['pxs'],px))
        min_index = np.argmin(distance)
        #image_pxs[min_index][3] += 0.0
        #return image_datas[min_index][1]
        name = color_dict[colhash(px)]['name'][min_index]
        return (name, os.path.basename(name).split('.')[0])

    images = map(px_to_image, pxs)

    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template('index.tpl.html')

    with open('index.html','w') as f:
        f.write( template.render({'images':images,'num':num_height*num_width}).encode('utf-8'))

if __name__ == '__main__':
    import sys
    pixelize(sys.argv[1])
>>>>>>> e2f7fd2420e21598d7b704c3dbf516e846e20fb6
