#!/usr/bin/env python
import sys

for i, line in enumerate(open('gospels.htm')):
    for c in line:
        if ord(c) > 128:
            import pdb; pdb.set_trace()
            sys.stdout.write("%4d  %s" % (i, line))
            break
