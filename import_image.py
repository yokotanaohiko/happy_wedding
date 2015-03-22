#!/usr/bin/env python
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
from color_hash import colhash

class ImportImage():
    u'''画像をインポートするクラス'''

    def __init__(self):
        pass

    def connect(self):
        u'''sqlite のコネクションを張る'''

        self.conn = sqlite3.connect('./image.sqlite')
        c = self.conn.cursor()

        try:
            c.execute(u'''create table rgbdata
           (id integer primary key ,image_path text,red integer,green integer,blue integer,hash integer, penalty integer, active integer) 
            ''')
        except:
            pass

    def get_color(self, image_file):
        u'''画像の平均色を( R,G,B )で返す'''

        name,ext = os.path.splitext(image_file)
        if ext not in ('.png','.JPG','.jpg','.jpeg'):
            return None
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
        return tuple(map(int, mean_rgb))

    def num_of_same_hash(self, rgb):
        if 'conn' not in dir( self ):
            self.connect()
        
        c = self.conn.cursor()
        try:
            c.execute('''
            select count(id) from rgbdata where hash = {0} and penalty <= 1000 and active=1
            '''.format(colhash(rgb)))
            num = c.fetchall()
            return num[0][0]
        except:
            return None

    def get_last_id(self):
        if 'last_id' in dir(self):
            return self.last_id

        if 'conn' not in dir( self ):
            self.connect()
        
        c = self.conn.cursor()
        try:
            c.execute('''
            select id from rgbdata order by id desc limit 1
            ''')
            id = c.fetchall()
            self.last_id = int( id[0][0] )
            print id
            return self.last_id
        except:
            return 0


    def make_thumbnail(self, image_file):
        u'''サムネイルとコピーをpng形式で保存'''
        name,ext = os.path.splitext(image_file)
        if ext not in ('.png','.JPG','.jpg','.jpeg'):
            return None
        im = Image.open(image_file)
        if im.mode != 'RGB':
            im = im.convert('RGB')

        # コピーを保存(上書き)
        copy_path = 'images/'+str(self.get_last_id())+'.png'
        if os.path.exists(copy_path):
            os.remove(copy_path)
        im.save(copy_path)

        # サムネイルを保存(上書き)
        thumbnail_path = 'thumbnail/'+str(self.get_last_id())+'.png'
        thumbnail_size = (160,120)
        im.thumbnail(thumbnail_size)
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
        im.save(thumbnail_path)

    def import_image(self, image_file, penalty=0, active=True):
        u'''画像をsqliteにインポートする'''
        rgb = self.get_color(image_file)
        if 'conn' not in dir( self ):
            self.connect()

        # 以前にインポートしたことがあるかどうかを確認
        try:
            c = self.conn.cursor()
            c.execute(u'''
                select id, active from rgbdata where red={0} and green={1} and blue={2} and image_path='{3}'
                '''.format(
                    rgb[0],
                    rgb[1],
                    rgb[2],
                    image_file 
                    ))
            state = c.fetchall()
            print 'Image {0} is already imported '.format(state[0][0])
            c.execute(u'''
                update rgbdata set active=1 where id={0}
                    '''.format(state[0][0]))
            c.close()
            return None
        except:
            pass
        
        # idをインクリメント(get_last_idメソッドの都合でここじゃなきゃだめ)
        self.last_id = self.get_last_id()+1

        try:
            c = self.conn.cursor()
            c.execute(u'''insert into rgbdata values (NULL,'{0}',{1},{2},{3},{4},{5},{6}) '''.format(
                image_file,
                rgb[0],
                rgb[1],
                rgb[2],
                colhash(rgb),
                penalty,
                int( active )
                ))
            self.conn.commit()
            c.close()
        except:
            self.last_id -= 1

        self.make_thumbnail(image_file)



    def import_dir(self, inputdir, penalty):
        u'''指定したディレクトリ下にある画像をすべてインポートする'''
        for image_file_path in glob.glob(inputdir+'/*'):
            self.import_image(image_file_path, penalty)

if __name__ == '__main__':
    inputname = sys.argv[1]
    penalty = sys.argv[2] if sys.argv[2] else 0
    ii = ImportImage()

    if os.path.isfile(inputname):
        ii.import_image(inputname, penalty)
    elif os.path.isdir(inputname):
        ii.import_dir(inputname, penalty)
    else:
        print 'no such files!'
   
