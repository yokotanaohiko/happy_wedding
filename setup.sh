#!/bin/sh

wget http://www.ijg.org/files/jpegsrc.v8c.tar.gz
tar zxvf jpegsrc.v8c.tar.gz
sudo pip install pillow
sudo pip install jinja2
mkdir images
mkdir thumbnail
./make_test_image.py
./import_image.py images
