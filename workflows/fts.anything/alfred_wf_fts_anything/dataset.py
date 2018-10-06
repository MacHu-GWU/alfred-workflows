# -*- coding: utf-8 -*-

import json
import shutil
from pprint import pprint
from collections import OrderedDict

import attr
from attrs_mate import AttrsClass
from whoosh import index, fields, qparser
from pathlib_mate import PathCls as Path
from .helpers import is_subset, no_overlap
from .constant import ALFRED_FTS


@attr.s
class Setting(AttrsClass):
    """

    :param ngram_columns: list.
    :param phrase_columns: list.
    :param keyword_columns: list.
    """
    columns = attr.ib(factory=list)

    ngram_columns = attr.ib(factory=list)
    phrase_columns = attr.ib(factory=list)
    keyword_columns = attr.ib(factory=list)

    searchable_columns_cache = attr.ib(default=None)

    ngram_minsize = attr.ib(default=2)
    ngram_maxsize = attr.ib(default=10)
    keyword_lowercase = attr.ib(default=True)
    keyword_commas = attr.ib(default=True)

    title_field = attr.ib(default=None)
    subtitle_field = attr.ib(default=None)
    arg_field = attr.ib(default=None)
    autocomplete_field = attr.ib(default=None)

    skip_post_init = attr.ib(default=False)

    def __attrs_post_init__(self):
        if not self.skip_post_init:
            assert is_subset(self.ngram_columns, self.columns)
            assert is_subset(self.phrase_columns, self.columns)
            assert is_subset(self.keyword_columns, self.columns)
            assert no_overlap(self.ngram_columns, self.phrase_columns, self.keyword_columns)

    @property
    def searchable_columns(self):
        if self.searchable_columns_cache is None:
            self.searchable_columns_cache = list()
            self.searchable_columns_cache.extend(self.ngram_columns)
            self.searchable_columns_cache.extend(self.phrase_columns)
            self.searchable_columns_cache.extend(self.keyword_columns)
        return self.searchable_columns_cache

    def create_whoosh_schema(self):
        schema_classname = "WhooshSchema"
        schema_classname = str(schema_classname)
        attrs = OrderedDict()
        for c in self.columns:
            if c in self.ngram_columns:
                field = fields.NGRAM(
                    minsize=self.ngram_minsize,
                    maxsize=self.ngram_maxsize,
                    stored=True,
                )
            elif c in self.phrase_columns:
                field = fields.TEXT(stored=True)
            elif c in self.keyword_columns:
                field = fields.KEYWORD(
                    lowercase=self.keyword_lowercase,
                    commas=self.keyword_commas,
                    stored=True,
                )
            else:
                field = fields.STORED()
            attrs[c] = field
        SchemaClass = type(schema_classname, (fields.SchemaClass,), attrs)
        schema = SchemaClass()
        return schema


@attr.s
class DataSet(AttrsClass):
    """
    Represent the dataset you want to search.

    :param data: dict list.
    :param columns: list.

    :param title_field: str, the field used for alfred workflow item title.
    :param subtitle_field: str, the field used for alfred workflow item subtitle.
    :param arg_field: str, the field used for alfred workflow item argument.
    :param autocomplete_field: str, the field used for alfred workflow item autocomplete.
    """
    name = attr.ib(default=None)
    data = attr.ib(default=None)
    setting = attr.ib(
        convert=Setting.from_dict,
        validator=attr.validators.optional(
            attr.validators.instance_of(Setting),
        ),
        factory=Setting,
    )
    schema_cache = attr.ib(default=None)

    def update_data_from_file(self):
        if self.data is None:
            data_file = self.get_data_file_path()
            with open(data_file.abspath, "rb") as f:
                self.data = json.loads(f.read().decode("utf-8"))

    def update_setting_from_file(self):
        if not self.setting.columns:
            setting_file = self.get_setting_file_path()
            with open(setting_file.abspath, "rb") as f:
                setting_data = json.loads(f.read().decode("utf-8"))
                self.setting = Setting(**setting_data)

    def get_data_file_path(self):
        return Path(ALFRED_FTS, "{}.json".format(self.name))

    def get_setting_file_path(self):
        return Path(ALFRED_FTS, "{}-setting.json".format(self.name))

    def get_index_dir_path(self):
        return Path(ALFRED_FTS, "{}-whoosh_index".format(self.name))

    def get_schema(self):
        if self.schema_cache is None:
            self.schema_cache = self.setting.create_whoosh_schema()
        return self.schema_cache

    def get_index(self):
        index_dir = self.get_index_dir_path()
        if index_dir.exists():
            idx = index.open_dir(index_dir.abspath)
        else:
            schema = self.get_schema()
            index_dir.mkdir()
            idx = index.create_in(dirname=index_dir.abspath, schema=schema)
        return idx

    def build_index(self, idx):
        self.update_data_from_file()
        writer = idx.writer()
        for row in self.data:
            doc = {c: row.get(c) for c in self.setting.columns}
            writer.add_document(**doc)
        writer.commit()

    def search(self, query_str, limit=20):
        schema = self.get_schema()
        idx = self.get_index()
        query = qparser.MultifieldParser(
            self.setting.searchable_columns,
            schema=schema,
        ).parse(query_str)
        with idx.searcher() as searcher:
            result = [hit.fields() for hit in searcher.search(query, limit=limit)]
        return result

    # @attr.s
    # class AlfredItemCreator(AttrsClass):
    #
    #     context = attr.ib(default=None)
    #
