FROM 		ubuntu:15.10
MAINTAINER 	Trever Cullen "iamttc@umich.edu"

COPY 		. /app
WORKDIR 	/app
RUN 		pip install -r requirements.txt

ENTRYPOINT 	["python"]
CMD 		["app.py"]
