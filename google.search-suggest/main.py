# -*- coding: utf-8 -*-

import os
import sys
from workflow import Workflow, web
import xml.etree.ElementTree as ET


class QueryExecutor(object):
    endpoint = "https://www.google.com/complete/search?output=toolbar&q={query}"

    def __init__(self, query=""):
        self.query = query

    def encode_query(self, query):
        query = "+".join([s for s in query.split(" ") if s.strip()])
        return self.endpoint.format(query=query)

    def _encode_query(self):
        return self.encode_query(self.query)

    def parse_html(self, html):
        root = ET.fromstring(html)
        suggestion_list = list()
        for suggestion in root.iter("suggestion"):
            suggestion_list.append(suggestion.attrib["data"])
        return suggestion_list


qe = QueryExecutor()


def test():
    qe.query = "money order"
    url = qe._encode_query()
    response = web.get(url)
    suggestion_list = qe.parse_html(response.text)
    print(suggestion_list)


def main(wf):
    query = ""
    if len(wf.args):
        qe.query = wf.args[0]

    def get_data():
        url = qe._encode_query()
        response = web.get(url)
        return qe.parse_html(response.text)

    url = qe._encode_query()
    response = web.get(url)
    suggestion_list = qe.parse_html(response.text)
    # suggestion_list =  wf.cached_data("suggestion_list", get_data, max_age=1)

    for suggestion in suggestion_list:
        wf.add_item(
            title=suggestion,
            subtitle="Search Google For `%s`" % suggestion,
            arg=suggestion,
            valid=True,
        )
    wf.send_feedback()


if __name__ == "__main__":
    # test()
    wf = Workflow()
    logger = wf.logger
    sys.exit(wf.run(main))
