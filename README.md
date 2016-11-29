# CAEN Docker Flask App

Flask app used to test and standardize deployments to AWS using Docker.


## Requirements

[AWS CLI](https://aws.amazon.com/cli/)

[Docker Engine](https://docs.docker.com/engine/installation/)

[DockerHub Account](https://hub.docker.com/)


## Deployment

All deployment instructions will be documented below. This is designed to
standardize deployments. If you would like to make changes to this process,
please create a pull request.


### AWS Virtual Machines

Our apps will be running on Ubuntu (Currently 15.10) VMs in AWS.

1. Edit aws-dm Credentials
	* ID and Key usually found in `~/.aws/credentials`
	* __This file is not yet included, pending approval. If needed
immediately, contact tknox@umich.edu.__

2. Run aws-dm following the prompts
	* Repeat for the number of VMs you would like to be in you Docker Swarm


### Docker Swarm

Find IP of Host VM

1. [Log into UMich AWS Console](https://michigan-engineering.signin.aws.amazon.com/console)
2. Find Private IP
	* Services > EC2 > Instances > YOUR_INSTANCE > Private IP
3. You can also find the Private IP through SSH - [Official Documentation](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html)

	1. `ssh -i /PATH/TO/KEY ubuntu@PUBLIC_DNS`
		* Key Pair is usually located in `~/.docker/machine/machines/INSTANCE_NAME/id_rsa`
	2. `ifconfig -a`
	3. eth0 -> inet addr

Point Docker Machine to Manager

`eval $(docker-machine env INSTANCE_NAME)`

Initiate Docker Swarm

1. `docker swarm -init --advertise-addr PRIVATE_IP:2377`
2. Copy the JOIN command
	* `docker swarm join --token LONG_TOKEN_STRING PRIVATE_IP:2377`

Join Workers

1. Point your Docker Machine to a worker VM
2. Run the JOIN command
3. Repeat with other worker VMs

Check Status

1. Switch back to Manager
2. Run `docker node ls`
3. Check if all manager and worker nodes are present


### Dockerize Flask App

Create a Dockerfile
* Simple Flask example can be found in this repository
* [Official Documentation](https://docs.docker.com/engine/reference/builder/)


### Docker Hub

__This documentation uses your personal DockerHub account and will need to be updated
for CAEN Organization__

We next need to link the GitHub repository to DockerHub so it can autogenerate
a Docker image, which will be used in the swarm.

Log into your [DockerHub](https://hub.docker.com/) account

Create a Automated Build

1. Create > Create Automated Build > GitHub
2. Link Account (with full access) if not sone so already
3. Choose Repository

You may have to force the first build

1. YOUR_DOCKER_REPO > Build Settings
2. Trigger the build you would like (used for versioning)
3. YOUR_DOCKER_REPO > Build Details
4. Wait until build completed


### Create Service

Point Docker Machine to Manager

`eval $(docker-machine env INSTANCE_NAME)`

Create Service

`docker service create --name NAME_OF_SERVICE DockerHub_Image`
* Ex: `docker service create --name flask_app iamttc/docker-flask`

Scale

To increase the number of containers running in the service, use
`docker service scale test=X` where X is the desired number

Publish

`docker service update --publish-add 80:80 NAME_OF_SERVICE` publishes to port 80


### View Service

To view the service you just created, find the Public DNS of your AWS Instances.

1. 1. [Log into UMich AWS Console](https://michigan-engineering.signin.aws.amazon.com/console)
2. Find Public DNS
	* Services > EC2 > Instances > YOUR_INSTANCE > Public DNS
	* Connect to any swarm instance to view the service


### Edit Service

To find additional information about updating or changing a service, view
the [Official Documentation](https://docs.docker.com/engine/reference/commandline/service_create/).
This documentation starts at `service create` but information on the other commands
can be found at the bottom.
