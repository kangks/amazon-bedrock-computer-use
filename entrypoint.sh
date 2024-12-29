#!/bin/bash
set -e

export DISPLAY=:${DISPLAY_NUM}

# to overcome Pillow grab error unsupported bit depth
Xvfb $DISPLAY -ac -screen 0 ${WIDTH}x${HEIGHT}x24 -dpi 96 &
tint2 -c $HOME/app/tint2/tint2rc &
x11vnc -noxdamage -nopw -forever --viewonly --multiptr &

# exec "$@"
python3 $HOME/app/main.py "$@"
