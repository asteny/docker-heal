FROM ubuntu:xenial

RUN apt-get update && \
    apt-get install gnupg2 apt-transport-https ca-certificates -y && \
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 379CE192D401AB61 && \
    echo "deb https://dl.bintray.com/asten/heal-docker xenial main" | tee -a /etc/apt/sources.list.d/heal-docker.list && \
    apt-get update && \
    apt-get install docker-heal -y && \
    apt-get purge -y gnupg2 && \
    apt-get autoremove -y && \
    rm -fr /var/lib/apt/lists/*

CMD ["/usr/bin/docker-heal"]
