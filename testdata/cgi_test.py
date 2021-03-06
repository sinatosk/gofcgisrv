#!/usr/bin/env python2.7

import sys
import argparse

def echo(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    def resp():
        for l in environ['wsgi.input'].readlines():
            yield l

    return resp()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="FastCGI test client application")
    parser.add_argument('--host', type=str, help='Hostname to listen on')
    parser.add_argument('--port', type=int, help='Port to listen on')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--fcgi', action="store_true", help='Run as a FastCGI server')
    group.add_argument('--cgi', action="store_true", help='Run as a CGI server')
    group.add_argument('--scgi', action="store_true", help='Run as an SCGI server')
    args = parser.parse_args()

    if args.host and args.port:
	kwargs = {'bindAddress' : (args.host, args.port) }
    else:
        kwargs = {}
    if args.cgi:
        import flup.server.cgi as cgimod
        kwargs = {}
    elif args.scgi:
        import flup.server.scgi as cgimod
    else:
        import flup.server.fcgi as cgimod

    WSGIServer = cgimod.WSGIServer

    result = WSGIServer(echo, **kwargs).run()

