FROM ubuntu:18.04
MAINTAINER luke_park "lukepark327@gmail.com"
RUN apt-get update -y
RUN apt-get install -y build-essential
RUN apt-get install -y --no-install-recommends python3.6 python3.6-dev python3-pip python3-setuptools python3-wheel gcc
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
WORKDIR ./example/server
CMD python3.6 app.py