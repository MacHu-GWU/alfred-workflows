# -*- coding: utf-8 -*-

import json
from collections import OrderedDict
from whoosh import fields
from .utils import create_whoosh_schema


class DataFrame(object):
    def __init__(self,
                 data,
                 columns,
                 searchable,
                 title_field,
                 subtitle_field,
                 arg_field,
                 autocomplete_field,
                 context):
        self.data = data
        self.columns = columns
        self.searchable = searchable
        self.title_field = title_field
        self.subtitle_field = subtitle_field
        self.arg_field = arg_field
        self.autocomplete_field = autocomplete_field
        self.context = context

    @classmethod
    def from_dct(cls, dct):
        return cls(
            data=dct["data"],
            columns=dct["columns"],
            searchable=dct["searchable"],
            title_field=dct.get("title_field"),
            subtitle_field=dct.get("subtitle_field"),
            arg_field=dct.get("arg_field"),
            autocomplete_field=dct.get("autocomplete_field"),
            context=dct.get("context")
        )

    @classmethod
    def from_file(cls, path):
        with open(path, "rb") as f:
            dct = json.loads(f.read().decode("utf-8"))
        return cls.from_dct(dct)

    def to_whoosh_schema(self, classname, ngram_minsize=2, ngram_maxsize=10):
        return create_whoosh_schema(
            str(classname), self.columns, self.searchable, ngram_minsize, ngram_maxsize
        )
