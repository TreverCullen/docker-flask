#!/usr/bin/env python
# Created by Trever Cullen

import sys
import subprocess as sub
import shlex

def run_command(c):
    try:
        result = sub.check_output(shlex.split(c))
        return result
    except (OSError, IOError) as e:
        # no permission
        if e.errno == 13:
            print 'Granting Permission to Shell Script...'
            run_command('chmod +x ' + c[2:c.find(' ')])
            run_command(c)
            return
        return str(e.errno) + ' ' + e.strerror
