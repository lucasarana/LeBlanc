# -*- coding: utf-8 -*-
import os
import sys
import getopt

from os.path import abspath
sys.path.insert(0, os.path.split(abspath(__file__))[0])
sys.path.insert(1, os.path.split(sys.path[0])[0])

import signal
import traceback
import tornado.httpserver
import tornado.ioloop
import tornado.iostream
import tornado.web
import tornado.gen
import tornado.httpclient

import config

import NaixCommon.simplejson
import NaixCommon.Errors

from NaixCommon.ValueObjects import VO_Message
from NaixCommon.Environment import Environment
from NaixCommon.NaixLogger import NaixLogger

from LeBlancService import LeBlancServices

def sighup():
    NaixLogger().info('HUP signal received')
    reload(config)

class LeBlancHandler(tornado.web.RequestHandler):

    def get(self, func, *args, **kwargs):
        Environment().reset()
        NaixLogger().info(">>> %s Request >>> (%s): %s%s" % (self.request.method, self.request.remote_ip, self.request.uri if len(self.request.uri) > 1 else '', self.request.body))

        try:
            responseBody = str(getattr(LeBlancServices, func)(self))

        except VO_Message, expected:
            NaixLogger().error(traceback.format_exc())
            responseBody = NaixCommon.simplejson.dumps(expected.getSerializableDict(), use_decimal=True)

        except:
            NaixLogger().error(traceback.format_exc())
            exception = NaixCommon.Errors.INTERNAL_SERVER_ERROR()
            responseBody = NaixCommon.simplejson.dumps(exception.getSerializableDict(), use_decimal=True)

        NaixLogger().info("<<< %s Response <<< (%s): %s" % (self.request.method, self.request.remote_ip, responseBody))
        self.write(responseBody)
        self.finish()

    post = get

if __name__ == '__main__':

    args = {'-p':config.port}
    options, operands = getopt.getopt(sys.argv[1:], 'p:s')
    args.update(dict(options))

    if operands:
        args['-p'] = operands[0]

    for arg in ('-p',):
        if arg in args:
            args[arg] = int(args[arg])

    NaixLogger().info('Starting LeBlancdinger at port %d' % args['-p'])

    app = tornado.web.Application([
        (r'/favicon.ico', tornado.web.ErrorHandler, dict(status_code=404)),
        (r'/(.*)', LeBlancHandler),
    ], debug = True)

    if '-s' in args:
        server = tornado.httpserver.HTTPServer(app, xheaders=True, ssl_options=config.ssl_options)
        NaixLogger().info('SSL Enabled')
    else:
        server = tornado.httpserver.HTTPServer(app, xheaders=True)

    server.bind(args['-p'], address=config.listenAddress)
    server.start(config.processes)

    #signal.signal(signal.SIGHUP, lambda sig, frame: tornado.ioloop.IOLoop.instance().add_callback_from_signal(sighup))

    tornado.ioloop.IOLoop.instance().start()