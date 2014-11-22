#!/usr/bin/env python
import yaml
import config

def date2str(d):
    return d.strftime("%m-%d-%Y")


def loadYaml(name):
    metadata = {}
    conf = config.getInstance()
    if name not in metadata:
        filename = '%s/conf/%s.yml' % (conf['basedir'], name)
        metadata[name] = yaml.load(open(filename, 'r'))

    return metadata[name]
