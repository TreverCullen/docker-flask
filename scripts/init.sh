#!/bin/bash
# Created by Trever Cullen

eval $(docker-machine env $1)
docker swarm init --advertise-addr eth0:2377
