#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from workflow import Workflow3
from alfred_wf_generate_password.handlers import generate_password
from alfred_wf_generate_password.handlers import (
    MSG_ENTER_DATETIME, DEFAULT_LENGTH, MSG_INVALID_LENGTH,
)


def test_main():
    """

    .. note::

        由于我们的 handler 函数都有一个可选参数 ``args``, 所以我们可以指定任何输入
        参数, 来测试 handler 函数的行为.
    """
    wf = Workflow3()
    generate_password(wf, args=[])
    assert len(wf._items) == 1
    item = wf._items[0]
    assert item.title == MSG_ENTER_DATETIME
    assert item.autocomplete == DEFAULT_LENGTH

    wf = Workflow3()
    generate_password(wf, args=["12", ])
    for item in wf._items:
        assert len(item.arg) == 12
        assert item.title == item.arg

    wf = Workflow3()
    generate_password(wf, args=["InValid", ])
    assert len(wf._items) == 1
    item = wf._items[0]
    assert "is NOT a valid length" in item.title

    wf = Workflow3()
    generate_password(wf, args=["Hello", "World"])
    assert len(wf._items) == 1
    item = wf._items[0]
    assert item.title == "`Hello World` is NOT a valid length!"

    for args in (["6", ], ["100", ]):
        wf = Workflow3()
        generate_password(wf, args=args)
        assert len(wf._items) == 1
        item = wf._items[0]
        assert item.title == MSG_INVALID_LENGTH


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
