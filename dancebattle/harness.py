#!/usr/bin/python -u

import sys
from subprocess import Popen, PIPE
from os import sep, listdir
import re

dir = "tests"
filepat = re.compile(r'^5\.(\d+)\.in$')

for file in listdir(dir):
    m = filepat.match(file)
    if not m:
        continue
    print "5 %d:" % (int(m.group(1))),
    result = Popen(["python","-u","dancebattle", dir + sep + file], \
            stdout=PIPE).communicate()[0]
    print result.strip()
