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
		data["title"] = text("#details h1", doc)

		price = text(".details_price span.price", doc)
		price = re.match(r"^(\d+).+", price)
		data["price"] = float(price.group(1))
		data["currency"] = "EURO"
		data["type"] = text(".characteristics:contains('Compartimentare') div:eq(1)", doc)
		# data["date"] = text("#social-data", doc)

		area = text("#details h1 span", doc)
		address = [area]

		# street = text("div.actiuni-col-a:contains('Strada')+div.actiuni-col-b", doc)
		# street = street.strip(" -")
		# if street:
		# 	address.append(street)

		data["address"] = ", ".join(address)

		selectors_extra = [
			".characteristics_container p",
		]
		data["extra"] = "".join(text(",".join(selectors_extra), doc))
	return data


def extract_urls(req):
	urls = []
	doc = pq(req["html"])
	for link in doc("li.next a"):
		urls.append(pq(link).attr("href"))
	next_page = doc("li.estate-listing exclusivity h2 a").attr("href")
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