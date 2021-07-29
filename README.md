![build](https://github.com/asteny/docker-heal/actions/workflows/build.yml/badge.svg)

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
pip install -U git+https://github.com/asteny/docker-heal
```

Deb package for Ubuntu
--------------------------------------

```bash
apt-get update
apt-get install gnupg2 apt-transport-https ca-certificates -y
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys DA05A43C4C8E9F8B
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys A57ED69D49D1012A
printf "deb https://packagecloud.io/the_asten/docker-heal/ubuntu/ focal main \ndeb-src https://packagecloud.io/the_asten/docker-heal
/ubuntu/ focal main" | tee -a /etc/apt/sources.list.d/docker-heal.list 
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
