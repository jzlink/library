#!/usr/bin/env python
import yaml
from pprint import pprint

import config

class LoadYaml(object):

    def __init__(self):
        self.conf = config.getInstance()

    def loadYaml(self, name):
        filename = '%s/conf/%s.yml' % (self.conf['basedir'], name)
        dictionary  = yaml.load(open(filename, 'r'))
        return dictionary

#test
def test():  
    test = LoadYaml()
    columns = test.loadYaml('columns')
    pprint(columns)

if __name__ == '__main__':
    test()
