#!/bin/bash

docker build -f Dockerfile-freecad-blender -t reisners/freecad-blender:master .
docker tag reisners/freecad-blender:master freecad-blender
docker push reisners/freecad-blender:master
