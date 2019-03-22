# encoding: utf-8
from __future__ import absolute_import, print_function

from setuptools import setup, find_packages

__version__ = '0.0.1'
__author__ = 'Pavel Sofrony <pavel@sofrony.ru>'

setup(
    name='docker-heal',
    version=__version__,
    author=__author__,
    author_email='pavel@sofrony.ru',
    license="MIT",
    description="Tool for restart docker container if health check failed",
    platforms="all",
    packages=find_packages(),
    install_requires=(
        'certifi==2018.11.29',
        'chardet==3.0.4',
        'colorlog==4.0.2',
        'ConfigArgParse==0.14.0',
        'docker==3.7.0',
        'docker-pycreds==0.4.0',
        'fast-json==0.3.2',
        'idna==2.8',
        'prettylog==0.2.0',
        'requests==2.21.0',
        'six==1.12.0',
        'ujson==1.35',
        'urllib3==1.24.1',
        'websocket-client==0.55.0',
    ),
    entry_points={
        'console_scripts': [
            'docker_heal = docker_heal.docker_heal:main',
        ],
    },
    extras_require={
        ':python_version <= "3.7.3"': 'typing >= 3.5.2',
    },
)
