#!/bin/bash
set -eu
width=640
height=360
bitrate=1000000
/usr/bin/raspivid -w ${width} -h ${height} -b ${bitrate} -g 50 -fps 25 -t 0 -a 12 -a '%Y-%m-%d %X' -l -o tcp://0.0.0.0:3333

