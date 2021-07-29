FROM snakepacker/python:all as builder

RUN python3.7 -m venv /usr/share/python3/app

RUN /usr/share/python3/app/bin/pip install -U git+https://github.com/asteny/docker-heal

RUN find-libdeps /usr/share/python3/app > /usr/share/python3/app/pkgdeps.txt

#################################################################
FROM snakepacker/python:3.7

COPY --from=builder /usr/share/python3/app /usr/share/python3/app

RUN ln -snf /usr/share/python3/app/bin/docker_heal /usr/bin/docker_heal

CMD ["/usr/bin/docker_heal"]
