import os
import sys

import fabric.api

import make

fabric.api.env.use_ssh_config = True
fabric.api.env.hosts = ['10.0.5.50:65422', '10.0.5.51:65422', '10.0.5.52:65422', '10.0.5.53:65422']
fabric.api.env.user = 'root'

if sys.argv[1] == 'deploy':
    make.install()
    make.server_init()
    os.chdir('..')
    fabric.api.local('python3 -m zipfile -c /tmp/ethereum-bft.zip ethereum-bft')
    os.chdir('ethereum-bft')


def deploy():
    fabric.api.run('rm -rf /src/ethereum-bft')
    fabric.api.put('/tmp/ethereum-bft.zip', '/tmp/ethereum-bft.zip')
    fabric.api.run('python3 -m zipfile -e /tmp/ethereum-bft.zip /src/')
    with fabric.api.cd('/src/ethereum-bft'):
        fabric.api.run('python3 -m make install')
    fabric.api.run('killall -q geth', warn_only=True)


def stop():
    fabric.api.run('killall -q geth', warn_only=True)
