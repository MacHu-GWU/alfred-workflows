# -*- coding: utf-8 -*-

import hashlib
from collections import OrderedDict
from whoosh import fields


def md5_file(path):
    m = hashlib.md5()
    with open(path, "rb") as f:
        b = f.read()
        m.update(b)
    return m.hexdigest()


def create_whoosh_schema(classname, columns, searchable, ngram_minsize=2, ngram_maxsize=10):
    attrs = OrderedDict()
    for c in columns:
        if c in searchable:
            attrs[c] = fields.NGRAM(minsize=ngram_minsize, maxsize=ngram_maxsize, stored=True)
        else:
            attrs[c] = fields.STORED()
    SchemaClass = type(classname, (fields.SchemaClass,), attrs)
    schema = SchemaClass()
    return schema
