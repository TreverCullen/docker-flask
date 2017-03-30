#!/usr/bin/env python
# Created by Trever Cullen
# Create a docker swarm on aws from pre-existing instances

import cmd
from swarm import *
from service import *
from extensions import *


class Command(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = '\n> '
        print 'Docker Swarm and Service Creator'
        self.swarm = Swarm()
        self.service = Service()

    # call swarm functions
    def do_swarm(self, args):
        args = args.split()
        try:
            self.swarm.call[args[0]](''.join(args[1:]))
        except:
            self.swarm.help_all()
    do_sw = do_swarm

    # call service functions
    def do_service(self, args):
        args = args.split()
        try:
            self.service.call[args[0]](''.join(args[1:]))
        except:
            self.service.help_all()
    do_se = do_service

    # show docker machines
    def help_machines(self):
        print 'show'
        print '-- shows all docker machines'
    def do_machines(self, args):
        print run_command('docker-machine ls')
    do_m = do_machines

    # send a raw command
    # TODO
    def do_raw(self, args):
        result = run_command(args)
        print result

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


