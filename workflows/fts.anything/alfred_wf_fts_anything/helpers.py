# -*- coding: utf-8 -*-

import json
import hashlib


def md5_file(path):
    m = hashlib.md5()
    with open(path, "rb") as f:
        b = f.read()
        m.update(b)
    return m.hexdigest()


def is_subset(set_a, set_b):
    return len(set(set_a).intersection(set_b)) == len(set_a)


def no_overlap(*set_list):
    return sum([len(s) for s in set_list]) == len(set.union(*[set(s) for s in set_list]))


def dump(data, path):
    with open(path, "wb") as f:
        f.write(json.dumps(data, indent=4, sort_keys=True).encode("utf-8"))


def load(path):
    with open(path, "rb") as f:
        return json.loads(f.read().decode("utf-8"))
