#!/usr/bin/env python
# Created by Trever Cullen
# Create a docker swarm on aws from pre-existing instances

import cmd
from extensions import *


class Command(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '\n> '
        print 'Docker Swarm and Service Creator'

    # variables
    host = ''
    nodes = []
    ip = '184.72.90.87'
    join = 'docker swarm join --token LONG_TOKEN_STRING PRIVATE_IP:2377'

    # init the swarm
    def help_init(self):
        print 'init <node>'
        print '-- initializes a swarm with manager <node>'
    def do_init(self, node):
        if node:
            self.host = node
            c = './init.sh ' + self.host + ' ' + self.ip
            result = run_command(c)
            self.join = result
        else:
            self.help_init()
    do_i = do_init

    # add a node to the swarm
    def help_add(self):
        print 'add <node> <node> ...'
        print '-- adds each space separated <node> to the swarm'
        print '-- must run <init> before running <add>'
    def do_add(self, nodes):
        if nodes and self.join != 'Error':
            for n in nodes.split():
                c = './add.sh ' + n + ' "' + self.join + '"'
                result = run_command(c)
                print result
        else:
            self.help_init()
    do_a = do_add

    # end command loop
    def help_quit(self):
        print 'quit'
        print '-- ends application'
    def do_quit(self, args):
        print 'bye'
        return True
    do_q = do_quit


if __name__ == '__main__':
    Command().cmdloop()


