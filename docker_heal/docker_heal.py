import logging
import os
import time
from datetime import datetime

import docker
from configargparse import ArgumentParser
from prettylog import basic_config

parser = ArgumentParser(default_config_files=[
    os.path.join('/etc/docker-heal.conf'),
], auto_env_var_prefix='APP_')

parser.add_argument(
    '-l',
    '--label',
    type=str,
    default='autoheal',
    help='container label'
)
parser.add_argument(
    '-s', '--start-time',
    type=int,
    default=20,
    help='time for first container up'
)
parser.add_argument(
    '-c',
    '--check-interval',
    type=int,
    default=30,
    help='check every seconds'
)

parser.add_argument(
    '-L', '--log-level', help='Log level',
    default='info',
    choices=(
        'critical', 'fatal', 'error', 'warning',
        'warn', 'info', 'debug', 'notset'
    ),
)
parser.add_argument('--log-format', type=str, default="color")

arguments = parser.parse_args()

log = logging.getLogger()


def validate_check_after_start_time(start_time_seconds, start_at):
    start_at_time = datetime.strptime(start_at[0:-2], '%Y-%m-%dT%H:%M:%S.%f')
    delta = datetime.utcnow() - start_at_time
    return delta.seconds > start_time_seconds


def get_container_info(container_inspect):
    health = container_inspect.get(
        'State', {}
    ).get(
        'Health', {}
    ).get(
        'Status', {}
    )

    start_at = container_inspect.get(
        'State', {}
    ).get(
        'StartedAt', {}
    )
    return health, start_at


def need_heal(health, start_at):
    return all(
        (health == 'unhealthy',
         validate_check_after_start_time(arguments.start_time, start_at))
    )


def container_restart(container):
    try:
        client.restart(container)
    except Exception:
        log.exception("Can't restart docker")


def main(client):
    for container in client.containers(filters={'label': arguments.label}):
        container_inspect_info = client.inspect_container(container['Id'])
        health, start_at = get_container_info(container_inspect_info)
        if need_heal(health, start_at):
            log.warning('Healing ' + (' '.join(container['Names'])))
            container_restart(container)
        else:
            log.exception((' '.join(
                container['Names']) + ' has label, but has no health check'))


if __name__ == "__main__":
    client = docker.APIClient(base_url='unix://var/run/docker.sock')
    basic_config(
        level=arguments.log_level.upper(),
        buffered=False,
        log_format=arguments.log_format
    )
    while True:
        main(client)
        time.sleep(arguments.check_interval)
