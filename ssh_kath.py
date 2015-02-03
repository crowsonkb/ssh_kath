#!/usr/bin/env python3

import argparse
import socketserver
import subprocess
import sys
import threading
import time

class State:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            '--user', default='kat', type=str,
            help='the user to log in as')
        parser.add_argument(
            '--host', default='kath.io', type=str,
            help='the host to log in to')
        parser.add_argument(
            '--port', default=22, type=int,
            help='the port number to connect to on the remote host')
        parser.add_argument(
            '--socks-port', default=1080, type=int,
            help='the local port number to open a socks proxy on')
        parser.add_argument(
            '--backchat-port', default=38627, type=int,
            help='the port number to use to stream push notifications back from the server')
        self.args = parser.parse_args()

class SSHCommand:
    def __init__(self):
        self.args = list(self._make_args())

    def _make_args(self):
        ssh_config = {
            'Compression': 'yes',
            'DynamicForward': 'localhost:{}'.format(S.args.socks_port),
            'EscapeChar': 'none',
            'LocalCommand': "echo -en '{}'".format(Titles.escape('connected')),
            'PermitLocalCommand': 'yes',
            'Port': S.args.port,
            'RemoteForward': '{0} localhost:{0}'.format(S.args.backchat_port),
            'RequestTTY': 'force',
            'ServerAliveCountMax': 1,
            'ServerAliveInterval': 3,
            'TCPKeepAlive': 'no',
        }
        yield 'ssh'
        for option in ssh_config.items():
            yield '-o'
            yield '{}={}'.format(*option)
        yield '{}@{}'.format(S.args.user, S.args.host)
        yield 'tmux attach || tmux'

    def connect(self):
        process = subprocess.Popen(self.args, pass_fds=(0, 1, 2))
        process.wait()

class BackchatHandler(socketserver.StreamRequestHandler):
    def handle(self):
        msg = [a.decode() for a in self.rfile.read().split(b'\xfe')]
        if len(msg) == 3:
            args = [
                '/usr/local/bin/terminal-notifier',
                '-sender', 'com.googlecode.iterm2',
                '-title', '{}. {}'.format(msg[0], msg[1]),
                '-message', msg[2]
            ]
            subprocess.call(args)
        else:
            raise RuntimeError()

class BackchatServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class BackchatThread:
    def __init__(self):
        self.server = BackchatServer(('localhost', S.args.backchat_port), BackchatHandler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

class Titles:
    messages = {
        'connected': 'Connected 😃',
        'reconnecting': 'Reconnecting… 😣',
        'starting': 'Making initial connection… 😐',
    }

    @classmethod
    def escape(cls, message_name):
        return '\x1b]2;{}@{}: {}\a'.format(
            S.args.user, S.args.host, cls.messages[message_name])

    @classmethod
    def title(cls, message_name):
        print(cls.escape(message_name), file=sys.stderr)

def main():
    BackchatThread()
    ssh = SSHCommand()
    Titles.title('starting')
    ssh.connect()

    while True:
        Titles.title('reconnecting')
        ssh.connect()
        time.sleep(1)

if __name__ == '__main__':
    S = State()
    main()
