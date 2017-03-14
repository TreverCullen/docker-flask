#!/bin/bash
# Created by Trever Cullen

echo $1
echo $2

eval $(docker-machine env $1)
eval $($2)
