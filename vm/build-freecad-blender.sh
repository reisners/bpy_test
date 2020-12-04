#!/bin/bash

docker build -f Dockerfile-freecad-blender -t reisners/freecad-blender .
docker push reisners/freecad-blender
docker tag reisners/freecad-blender freecad-blender
