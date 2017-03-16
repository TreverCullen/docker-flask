#!/bin/bash
# Created by Trever Cullen

eval $(docker-machine env $1)
docker node ls
docker swarm join-token worker
