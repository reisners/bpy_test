#!/bin/bash

docker build -f Dockerfile-bpy -t reisners/bpy:v1.0 .
docker push reisners/bpy:v1.0
