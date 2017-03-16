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
    manager = ''
    nodes = []
    join = ''

    # this is documented by docker
    port = '2377'

    # init the swarm
    def help_init(self):
        print 'init <node>'
        print '-- shortcut: i'
        print '-- initializes a swarm with manager <node>'
    def do_init(self, node):
        if node:
            self.manager = node
            self.nodes.append(node)
            c = './init.sh ' + self.manager
            result = run_command(c)
            print result
            self.join = result[result.find('docker swarm join'):result.find(self.port) + 4]
        else:
            self.help_init()
    do_i = do_init

    # add a node to the swarm
    def help_join(self):
        print 'add <node> <node> ...'
        print '-- shortcut: a'
        print '-- adds each space separated <node> to the swarm'
        print '-- must run <init> before running <add>'
    def do_join(self, args):
        if args and self.manager != '':
            for n in args.split():
                if n not in self.nodes:
                    self.nodes.append(n)
                    c = './join.sh ' + n + ' "' + self.join + '"'
                    result = run_command(c)
                else:
                    result = n + ' already in swarm... continuing'
                print result
        else:
            self.help_init()
    do_j = do_join

    # remove node from swarm
    def help_leave(self):
        print 'leave <node> <node> ...'
        print '-- shortcut: l'
        print '-- removes <node> from the swarm'
    def do_leave(self, args):
        if args:
            for n in args.split():
                if n == self.manager:
                    print 'This is the manager. The entire swarm will be deleted.'
                    res = raw_input('Are you sure (y/n): ')
                    if res.lower() == 'y':
                        c = './leave.sh ' + n
                        result = run_command(c)
                elif n in self.nodes:
                    c = './leave.sh ' + n
                    result = run_command(c)
                else:
                    result = n + ' not in swarm... continuing'
                print result
        else:
            self.help_leave()
    do_l = do_leave

    # obtain information from manager node
    def help_fetch(self):
        print 'fetch <node>'
        print '-- shortcut: f'
        print '-- fetches data from manager <node>'
    def do_fetch(self, node):
        if node:
            c = './fetch.sh ' + node
            result = ''
            try:
                result = run_command(c)
            except:
                return
            self.manager = node
            self.join = result[result.find('docker swarm join'):result.find(self.port) + 4]
            data = result[:result.find('To add a worker')].split('\n')[1:-1]
            for temp in data:
                d = temp.split()
                if d[1].find('*') == -1:
                    self.nodes.append(d[1])
                else:
                    self.nodes.append(d[2])
            self.do_status(self.manager)
        else:
            self.help_fetch()
    do_f = do_fetch


    # swarm status
    def help_status(self):
        print 'status'
        print '-- shortcut: s'
        print '-- display the status of the swarm'
    def do_status(self, args):
        if self.manager == '':
            print 'No Swarm Selected'
            print 'Use <fetch> or <init>'
        else:
            print 'Manager: ' + self.manager
            print 'Nodes: ' + ', '.join(self.nodes)
            print 'Join Command: ' + self.join
    do_s = do_status


    # show docker machines
    def help_show(self):
        print 'show'
        print '-- shows all docker machines'
    def do_show(self, args):
        print run_command('docker-machine ls')


    # end command loop
    def help_quit(self):
        print 'quit'
        print '-- shortcut: q'
        print '-- ends application'
    def do_quit(self, args):
        print 'bye'
        return True
    do_q = do_quit


    # hide undocumented commands (shortcuts)
    undoc_header = None
    def print_topics(self, header, cmds, cmdlen, maxcol):
        if header is not None:
            if cmds:
                self.stdout.write("%s\n"%str(header))
                if self.ruler:
                    self.stdout.write("%s\n"%str(self.ruler * len(header)))
                self.columnize(cmds, maxcol-1)
                self.stdout.write("\n")


if __name__ == '__main__':
    Command().cmdloop()


