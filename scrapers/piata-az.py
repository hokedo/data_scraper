#!/usr/bin/env python
# coding: utf-8

import sys
import json
from pyquery import PyQuery as pq

def extract_data(req):
    data = {}
    doc = pq(req["html"])
    data["title"] = text("h1", doc)
    data["address"] = text("#detaliu-localitate", doc)
    data["price"] = text("#detaliu-pret-mob", doc)
    data["type"] = text(".Compartim\.", doc)
    data["date"] = text("#social-data", doc)

    selectors_extra = ["#social-vizualizari", "#social-abuz",
                       ".descriere-text", ".related",
                       "#social-ora", "#footer"
                       "#contact-titlu", "div#page header div#cnt-breadcrumb",
                       "header div#cnt-breadcrumb div#breadcrumb.nomobile div#social div#vizitatori-sap",
                       "header div#cnt-breadcrumb div#breadcrumb.nomobile ul li.breadcrumb-cat",
                       "#anunt-descriere"]
    data["extra"] = "".join(text(",".join(selectors_extra), doc))
    return data

def extract_urls(req):
    return []

def text(selector, pq_obj):
    return pq_obj(selector).text().strip()

if __name__ == "__main__":
    for line in sys.stdin:
        req = json.loads(line.strip())
        data = extract_data(req)
        print json.dumps(data)