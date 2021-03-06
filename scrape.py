#!/usr/bin/env python
# coding: utf-8

import os
import sys
import json
import socket
import logging
import requests
import traceback
from collections import deque

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def start_crawling(req_obj, proxies={}):
    start_url = req_obj.get("url")
    domain = req_obj.get("domain")
    session = requests.Session()
    urls = deque()
    visited_urls = set()
    visited_urls.add(start_url)
    urls.append(start_url)
    while urls:
        data = {"domain": domain}
        req = dict()
        url = urls.popleft()
        try:
            logger.info("Requesting:\t%s", url)
            res = session.request("GET", url, timeout=150, cookies=None, verify=False,
                                  headers={
                                      "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16",
                                      "Accept-Language": "en-US,en;q=0.8,de-DE;q=0.6,de;q=0.4,en;q=0.2",
                                      "Accept-Charset": "utf-8;q=0.7,*;q=0.7"
                                  },
                                  proxies=proxies)

        except (requests.exceptions.RequestException, socket.error) as ex:
            #print >> sys.stderr, ex
            #print >> sys.stderr, url
            logger.error(str(ex))
            logger.error(url)
            continue

        if res is None: continue

        req["url"], req["html"] = res.url, res.text
        data["url"] = res.url

        try:
            extractor = __import__(domain)
        except ImportError as ex:
            #print >> sys.stderr, ex
            logger.error(str(ex))
            continue

        try:
            logger.info("Extracting urls:\t%s", req["url"])
            crawled = extractor.extract_urls(req)
        # print crawled
        except Exception as ex:
            # print >>sys.stderr, "URL\n", ex
            traceback.print_exc(file=sys.stderr)
            continue
        for page in crawled:
            if page not in visited_urls:
                visited_urls.add(page)
                urls.append(page)

        try:
            logger.info("Extracting data:\t%s", req["url"])
            data["data"] = extractor.extract_data(req)
            data["start_url"] = req["url"]
            data["html"] = req["html"]
        except Exception as ex:
            # print >>sys.stderr, "DATA\n", ex
            #traceback.print_exc(file=sys.stderr)
            logger.error(str(ex))
            continue

        if data:
            yield data


if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(__file__), "scrapers"))
    for line in sys.stdin:
        request_obj = json.loads(line.strip())
        for data in start_crawling(request_obj):
            print json.dumps(data)
