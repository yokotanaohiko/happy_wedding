#!/bin/sh

python embed.py

if [ "$(uname)" == 'Darwin' ]; then
    echo 'mac!'
    open index.html
elif [ "$(expr substr $(uname -s) 1 5)" == 'Linux' ]; then
    python -B app.py
else
    echo "your platform ($(uname -a)) is not supported."
fi
