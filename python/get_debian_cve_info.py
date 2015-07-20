#!/usr/bin/env python

from sys import argv
from bs4 import BeautifulSoup
from urllib.request import urlopen
from textwrap import wrap

import re

first = True
for arg in argv:
    if first:
        first = False
        continue

    print('NUMBER: ' + arg)
    try:
        response = urlopen('https://security-tracker.debian.org/tracker/' + arg).read()
        html = BeautifulSoup(response, "html5lib")
        tr = html.findAll('tr')

        severity = [s for s in tr if s.findAll(text=re.compile('NVD severity'))][0]
        print('SEVERITY: ' + severity.findAll('td')[1].find(text=True))

        description = [t for t in tr if t.findAll(text=re.compile('Description'))][0]
        description = wrap(description.findAll('td')[1].find(text=True), 75)
        for line in description:
            print('  ' + line)

    except Exception as e:
        print("  An error occured. Could not get CVE info.")
        #print(e)
