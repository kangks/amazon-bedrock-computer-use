#!/bin/bash
set -e

export DISPLAY=:${DISPLAY_NUM}

# Xvfb &
Xvfb $DISPLAY -ac -screen 0 ${WIDTH}x${HEIGHT}x16 -dpi 96 &
tint2 -c $HOME/app/tint2/tint2rc &
x11vnc -noxdamage -nopw -forever --viewonly --multiptr &
# x11vnc -noxdamage -nopw -forever --multiptr &

# exec "$@"
python3 $HOME/app/computer_use.py "$@"
