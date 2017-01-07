#!/usr/bin/env python
# coding: utf-8

import sys
import requests
from pyquery import PyQuery as pq

url = "http://www.piata-az.ro/anunturi/apartamente-de-inchiriat-1031"

while url:
    print >> sys.stderr, "Current url:\t{}".format(url)
    r = requests.get(url)
    h = pq(r.text)
    for item in h("a.link_totanunt"):
        print pq(item).attr("href")
    url = h(".next_page").attr("href")

