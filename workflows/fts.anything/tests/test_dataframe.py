# -*- coding: utf-8 -*-

import pytest
from pytest import raises, approx
from fts_anything.dataframe import DataFrame


class TestDataFrame(object):
    dct = {
        "columns": ["id", "name"],
        "searchable": ["name"],
        "data": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"},
            {"id": 3, "name": "Cathy"},
        ]
    }
    df = DataFrame.from_dct(dct)

    def test_to_whoosh_schema(self):
        schema = self.df.to_whoosh_schema("User")


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
