#!/usr/local/bin/python
# -*- coding:utf-8 -*-

import os
from bottle import route, run, static_file, redirect, request
from embed import pixelize
from import_image import ImportImage
from colemb import pallet_embed

@route('/')
def index():
    f = open('index.html', 'r')
    ret = f.read()
    return ret

@route('/pallet')
def index():
    f = open('pallet.html', 'r')
    ret = f.read()
    return ret

@route('/upload', method='POST')
def upload():
    photo = request.files.get('photo')
    image_filename = photo.filename
    print image_filename
    save_path = '/home/vagrant/happy_wedding/'
    photo.save(save_path+image_filename)
    pixelize(save_path+image_filename)
    return '''upload complete! <a href='/'>戻る</a>'''
#    redirect("/")

@route('/addpallet', method='POST')
def add_pallet():
    photo = request.files.get('photo')
    image_filename = photo.filename
    print image_filename
    save_path = '/home/vagrant/happy_wedding/image/'
    if not os.path.exists(save_path+image_filename):
        photo.save(save_path+image_filename)

    ii = ImportImage()
    ii.import_image(save_path+image_filename, 0)
    return '''add pallet complete! <a href='/'>戻る</a>'''
#    redirect("/")

@route('/colorcheck', method='POST')
def color_check():
    photo = request.files.get('photo')
    image_filename = photo.filename
    print image_filename
    save_path = '/home/vagrant/happy_wedding/tmp/'
    if not os.path.exists(save_path+image_filename):
        photo.save(save_path+image_filename)

    ii = ImportImage()
    rgb = ii.get_color(save_path+image_filename)
    data = {
        'name':image_filename,
        'color':rgb,
        'hashnum':ii.num_of_same_hash(rgb)
        }
    return pallet_embed(data)
#    redirect("/")

@route('/thumbnail/<filename>')
def thumbnail(filename):
    return static_file(filename, root='thumbnail')

@route('/static/<path>/<filename>')
def static(path, filename):
    return static_file(filename, root='static/'+path)

run(host='0.0.0.0', port=8888, debug=True, reloader=True)
