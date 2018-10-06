#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx
from workflow import Workflow3
from alfred_wf_fts_anything.handlers import main
from alfred_wf_fts_anything.handlers import MSG_FOUND_NOTHING


class TestSearch(object):
    def test_no_argument(self):
        wf = Workflow3()
        main(wf, args=["d2skills"])
        assert len(wf._items) == 1
        item = wf._items[0]
        assert "Search in Dataset" in item.title

    def test_found_nothing(self):
        wf = Workflow3()
        main(wf, args=["d2skills", "SomethingYouCanNotFind"])
        assert len(wf._items) == 1
        item = wf._items[0]
        assert item.title == MSG_FOUND_NOTHING

    def test_found(self):
        wf = Workflow3()
        main(wf, args=["d2skills", "sor"])
        assert len(wf._items) >= 10
        for item in wf._items:
            print(item.title)



if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
