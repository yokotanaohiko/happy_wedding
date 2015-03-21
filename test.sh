#!/bin/sh

if [ $# -ne 1 ]; then
    python embed.py heart.png
else
    python embed.py $1
fi

if [ "$(uname)" == 'Darwin' ]; then
    echo 'mac!'
    open index.html
elif [ "$(expr substr $(uname -s) 1 5)" == 'Linux' ]; then
    python -B app.py
else
    echo "your platform ($(uname -a)) is not supported."
fi
