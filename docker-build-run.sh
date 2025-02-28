#!/bin/bash

IMAGE_NAME=marhoy/meteogram
VERSION=$(uv run --with setuptools_scm -m setuptools_scm)
LOCAL_PORT=8080

echo -e "\n\nBuilding version $VERSION...\n\n"
docker buildx build --platform linux/amd64,linux/arm64 --build-arg VERSION=$VERSION --tag $IMAGE_NAME:$VERSION --tag $IMAGE_NAME:latest .

echo -e "\n\nRunning container on http://localhost:$LOCAL_PORT\n\n"
docker run --rm --publish $LOCAL_PORT:5000 $IMAGE_NAME:$VERSION
