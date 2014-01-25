#!/usr/bin/env python

import os

print 'Content-Type: text/html\n'

keys = os.environ.keys()
keys.sort()

print "<center><h2>OS Environment</h2></center>"

print "<table border='1' cellpadding='2' cellspacing='0'>"
for k in keys:
    v = os.environ[k]
    if not v:
        v = "&nbsp;"
    print "  <tr> <td valign='top'><font color='blue'>%s</font></td> " \
          "<td>%s</td> </tr>" % (k, v)
print "</table>"
