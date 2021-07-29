# encoding: utf-8
from __future__ import absolute_import, print_function

from setuptools import setup, find_packages

__version__ = '0.0.3'
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
        'ConfigArgParse==1.5.1',
        'docker==5.0.0',
        'prettylog==0.3.0',
        'python-dateutil==2.8.2',
        'six==1.16.0',
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
