#!/usr/bin/env python
import argparse

import os.path
import os
from bottle import route, run, static_file, template

parser = argparse.ArgumentParser()
parser.add_argument('path', help='path to serve files from', default='./', nargs='?')
parser.add_argument('port', help='port server will listen on', default=8888, type=int, nargs='?')
args = parser.parse_args()

@route('/favicon.ico')
def blackhole():
    return None

def server(file):
    if os.path.isdir(os.path.join(args.path, file)):
        if os.path.exists(os.path.join(args.path, file, 'index.html')):
            file = os.path.join(file, 'index.html')
        else:
            return '<html><body><h1>/{0}</h1><ul>{1}</ul></body></html>'.format(file, ''.join(['<li><a href="/{0}">{1}</a></li>'.format(os.path.join(file, path), path) for path in os.listdir(os.path.join(args.path, file))]))
    return static_file(file, root=args.path)

@route('/')
def server_index():
    return server('')

@route('/<file:path>')
def server_path(file):
    return server(file)


print 'Starting serving from "{1}" on http://localhost:{0}'.format(args.port, args.path)
run(server='tornado', host='localhost', port=args.port, quiet=True)