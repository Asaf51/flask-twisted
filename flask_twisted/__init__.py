import sys
from twisted.python import log
from twisted.internet import reactor, ssl
from twisted.web.server import Site
from twisted.web.wsgi import WSGIResource
from .resource import WSGIRootResource
from observable import Observable
import OpenSSL


class Twisted(Observable):
    def __init__(self, app=None, ssl=False, ssl_cert=None, ssl_pem=None):
        Observable.__init__(self)
        self.app = None
        self.resources = {}

        if app is not None:
            self.init_app(app)

        if ssl and ssl_cert and ssl_pem:
            self.ssl = True
            self.ssl_cert = ssl_cert
            self.ssl_pem = ssl_pem

    def init_app(self, app):
        self.app = app
        app.run = self.run

    def add_resource(self, name, resource):
        self.resources[name] = resource

    def create_site(self, resource, **options):
        return Site(resource)

    def get_certificate(self):
        ssl_context = ssl.DefaultOpenSSLContextFactory(
            self.ssl_pem,
            self.ssl_cert,
        )

        return ssl_context

    def run_simple(self, app, host, port, **options):
        self.trigger('run', app)

        if app.debug:
            log.startLogging(sys.stdout)

        resource = WSGIResource(reactor, reactor.getThreadPool(), app)
        site = self.create_site(
            WSGIRootResource(resource, self.resources), **options)

        reactor.listenTCP(int(port), site, interface=host)

        if 'run_reactor' in options and options['run_reactor'] is False:
            pass
        else:
            reactor.run()

    def run_ssl(self, app, host, port, **options):
        self.trigger('run', app)

        if app.debug:
            log.startLogging(sys.stdout)

        resource = WSGIResource(reactor, reactor.getThreadPool(), app)
        site = self.create_site(
            WSGIRootResource(resource, self.resources), **options)

        try:
            certificate = self.get_certificate()
        except OpenSSL.SSL.Error:
            raise IOError(
                "Invalid / Not Exists certificate files")

        reactor.listenSSL(
            int(port),
            site,
            interface=host,
            contextFactory=certificate)

        if 'run_reactor' in options and options['run_reactor'] is False:
            pass
        else:
            reactor.run()

    def run(self, host=None, port=None, debug=None, **options):
        app = self.app
        if app is None and 'app' in options:
            app = options['app']
        if app is None:
            raise Exception('"app" not defined')

        if host is None:
            host = '127.0.0.1'

        if port is None:
            server_name = app.config['SERVER_NAME']
            if server_name and ':' in server_name:
                port = int(server_name.rsplit(':', 1)[1])
            else:
                port = 5000

        if debug is not None:
            app.debug = bool(debug)

        if self.ssl:
            self.run_ssl(app, host, port, **options)
        else:
            self.run_simple(app, host, port, **options)
