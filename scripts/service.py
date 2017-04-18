#!/usr/bin/env python
# Created by Trever Cullen
# Create a docker sservice on an aws swarm

from extensions import *


class Service:

    def __init__(self):
        self.manager = None
        self.host = None
        self.name = None
        self.image = None
        self.version = None

        # used to call functions from arguments
        self.call = {
            'create':       self.create,
            'c':            self.create
        }


    def help_all(self):
        print 'service commands'
        print '-- create'
        print 'run \'service <command>\' for help'


    def help_create(self):
        print 'create <aws|docker> <name> <image> <version>'
        print '-- shortcut: c'
        print '-- create a service on the current swarm'
    def create(self, args):
        args = args.split()
        if len(args) == 4:
            self.host = args[0]
            self.name = args[1]
            self.image = args[2]
            self.version = args[3]
            c = '\"docker service create '
            if args[0] == 'aws':
                c += '--with-registry-auth '
            c += '--name {} {}:{}\"'.format(self.name, self.image, self.version)
            result = run_command(c)
            print result
        else:
            self.help_create()


        def help_remove(self):
            print 'remove <name>'
            print '-- shortcut: rm'
            print '-- removes service from swarm'
        def remove(self, args):
            args = args.split()
            if len(args) == 1:
                c = '\"docker service rm %s\"' % args[0]
                result = run_command('./script.sh ' + c)
                print result
            else:
                self.help_remove()

    # reset variables
    def reset(self):
        self.manager = None
        self.host = None
        self.name = None
        self.image = None
        self.version = None



