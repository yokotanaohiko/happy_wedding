#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import os
from bottle import route, run, static_file, redirect, request
from embed import pixelize
from import_image import ImportImage
from colemb import pallet_embed

save_path = '/home/job/githome/happy_wedding/tmp/'

@route('/')
def index():
    f = open('index.html', 'r')
    ret = f.read()
    return ret

@route('/happy_wedding')
def happy_wedding():
    redirect('/')

@route('/pallet')
def pallet():
    f = open('pallet.html', 'r')
    ret = f.read()
    return ret

@route('/upload', method='POST')
def upload():
    photo = request.files.get('photo')
    if not photo:
        redirect('/no_photo')

    image_filename = photo.filename
    if not os.path.exists(save_path+image_filename):
        photo.save(save_path+image_filename)
    pixelize(save_path+image_filename)
    data = {
        'status':'bg-success',
        'message':u"{0}をベースに変更しました。".format(image_filename)
        }
    return pallet_embed(data)

@route('/addpallet', method='POST')
def add_pallet():
    photos = list(map(lambda x: x[1], filter(lambda x: x[0] == "photo", request.POST.allitems())))
    if not photos[0]:
        redirect('/no_photo')
   
    image_num = len(photos)
    for photo in photos:
        image_filename = photo.filename
        if not os.path.exists(save_path+image_filename):
            photo.save(save_path+image_filename)

        ii = ImportImage()
        ii.import_image(save_path+image_filename)
    data = {
        'status':'bg-success',
        'message':u"{0}枚のピースを追加しました。".format(image_num)
        }
    return pallet_embed(data)

@route('/colorcheck', method='POST')
def color_check():
    photos = list(map(lambda x: x[1], filter(lambda x: x[0] == "photo", request.POST.allitems())))
    if not photos[0]:
        redirect('/no_photo')

    iroais = []
    for photo in photos:
        image_filename = photo.filename
        print image_filename
        if not os.path.exists(save_path+image_filename):
            photo.save(save_path+image_filename)

        ii = ImportImage()
        ii.import_image(save_path+image_filename, active=False)
        rgb = ii.get_color(save_path+image_filename)
        iroai = {
            'name':image_filename,
            'color':rgb,
            'hashnum':ii.num_of_same_hash(rgb),
            'path':'/thumbnail/{0}.png'.format(ii.get_last_id())
            }
        iroais.append(iroai)

    data = {
        'status':'bg-success',
        'iroais':iroais,
        'message':u"色合いの調査が終わりました。"
        }
    return pallet_embed(data)

@route('/no_photo')
def no_photo():
    data = {
        'status':'bg-warning',
        'message':u"ERROR!:ファイルが存在しません"
        }
    return pallet_embed(data)

@route('/thumbnail/<filename>')
def thumbnail(filename):
    return static_file(filename, root='thumbnail')

@route('/test_image/<filename>')
def test_image(filename):
    return static_file(filename, root='test_image')

@route('/image/<filename>')
def image(filename):
    return static_file(filename, root='image')

@route('/images/<filename>')
def images(filename):
    return static_file(filename, root='images')

@route('/static/<path>/<filename>')
def static(path, filename):
    return static_file(filename, root='static/'+path)

run(host='0.0.0.0', port=8888, debug=True, reloader=True)
