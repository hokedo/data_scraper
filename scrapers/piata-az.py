#!/usr/bin/env python
# coding: utf-8

import sys
import json
from pyquery import PyQuery as pq

def extract_data(req):
    data = {}
    doc = pq(req["html"])
    data["title"] = doc("h1").text()
    data["address"] = doc("#detaliu-localitate").text()
    data["price"] = doc("#detaliu-pret-mob").text()
    data["type"] = doc(".Compartim\.").text()

    return data

def extract_urls(req):
    return []


if __name__ == "__main__":
    for line in sys.stdin:
        req = json.loads(line.strip())
        data = extract_data(req)
        print json.dumps(data)