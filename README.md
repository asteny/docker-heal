[![Deb build Status](https://travis-ci.org/asteny/docker-heal.svg?branch=master)](https://travis-ci.org/asteny/docker-heal)[![Download](https://api.bintray.com/packages/asten/heal-docker/docker-heal/images/download.svg)](https://bintray.com/asten/heal-docker/docker-heal/_latestVersion)


Docker heal
===========

Tool for restart docker container if [health check failed](https://docs.docker.com/engine/reference/builder/#healthcheck) 

To use docker-heal you need:
- build container or up [docker-compose with health check](https://docs.docker.com/compose/compose-file/#healthcheck)
- build container with label (default is 'autoheal', but you could write you own) or use flag ```-l all``` for healing all containers (but they all should have health check)
 
Code of this repo is a python version of [willfarrell/docker-autoheal](https://github.com/willfarrell/docker-autoheal) 

INSTALLATION
------------

pip
---
```bash
pip install git+https://github.com/asteny/docker-heal
```

Deb package for Ubuntu (16.04 - 18.04)
--------------------------------------

```bash
apt-get update
apt-get install gnupg2 apt-transport-https ca-certificates -y
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 379CE192D401AB61
echo "deb https://dl.bintray.com/asten/heal-docker xenial main" | tee -a /etc/apt/sources.list.d/heal-docker.list
apt-get update
apt-get install docker-heal -y

```

Docker
------


```bash
docker pull asteny/docker-heal

```

USAGE
=====

Deb package
------
Default config in /etc/docker-heal.conf

```bash
systemctl enable docker-heal
systemctl start docker-heal

```

Docker compose
--------------

```bash
version: "3"

services:
  docker-heal:
    image: asteny/docker-heal
    restart: always
    environment:
      APP_LABEL: autoheal
      APP_START_TIME: 20
      APP_CHECK_INTERVAL: 30
      APP_LOG_LEVEL: debug
      APP_LOG_FORMAT: color
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
```
