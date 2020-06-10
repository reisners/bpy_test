#!/bin/bash

sudo docker build -f Dockerfile-freecad-blender -t reisners/freecad-blender .
sudo docker push reisners/freecad-blender
sudo docker tag reisners/freecad-blender freecad-blender
