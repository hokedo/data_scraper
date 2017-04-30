#!/usr/bin/env python
# coding: utf-8

import re
import sys
import json
from pyquery import PyQuery as pq

def extract_data(req):
		data = {}
		if re.search(r"www\.piata-az\.ro/anunturi/oras-cluj-napoca/\d+", req["url"]):
			doc = pq(req["html"])
			data["title"] = text("h1", doc)

			price = text("#detaliu-pret-mob:eq(0)", doc)
			price = re.match(r"(\d+)\s*([A-z]+)", price)
			data["price"] = float(price.group(1))
			data["currency"] = price.group(2)
			data["type"] = text(".Compartim\.", doc)
			data["date"] = text("#social-data", doc)

			street = text("div.actiuni-col-a:contains('Strada')+div.actiuni-col-b", doc)

			data["address"] = "{}, {}".format(street or "", text("#detaliu-localitate", doc))

			selectors_extra = [
							"#social-vizualizari",
							"#social-abuz",
							 ".descriere-text", ".related",
							 "#social-ora", "#footer"
							 "#contact-titlu", "div#page header div#cnt-breadcrumb",
							 "header div#cnt-breadcrumb div#breadcrumb.nomobile div#social div#vizitatori-sap",
							 "header div#cnt-breadcrumb div#breadcrumb.nomobile ul li.breadcrumb-cat",
							 "#anunt-descriere"
							]
			data["extra"] = "".join(text(",".join(selectors_extra), doc))
		return data

def extract_urls(req):
		urls = []
		doc = pq(req["html"])
		for link in doc("a.link_totanunt"):
			urls.append(pq(link).attr("href"))
		next_page = doc("a.next_page:eq(0)").attr("href")
		if next_page:
			urls.append(next_page)
		return urls

def text(selector, pq_obj):
		return pq_obj(selector).text().strip()

if __name__ == "__main__":
		for line in sys.stdin:
			req = json.loads(line.strip())
			data = extract_data(req)
			print json.dumps(data)