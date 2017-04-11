#!/bin/bash
set -o allexport

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..

if [ -e .env ]; then
	source .env
fi
echo $OMAR_SEVICE1_DOCKER_IMAGE_LOCAL

docker build -t $OMAR_SEVICE1_DOCKER_IMAGE_LOCAL:$OMAR_SEVICE1_IMAGE_VERSION . 
