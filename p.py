import sys
from twisted.web import http, proxy
from twisted.internet import reactor

HEAD = 'fuck fangbinxing\r\n'
if 'client' in sys.argv:
    listen_port = 8080
    _connectTCP = reactor.connectTCP

    def connectTCP_(host, p, factory):
        _connectTCP(sys.argv[2], 1984, factory)

    reactor.connectTCP = connectTCP_

    def _sendCommand(self, command, path):
        # self.transport.writeSequence(HEAD)
        self.sendCommand_(command, path)

    http.HTTPClient.sendCommand_ = http.HTTPClient.sendCommand
    http.HTTPClient.sendCommand = _sendCommand
elif 'server' in sys.argv:
    listen_port = 1984
    def process_(self):
        headers = self.getAllHeaders().copy()
        parsed = headers['host'].split(':')
        host = parsed[0]
        port = 80 if len(parsed) == 1 else int(parsed(1))
        self.content.seek(len(HEAD), 0)
        clientFactory = proxy.ProxyClientFactory(self.method, self.uri,
                                                 self.clientproto, headers,
                                                 self.content.read(), self)
        self.reactor.connectTCP(host, port, clientFactory)

    def _lineReceived(self, line):
        print line
        if line.strip() == HEAD.strip():
            return
        else:
            http.HTTPChannel.lineReceived_(self, line)

    proxy.ProxyRequest.process = process_
    http.HTTPChannel.lineReceived_ = http.HTTPChannel.lineReceived
    http.HTTPChannel.lineReceived = _lineReceived
else:
    print 'p.py client/server [server_ip]'
    sys.exit(1)

f = http.HTTPFactory()
f.protocol = proxy.Proxy
reactor.listenTCP(listen_port, f)
reactor.run()