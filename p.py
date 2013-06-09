import sys
from twisted.web import http, proxy
from twisted.internet import reactor

HEAD = 'Fuck GFW\x01\r\n'
f = http.HTTPFactory()
f.protocol = proxy.Proxy
if 'client' in sys.argv:
    _connectTCP = reactor.connectTCP
    reactor.connectTCP = lambda host, p, factory: _connectTCP(sys.argv[2], 1984, factory)  # redirect to our server
    _sendCommand = http.HTTPClient.sendCommand
    http.HTTPClient.sendCommand = lambda self, command, path: _sendCommand(self, HEAD + command, path)  # prepend HEAD
    reactor.listenTCP(8080, f)
elif 'server' in sys.argv:
    _process = proxy.ProxyRequest.process
    proxy.ProxyRequest.process = lambda self: (setattr(self, 'uri', 'http://%s:%s%s' % tuple(((self.getHeader('host') + ':80').split(':'))[:2] + [self.uri])), _process(self))  # replace rel path with abs path
    _lineReceived = http.HTTPChannel.lineReceived
    http.HTTPChannel.lineReceived = lambda self, line: self.f(self, line) if line.strip() != HEAD.strip() else setattr(self, 'f', _lineReceived)  # remove HEAD
    reactor.listenTCP(1984, f)
else:
    print 'p.py server\np.py client server_ip'
    sys.exit(1)
reactor.run()