#!/usr/bin/env python
# coding: utf-8

import re
import sys
import json
from pyquery import PyQuery as pq


def extract_data(req):
	data = {}
	if re.search(r"inchiriere-apartament", req["url"]):
		doc = pq(req["html"])
		data["title"] = text("h1.page-header", doc)

		price = text("h5.price-darkred", doc)
		price = re.match(r"^(\d+).+", price)
		data["price"] = float(price.group(1))
		data["currency"] = "EURO"
		data["type"] = text("dt:contains('Compartimentare') + dd", doc)
		# data["date"] = text("#social-data", doc)

		area = text("dt:contains('Cartier') + dd", doc)
		city = text("dt:contains('Localitate') + dd", doc)
		address = [area, city]
		
		# street = text("div.actiuni-col-a:contains('Strada')+div.actiuni-col-b", doc)
		# street = street.strip(" -")
		# if street:
		# 	address.append(street)

		data["address"] = ", ".join(address)

		selectors_extra = [
			".mb30 p.text",
		]
		data["extra"] = "".join(text(",".join(selectors_extra), doc))
	return data


def extract_urls(req):
	urls = []
	doc = pq(req["html"])
	for link in doc("h2.property-row-title a"):
		urls.append("https://www.edil.ro" + pq(link).attr("href"))
	next_page = doc("li a[rel='next']").attr("href")
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