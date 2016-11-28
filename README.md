# CAEN Docker Flask App

Flask app used to test and standardize deployments to AWS using Docker.


## Requirements

* [AWS CLI](https://aws.amazon.com/cli/)
* [Docker Engine](https://docs.docker.com/engine/installation/)


## Deployment

All deployment instructions will be documented below. This is designed to
standardize deployments. If you would like to make changes to this process,
please create a pull request.


### AWS Virtual Machines

Our apps will be running on Ubuntu (Currently 15.10) VMs in AWS.

1. Edit aws-dm Credentials
	* ID and Key usually found in *~/.aws/credentials*
	* __This file is not yet included, pending approval. If needed
	immediately, contact tknox@umich.edu__

2. Run aws-dm Following Prompts

3. Repeat Step 2 for the number of VMs you would like to be in you Docker Swarm


### Docker Swarm

1. Find IP of Host VM
	1. [Log into UMich AWS Console](https://michigan-engineering.signin.aws.amazon.com/console)
	2. Find Private IP
		* Services -> EC2 -> Instances -> YOUR_INSTANCE -> Private IP
	3. Note: you can also find the Private IP through SSH
		1. `ssh -i /PATH/TO/KEY ubuntu@PUBLIC_DNS`
			* Key Pair is usually located in `~/.docker/machine/machines/INSTANCE_NAME/id_rsa`
		2. `ifconfig -a`
		3. eth0 -> inet addr
		* [Official Documentation](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html)

2. Point Docker Machine to Manager
	* `eval $(docker-machine env INSTANCE_NAME)`

3. Initiate Docker Swarm
	1. `docker swarm -init --advertise-addr PRIVATE_IP:2377`
	2. Copy the JOIN command
		* `docker swarm join --token LONG_TOKEN_STRING PRIVATE_IP:2377`

4. Join Workers
	1. Point your Docker Machine to a worker VM
	2. Run the JOIN command
	3. Repeat with other worker VMs

5. Check Status
	1. Switch back to Manager
	2. Run `docker node ls`
	3. Check if all manager and worker nodes are present


### Dockerize Flask App

1. Create a Dockerfile
	* Simple Flask example can be found in this repository
	* [Official Documentation](https://docs.docker.com/engine/reference/builder/)


### Docker Image
