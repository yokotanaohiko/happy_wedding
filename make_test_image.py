#!/usr/bin/env python
# -*- coding:utf-8 -*-
u'''連番の数値が書かれた画像を生成する'''

from PIL import Image, ImageDraw, ImageFont

def make_number_image():
    text_color = 'black'
    font = ImageFont.truetype('/Library/Fonts/Verdana Bold.ttf', 60)
    for num in range(1089):
        im = Image.new('RGB',(160,120),color=(255,255,255))
        draw = ImageDraw.Draw(im)
        draw.text((10,10), str( num ),font=font, fill=text_color)
        del(draw)
        im.save('./thumbnail/test{0}.png'.format(num))

def make_color_image():
    for num in range(1000):
        im = Image.new('RGB',(160,120),color=(25*( (num/100)%10 ),25*(( num/10 )%10),25*(num%10)))
        im.save('./image/test{0}.png'.format(num))

if __name__ == '__main__':
    make_color_image()
