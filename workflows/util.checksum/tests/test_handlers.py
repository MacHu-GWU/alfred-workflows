#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from workflow import Workflow3
import os
import hashlib
from alfred_wf_util_checksum.helpers import get_file_fingerprint
from alfred_wf_util_checksum.handlers import main


class TestHandler(object):
    def test_main(self):
        # random checksum
        wf = Workflow3()
        main(wf, args=["md5", ])
        assert len(wf._items) == 10
        assert wf._items[0].title == wf._items[0].arg  # Random MD5

        # file exists
        wf = Workflow3()
        main(wf, args=["md5", __file__])
        assert len(wf._items) == 1
        item = wf._items[0]
        assert item.title == get_file_fingerprint(__file__, hashlib.md5)

        # file not exists
        wf = Workflow3()
        main(wf, args=["md5", "__file__" + "NotFound"])
        assert len(wf._items) == 1
        assert "does not exists!" in wf._items[0].title

        # is a directory
        wf = Workflow3()
        main(wf, args=["md5", os.path.dirname(__file__)])
        assert len(wf._items) == 1
        assert "is a directory!" in wf._items[0].title


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
