import sys
from twisted.web import http, proxy
from twisted.internet import reactor

HEAD = 'fuck fangbinxing\r\n'
if 'client' in sys.argv:
    listen_port = 8080
    _connectTCP = reactor.connectTCP
    reactor.connectTCP = lambda host, p, factory: _connectTCP(sys.argv[2], 1984, factory)  # redirect to our server
    _sendCommand = http.HTTPClient.sendCommand
    http.HTTPClient.sendCommand = lambda self, command, path: _sendCommand(self, HEAD + command, path)  # prepend something
elif 'server' in sys.argv:
    listen_port = 1984

    # def process_(self):
    #     headers = self.getAllHeaders().copy()
    #     parsed = headers['host'].split(':')
    #     self.content.seek(0, 0)
    #     clientFactory = proxy.ProxyClientFactory(self.method, self.uri, self.clientproto, headers, self.content.read(), self)
    #     self.reactor.connectTCP(parsed[0], 80 if len(parsed) == 1 else int(parsed(1)), clientFactory)

    def process_(self):
        self.uri = 'http://%s:%s%s' % tuple(((self.getHeader('host') + ':80').split(':'))[:2] + [self.uri])
        _process(self)

    _process = proxy.ProxyRequest.process
    proxy.ProxyRequest.process = process_
    _lineReceived = http.HTTPChannel.lineReceived
    http.HTTPChannel.lineReceived = lambda self, line: _lineReceived(self, line) if line.strip() != HEAD.strip() else None
else:
    print 'p.py server\np.py client server_ip'
    sys.exit(1)

f = http.HTTPFactory()
f.protocol = proxy.Proxy
reactor.listenTCP(listen_port, f)
reactor.run()