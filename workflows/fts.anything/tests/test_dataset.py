#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import pytest
from pytest import raises

import shutil
from alfred_wf_fts_anything.helpers import dump
from alfred_wf_fts_anything.dataset import DataSet, Setting


class TestSetting(object):
    def test_init(self):
        setting = Setting(columns=["movie_id"])
        assert len(setting.searchable_columns) == 0

    def test_post_init(self):
        setting = Setting(
            columns=["movie_id", "title", "description", "genres"],
            ngram_columns=["title", ],
            phrase_columns=["description", ],
            keyword_columns=["genres", ],
        )

        with raises(ValueError):
            Setting(
                columns=[1, 2, 3],
                ngram_columns=[4, ],
                phrase_columns=[5, ],
                keyword_columns=[6, ],
            )

        with raises(ValueError):
            Setting(
                columns=[1, 2, 3],
                ngram_columns=[1, 2],
                phrase_columns=[2, 3],
                keyword_columns=[3, 1],
            )

    def test_convert_to_item(self):
        doc = dict(
            movie_id=1, title="The Shawshank Redemption",
            description="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
            genres="Drama",
        )
        setting = Setting(
            columns=["movie_id", "title", "description", "genres"],
            subtitle_field="description: {description}",
        )
        item = setting.convert_to_item(doc)
        assert item.title == doc["title"]

        setting = Setting(
            columns=["movie_id", "title", "description", "genres"],
            title_field="movie_id",
            subtitle_field="description: {description}",
        )
        item = setting.convert_to_item(doc)
        assert item.title == "1"


class TestMovieDataset(object):
    dataset_name = None
    data = None
    setting = None

    @classmethod
    def setup_class(cls):
        dataset_name = "movie"
        movie_data = [
            dict(movie_id=1, title="The Shawshank Redemption",
                 description="Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.",
                 genres="Drama"),
            dict(movie_id=2, title="The Godfather",
                 description="The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
                 genres="Crime,Drama"),
            dict(movie_id=3, title="The Godfather: Part II",
                 description="The early life and career of Vito Corleone in 1920s New York City is portrayed, while his son, Michael, expands and tightens his grip on the family crime syndicate.",
                 genres="Crime,Drama"),
        ]
        movie_setting = dict(
            columns=["movie_id", "title", "description", "genres"],
            ngram_columns=["description", ],
            phrase_columns=["title"],
            keyword_columns=["genres", ],
            ngram_minsize=2,
            ngram_maxsize=10,
            keyword_lowercase=True,
            keyword_commas=True,
        )

        cls.dataset_name = dataset_name
        cls.data = movie_data
        cls.setting = movie_setting

        dataset = DataSet(name=dataset_name, data=None, setting=Setting(skip_post_init=True))
        data_file_path = dataset.get_data_file_path()
        setting_file_path = dataset.get_setting_file_path()
        index_dir = dataset.get_index_dir_path()
        if index_dir.exists():
            shutil.rmtree(index_dir.abspath)
        dump(movie_data, data_file_path.abspath)
        dump(movie_setting, setting_file_path.abspath)

    def test_search(self):
        dataset = DataSet(
            name=self.dataset_name,
            data=self.data,
            setting=self.setting,
        )
        idx = dataset.get_index()
        dataset.build_index(idx)

        result = dataset.search("redemption")
        assert len(result) == 1

        result = dataset.search("godfather")
        assert len(result) == 2

        # for doc in result:
        #     print(doc["title"])


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
