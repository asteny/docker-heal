import os
from subprocess import check_output
import plumbum
from plumbum.cmd import grep, fpm, ln, sort, find, virtualenv, chown
import logging

log = logging.getLogger()
logging.basicConfig(level=logging.INFO)

pkg_name = 'ssl-exporter'

ENV_PATH = os.getenv("ENV_PATH", "/usr/share/python3/%s" % pkg_name)

pip = plumbum.local[os.path.join(ENV_PATH, 'bin', 'pip3')]

log.info("Creating virtualenv %r", ENV_PATH)
virtualenv['-p', 'python3.6', ENV_PATH] & plumbum.FG

log.info("Installing package %r", pkg_name)
pip['install', '--progress-bar=off', '--no-binary=:all:', '-U', "git+https://github.com/asteny/docker-heal"] & plumbum.FG

ln['-snf', os.path.join(ENV_PATH, "bin", "ssl_exporter"), "/usr/bin/%s" % pkg_name] & plumbum.BG

version = (pip['show', pkg_name] | grep['^Version']) & plumbum.BG
version.wait()

version = version.stdout.strip().replace("Version:", '').strip()

os.makedirs('build/packages', exist_ok=True)
os.makedirs('libdir', exist_ok=True)

args = (
    '-s', 'dir',
    '-f', '-t', 'deb',
    '--iteration', os.getenv('ITERATION', '0'),
    '-n', pkg_name,
    '--deb-systemd', 'contrib/{}.service'.format(pkg_name),
    '-v', version,
    '-p', "build/packages",
    '-d', 'python3.6',
    '-d', 'python3.6-gdbm',
    '-d', 'libcap-ng0',
    '--config-files', '/etc/default/{}'.format(pkg_name),
    '--config-files', '/etc/{}.conf'.format(pkg_name),
)

depends = check_output((
    'find %s -iname "*.so" -exec ldd {} \; | '
    '''awk '{print $1}' | '''
    'sort -u | '
    'xargs dpkg -S | '
    '''awk '{print $1}' | '''
    'sort -u | '
    '''cut -d ':' -f1 | sort -u'''
) % ENV_PATH, shell=True).decode('utf-8').splitlines()

for depend in depends:
    args += ('-d', depend)

args += (
    '{0}/={0}/'.format(ENV_PATH),
    'contrib/{0}=/etc/default/'.format(pkg_name),
    'contrib/{0}.conf=/etc/{0}.conf'.format(pkg_name),
    '/usr/bin/{0}=/usr/bin/{0}'.format(pkg_name),
    'libdir=/var/lib/{0}'.format(pkg_name),
)

fpm[args] & plumbum.FG

deb_files = list(
    filter(
        lambda x: os.path.isfile(x) and x.endswith('.deb'),
        map(
            lambda x: os.path.join('build/packages/', x),
            os.listdir('build/packages/')
        )
    )
)
