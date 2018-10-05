#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
from workflow import Workflow, web

github_v3_headers = dict(
    Accept="application/vnd.github.v3+json"
)


class QueryExecutor(object):
    token = "f3e50963caa04a95df279a10df1a270ab7a80387"
    endpoint = "https://api.github.com/search/repositories?q={query}+user:{username}&access_token={token}"

    def __init__(self, username="", query=""):
        self.username = username
        self.query = query

    def encode_query(self, username, query):
        query = "+".join([s for s in query.split(" ") if s.strip()])
        return self.endpoint.format(query=query, username=username, token=self.token)

    def _encode_query(self):
        return self.encode_query(self.username, self.query)

    def parse_html(self, html):
        data = json.loads(html)
        repo_list = list()
        for item in data["items"][:10]:
            name = item["name"]
            url = item["html_url"]
            description = item["description"]
            repo_list.append((name, url, description))
        return repo_list


qe = QueryExecutor()


def main(wf):
    import requests

    # if len(wf.args) >= 2:
    #     qe.username = wf.args[0]
    #     qe.query = wf.args[1]

    qe.username = "MacHu-GWU"
    qe.query = "crawlib"

    def get_data():
        url = qe._encode_query()
        response = requests.get(url, headers=github_v3_headers)
        return qe.parse_html(response.text)

    # url = qe._encode_query()
    # response = requests.get(url)
    # repo_list = qe.parse_html(response.text)

    repo_list = wf.cached_data("repo_list", get_data, max_age=2)

    for name, url, description in repo_list:
        wf.add_item(
            title=name,
            subtitle=description,
            arg=url,
            valid=True,
        )
    wf.send_feedback()


def test():
    import requests

    qe.query = "crawlib"
    qe.username = "MacHu-GWU"
    url = qe._encode_query()
    response = requests.get(url, headers=github_v3_headers)
    repo_list = qe.parse_html(response.text)
    assert len(repo_list) >= 1
    print(repo_list)


if __name__ == "__main__":
    # test()
    wf = Workflow(
        libraries=["lib", ],
    )
    logger = wf.logger
    sys.exit(wf.run(main))
