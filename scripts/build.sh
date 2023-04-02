#!/usr/bin/env bash
set -eu

IMAGE_NAME="fastapi-auth0-code-flow-build"

CWD="$(pwd)"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
BASE_DIR=$(realpath $SCRIPT_DIR/..)

cd $BASE_DIR

docker build -f Dockerfile                   \
             -t $IMAGE_NAME                  .
docker run   --rm                            \
             --user "$(id -u):$(id -g)"      \
             --volume $BASE_DIR:/src_code:rw \
             $IMAGE_NAME
