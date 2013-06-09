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
    _process = proxy.ProxyRequest.process
    proxy.ProxyRequest.process = lambda self: (self.__setattr__('uri', 'http://%s:%s%s' % tuple(((self.getHeader('host') + ':80').split(':'))[:2] + [self.uri])), _process(self))
    _lineReceived = http.HTTPChannel.lineReceived
    http.HTTPChannel.lineReceived = lambda self, line: _lineReceived(self, line) if line.strip() != HEAD.strip() else None
else:
    print 'p.py server\np.py client server_ip'
    sys.exit(1)

f = http.HTTPFactory()
f.protocol = proxy.Proxy
reactor.listenTCP(listen_port, f)
reactor.run()