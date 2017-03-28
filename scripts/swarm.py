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
    manager = None
    join = None
    nodes = []

    # this is documented by docker
    port = '2377'

    # init the swarm
    def help_init(self):
        print 'init <node>'
        print '-- shortcut: i'
        print '-- initializes a swarm with manager <node>'
    def do_init(self, node):
        if node:
            self.reset()
            self.manager = node
            self.nodes.append(node)
            c = './init.sh ' + self.manager
            result = run_command(c)
            print result
            self.join = format_join(result, self.port)
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
        if args:
            # must init swarm first
            if self.manager == None:
                print 'No Manager, use <init>'
                return
            # join nodes to swarm
            for n in args.split():
                if n not in self.nodes:
                    c = './join.sh {} "{}"'.format(n, self.join)
                    result = run_command(c)
                    self.nodes.append(n)
                else:
                    result = '%s already in swarm... continuing' % n
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
                result = None
                # remove manager ending swarm
                if n == self.manager and len(self.nodes) == 1:
                    c = './leave.sh %s' % n
                    result = run_command(c)
                    self.reset()
                # don't remove manager until all others removed
                elif n == self.manager:
                    result = 'This is the manager. Please delete all other nodes first.'
                # remove node, update manager list
                elif n in self.nodes:
                    commands = ['./leave.sh %s' % n, './rm.sh {} {}'.format(self.manager, n)]
                    result = run_command(commands[0])
                    run_command(commands[1])
                    nodes.remove(n)
                else:
                    result = '%s not in swarm... continuing' % n
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
            # clear other swarm if there
            self.reset()
            c = './fetch.sh %s' % node
            result = None
            try:
                result = run_command(c)
            except:
                return
            # parse data
            self.manager = node
            self.join = format_join(result, self.port)
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
        if not self.manager:
            print 'No Swarm Selected'
            print 'Use <fetch> or <init>'
        else:
            self.nodes.sort()
            print 'Manager: ' + self.manager
            print 'Nodes: ' + ', '.join(self.nodes)
            # print 'Join Command: ' + self.join # don't really need to show this
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


    # reset variables
    def reset(self):
        self.manager = None
        self.nodes = []
        self.join = None


    # send a raw command
    # TODO
    def do_raw(self, args):
        result = run_command(args)
        print result


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


