#!/usr/bin/env python
# Created by Trever Cullen
# Create a docker sservice on an aws swarm

from extensions import *


class Service:

    def __init__(self):
        self.data = None    

        # used to call functions from arguments
        self.call = {
            'create':       self.create
        }


    def help_all(self):
        print 'service commands'
        print '-- create'
        print 'run \'service <command>\' for help'


    def create(self, args):
        print args

    # reset variables
    def reset(self):
        self.data = None



