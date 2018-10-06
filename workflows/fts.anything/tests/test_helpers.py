#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx
from alfred_wf_fts_anything import helpers


def test_is_subset():
    assert helpers.is_subset([1, ], [1, 2, 3])
    assert helpers.is_subset([1, 2, 3], [1, 2, 3])
    assert helpers.is_subset([1, 2, 3], [1, ]) is False


def test_no_overlap():
    assert helpers.no_overlap([1, 2], [3, 4])
    assert helpers.no_overlap([1, 2], [2, 3]) is False


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
