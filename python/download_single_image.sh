#!/bin/bash 

IMAGE_PATH=$1

aws s3 cp s3://servile-snapshots/successful-tests/$IMAGE_PATH .
