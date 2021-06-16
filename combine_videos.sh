#!/bin/bash

# Borrowed from
# https://ottverse.com/stack-videos-horizontally-vertically-grid-with-ffmpeg

set -eu

# Pass this in as an env var
youtube_key="${YT_KEY}"
twitch_key="${TWITCH_KEY}"

twitch_url="rtmp://live-lhr.twitch.tv/app/${twitch_key}"
youtube_url="rtmp://a.rtmp.youtube.com/live2/${youtube_key}"

# stream_url="${twitch_url}"
stream_url="${youtube_url}"

ffmpeg \
    -ar 44100 \
    -ac 2 \
    -acodec pcm_s16le \
    -f s16le \
    -ac 2 \
    -i /dev/zero \
    -i tcp://p1:3333/ \
    -i tcp://p2:3333/ \
    -i tcp://p3:3333/ \
    -i tcp://p4:3333/ \
    -filter_complex \
        "[1:v][2:v]hstack=inputs=2[top]; \
         [3:v][4:v]hstack=inputs=2[bottom]; \
         [top][bottom]vstack=inputs=2[v]" \
    -map "[v]" \
    -acodec aac \
    -ab 128k \
    -g 50 \
    -strict experimental \
    -f flv \
    "${stream_url}"
    
