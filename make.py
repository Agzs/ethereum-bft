import contextlib
import datetime
import os
import shutil
import subprocess
import sys
import json

os.environ['GOPATH'] = os.getcwd()


def call(cmd):
    pre = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    print(pre, cmd)
    r = subprocess.call(cmd, shell=True)
    if r != 0:
        sys.exit(r)


@contextlib.contextmanager
def chdir(path):
    cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cwd)


def install_geth():
    call('go install github.com/ethereum/go-ethereum/cmd/geth')


def install_istanbul():
    call('go install github.com/getamis/istanbul-tools/cmd/istanbul')


def install():
    install_istanbul()
    install_geth()


istanbul = os.path.abspath(os.path.join('bin', 'istanbul'))
geth = os.path.abspath(os.path.join('bin', 'geth'))
if os.name == 'nt':
    istanbul += '.exe'
    geth += '.exe'


def init():
    shutil.rmtree('eth/0', ignore_errors=True)
    shutil.rmtree('eth/1', ignore_errors=True)
    shutil.rmtree('eth/genesis.json', ignore_errors=True)
    shutil.rmtree('eth/static-nodes.json', ignore_errors=True)
    with chdir('eth'):
        call(f'{istanbul} setup --num 2 --nodes --verbose --save')
        call(f'{geth} --datadir 0 init genesis.json')
        call(f'{geth} --datadir 1 init genesis.json')
        with open('0/password', 'w') as f:
            pass
        with open('1/password', 'w') as f:
            pass
        call(f'{geth} --datadir 0 account import 0/nodekey --password 0/password')
        call(f'{geth} --datadir 1 account import 1/nodekey --password 1/password')


def run0():
    with chdir('eth'):
        call(f'{geth} --datadir 0 --mine --minerthreads 1 --syncmode "full" \
            --networkid 2017 --port 2000 --istanbul.blockperiod 10 console 2>/tmp/node0.log')


def run1():
    with chdir('eth'):
        with open('static-nodes.json') as f:
            data = json.load(f)
        bootnodes0 = data[0]
        bootnodes0 = bootnodes0.replace('@0.0.0.0:30303?discport=0', '@127.0.0.1:2000')
        if os.name == 'nt':
            call(f'{geth} --ipcdisable --datadir 1 --mine --minerthreads 1 ' +
                 '--syncmode "full" --networkid 2017 --port 2001 --istanbul.blockperiod 10 ' +
                 f'--bootnodes={bootnodes0} console 2>/tmp/node1.log')
        else:
            call(f'{geth} --datadir 1 --mine --minerthreads 1 --syncmode "full" ' +
                 '--networkid 2017 --port 2001 --istanbul.blockperiod 10 ' +
                 f'--bootnodes={bootnodes0} console 2>/tmp/node1.log')


def main():
    install()


if __name__ == '__main__':
    main()
