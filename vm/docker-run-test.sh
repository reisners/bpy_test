#!/bin/bash

model=$1

docker run -v $PWD:/work -it freecad-blender python scripts/test.py $model
