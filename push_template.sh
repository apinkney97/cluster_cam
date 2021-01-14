#!/bin/bash
set -eux

for host in p1 p2 p3 p4
do
    rsync -avz /home/pi/template/ $host:
done
