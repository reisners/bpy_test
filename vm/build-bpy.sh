#!/bin/bash

sudo docker build -f Dockerfile-bpy -t reisners/bpy .
sudo docker push reisners/bpy
sudo docker tag reisners/bpy bpy
