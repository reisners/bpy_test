#!/bin/bash

docker build -f Dockerfile-bpy -t reisners/bpy:master .
docker push reisners/bpy:master
docker tag reisners/bpy:master bpy
