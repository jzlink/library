#!/usr/bin/env python

import yaml

import config

class Columns(object):

    def __init__(self):
        self.conf = config.getInstance()
        filename = '%s/conf/columns.yml' % self.conf['basedir']
        self.columns = yaml.load(open(filename, 'r'))
        
