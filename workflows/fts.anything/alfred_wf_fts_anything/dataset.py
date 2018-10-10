# -*- coding: utf-8 -*-

import json
import shutil
from pprint import pprint
from collections import OrderedDict

import six
import attr
from attrs_mate import AttrsClass
from whoosh import index, fields, qparser
from pathlib_mate import PathCls as Path
from .helpers import is_subset, no_overlap
from .constant import ALFRED_FTS


@attr.s
class WFItem(AttrsClass):
    """
    Represent a Workflow Item.

    TODO: support custom icon.
    """
    title = attr.ib(default="")
    subtitle = attr.ib(default="")
    arg = attr.ib(default=None)
    autocomplete = attr.ib(default=None)


ITEM_ATTRS = [a.name for a in WFItem.__attrs_attrs__]


@attr.s
class Setting(AttrsClass):
    """
    Defines how you want to index your dataset

    :param ngram_columns: list, columns to use ngram index.
    :param phrase_columns: list. columns to use phrase (full word) index.
    :param keyword_columns: list. columns to use keyword index.

    :param ngram_minsize: minimal number of character to match., default 2.
    :param ngram_maxsize: maximum number of character to match., default 10.
    :param keyword_lowercase: for keyword type field, is the match case sensitive?
        default True (not sensitive).
    :param keyword_commas: is the delimiter of keyword is comma or space?

    :param title_field: which field is used as ``WorkflowItem.title``?
    :param subtitle_field: which field is used as ``WorkflowItem.subtitle``?
    :param arg_field: which field is used as ``WorkflowItem.arg``?
    :param autocomplete_field: which field is used as ``WorkflowItem.autocomplete``?

    :param searchable_columns_cache: implementation reserved attribute.
    :param skip_post_init: implementation reserved attribute.

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
            if not is_subset(self.ngram_columns, self.columns):
                msg = "{} not subset of {}".format(self.ngram_columns, self.columns)
                raise ValueError(msg)

            if not is_subset(self.phrase_columns, self.columns):
                msg = "{} not subset of {}".format(self.phrase_columns, self.columns)
                raise ValueError(msg)

            if not is_subset(self.keyword_columns, self.columns):
                msg = "{} not subset of {}".format(self.keyword_columns, self.columns)
                raise ValueError(msg)

            if not no_overlap(self.ngram_columns, self.phrase_columns, self.keyword_columns):
                msg = ("`ngram_columns`, `phrase_columns` and `keyword_columns` "
                       "should not have any overlaps!")
                raise ValueError(msg)

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

    def convert_to_item(self, doc):
        # whoosh 所返回的 doc 中并不一定所有项都有, 有的项可能没有, 我们先为这些
        # 没有的项赋值 None
        doc = {c: doc.get(c) for c in self.columns}
        item_data = dict()
        for item_field in ITEM_ATTRS:
            setting_key = "{}_field".format(item_field)
            setting_value = getattr(self, setting_key)

            if setting_value is None:  # use item_field by default
                field_value = doc.get(item_field)

            elif setting_value in self.columns:  # on of column
                field_value = doc.get(setting_value)

            else:  # template
                field_value = setting_value.format(**doc)

            if field_value is not None:
                field_value = six.text_type(field_value)
                if field_value:
                    item_data[item_field] = field_value

        return WFItem(**item_data)


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
        converter=Setting.from_dict,
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
