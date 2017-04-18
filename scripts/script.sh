#!/bin/bash
# Created by Trever Cullen

eval $(docker-machine env $1)
$2
