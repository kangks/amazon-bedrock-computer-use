#!/bin/bash
set -e

export DISPLAY=:${DISPLAY_NUM}

# to overcome Pillow grab error unsupported bit depth
Xvfb $DISPLAY -ac -screen 0 ${WIDTH}x${HEIGHT}x24 -dpi 96 2>${LOG_OUTPUT_FOLDER}/xvfb.err 1>${LOG_OUTPUT_FOLDER}/xvfb.log &
tint2 -c $HOME/app/tint2/tint2rc 2>${LOG_OUTPUT_FOLDER}/tint2.err 1>${LOG_OUTPUT_FOLDER}/tint2.log &
x11vnc -noxdamage -nopw -forever --viewonly --multiptr 2>${LOG_OUTPUT_FOLDER}/x11vnc.err 1>${LOG_OUTPUT_FOLDER}/x11vnc.log &

# exec "$@"
python3 $HOME/app/main.py "$@"
