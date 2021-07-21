#!/usr/bin/env python3
'''
@作者: 风沐白
@文件: app.py
@描述: 将clash订阅链接转为ss订阅链接
@版本: v0.1
'''

import yaml
import requests
import atexit
import base64
from flask import Flask, request, abort
from urllib import parse

app = Flask(__name__)


@atexit.register
def clean():
    return


@app.route("/", methods=['GET'])
def run():
    key = request.args.get('key')
    with open('key.ini', 'r') as f:
        if key != f.readline().strip():
            abort(403)
    text = main()
    return base64.b64encode(text.encode()).decode()


class SS:
    def __init__(self, proxy: dict) -> None:
        self.name = proxy.get('name')
        self.type = proxy.get('type')
        self.server = proxy.get('server')
        self.port = proxy.get('port')
        self.cipher = proxy.get('cipher')
        self.password = proxy.get('password')
        self.plugin = proxy.get('plugin')
        self.plugin_opts = proxy.get('plugin-opts')
        pass

    def encode(self):
        payload = '{}:{}'.format(self.cipher, self.password)
        payload = base64.b64encode(payload.encode()).decode()
        # ToDo
        plugin = 'obfs-local' if self.plugin == 'obfs' else ''

        obfs = self.plugin_opts.get('mode')
        obfs_host = self.plugin_opts.get('host')
        plugin_text = parse.quote(
            '{};obfs={};obfs-host={}'.format(plugin, obfs, obfs_host))
        name = parse.quote(self.name)
        ssrl = 'ss://{}@{}:{}'.format(payload, self.server, self.port)
        if plugin != None:
            ssrl += '/?plugin='+plugin_text
        if name != None:
            ssrl += '#'+name
        return ssrl


def main():
    url = ''
    with open('url.ini', 'r') as f:
        url = f.readline().strip()
    y = requests.get(url).text
    y = yaml.load(y, Loader=yaml.FullLoader)
    ssrls = []
    for proxy in y['proxies']:
        ss = SS(proxy)
        ssrls.append(ss.encode())
    return '\n'.join(ssrls)


if __name__ == '__main__':
    main()
