import subprocess
import datetime
import os
import sys

os.environ['GOPATH'] = os.getcwd()


def println_call(cmd):
    pre = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    print(pre, cmd)
    r = subprocess.call(cmd, shell=True)
    if r != 0:
        sys.exit(r)


def install_geth():
    println_call('go install github.com/ethereum/go-ethereum/cmd/geth')


def install_istanbul():
    println_call('go install github.com/getamis/istanbul-tools/cmd/istanbul')


def install():
    install_geth()
    install_istanbul()


def main():
    install()


if __name__ == '__main__':
    main()
