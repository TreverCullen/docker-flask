# CAEN Docker Flask App

Flask app used to test and standardize deployments to AWS running Ubuntu 15.10 and Docker 1.12.

## Requirements

[AWS CLI](https://aws.amazon.com/cli/)

[Docker Engine](https://docs.docker.com/engine/installation/)

[DockerHub Account](https://hub.docker.com/)


## Deployment

All deployment instructions will be documented below. This is designed to
standardize deployments. If you would like to make changes to this process,
please create a pull request.


## 1. AWS Virtual Machines

Edit aws-dm credentials to reflect your AWS ID and KEY.

ID and Key are usually found here:
```
~/.aws/credentials
```
Run aws-dm and follow the prompts to create your desired number of VMs for the swarm.


## 2. Docker Swarm

__Find IP of Host VM__


Find Private IP on [AWS Console](https://michigan-engineering.signin.aws.amazon.com/console)

```
Services > EC2 > Instances > YOUR_INSTANCE > Private IP
```
You can also find the Private IP through [AWS SSH](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html)

```
ssh -i /PATH/TO/KEY ubuntu@PUBLIC_DNS
ifconfig -a
# eth0 > inet addr
```

The default key pair for each VM is usually located here:
```
~/.docker/machine/machines/INSTANCE_NAME/id_rsa
```

__Point Docker Machine to Manager__

```
eval $(docker-machine env INSTANCE_NAME)
```

__Initiate Docker Swarm__

```
docker swarm -init --advertise-addr PRIVATE_IP:2377
```
Copy the JOIN command

```
docker swarm join --token LONG_TOKEN_STRING PRIVATE_IP:2377
```

__Join Workers__

Point your Docker Machine to a worker VM and run the JOIN command. Repeat for the remaining workers.

__Check Status__

Run the command:
```
docker node ls
```
Check if all nodes are part of the swarm.


## 3. Dockerize Flask App

Create a [Dockerfile](https://docs.docker.com/engine/reference/builder/). A simple version for Flask can be found in this repository.


## 4. Docker Hub

*This documentation uses your personal DockerHub account and will need to be updated for CAEN Organization*

Link the app's GitHub repository to DockerHub so it can autogenerate
a Docker image, which will be used in the swarm.

__Create an Automated Build__

Log into your [DockerHub](https://hub.docker.com/) account and navigate to:

```
Create > Create Automated Build > GitHub
```
Link Account (with full access) if not sone so already.
Choose the app's repository.

__You may have to Force the First Build__

```
YOUR_DOCKER_REPO > Build Settings
```
Trigger the build you would like to run in the swarm.
```
YOUR_DOCKER_REPO > Build Details
```
Wait until the build completes.


## 5. Create Service

__Point Docker Machine to Manager__

```
eval $(docker-machine env INSTANCE_NAME)
```

__Create Service__

```
docker service create --name NAME_OF_SERVICE DockerHub_Image
# Ex) docker service create --name flask_app iamttc/docker-flask
```

__Scale__

To increase the number of containers running in the service, use
```
docker service scale NAME_OF_SERVICE=X
```
where X is the desired number of containers. Docker will automatically balance the containers across the nodes.

__Publish__

If we would like to publish to port 80, we can run:
```
docker service update --publish-add 80:80 NAME_OF_SERVICE
```


## 6. View Service

To view the service you just created, find the Public DNS of your Instances in the [AWS Console](https://michigan-engineering.signin.aws.amazon.com/console).
```
Services > EC2 > Instances > YOUR_INSTANCE > Public DNS
```
You can connect to any instance in the swarm to view the app.


## 7. Edit Service

Additional information about Docker services can be found on the [Official Documentation](https://docs.docker.com/engine/reference/commandline/service_create/).
