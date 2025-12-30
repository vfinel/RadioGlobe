#! /usr/bin/sh
# this script is mostly useful for debug purposes !
kill $(pgrep python)
python main.py &
