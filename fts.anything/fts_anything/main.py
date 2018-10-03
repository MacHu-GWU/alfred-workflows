# -*- coding: utf-8 -*-

import os
import hashlib

HOME = os.path.expanduser("~")

def md5_string(text):
    m = hashlib.md5()
    m.update(text.encode("utf8"))
    return m.hexdigest()
