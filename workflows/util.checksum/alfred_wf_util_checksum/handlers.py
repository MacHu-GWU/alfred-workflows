# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import hashlib
from .helpers import get_file_fingerprint, get_text_fingerprint, random_string
from .icons import ICON_NOT_FOUND

hash_algo_mapper = {
    "md5": hashlib.md5,
    "sha256": hashlib.sha256,
    "sha512": hashlib.sha512,
}


def main(wf, args=None):
    if args is None:
        args = wf.args
    n_args = len(args)

    hash_algo = hash_algo_mapper[args[0]]
    if n_args == 1:  # display some random checksum for copy
        for _ in range(10):
            checksum = get_text_fingerprint(random_string(32), hash_algo)
            wf.add_item(
                title=checksum,
                subtitle="copy to clipboard",
                arg=checksum,
                valid=True,
            )

    elif n_args >= 2:
        abspath = " ".join(args[1:])
        if os.path.exists(abspath):
            if os.path.isfile(abspath):
                checksum = get_file_fingerprint(abspath, hash_algo)
                wf.add_item(
                    title=checksum,
                    subtitle="copy to clipboard",
                    arg=checksum,
                    valid=True,
                )
            elif os.path.isdir(abspath):
                wf.add_item(
                    title="'%s' is a directory!" % abspath,
                    valid=True,
                    icon=ICON_NOT_FOUND,
                )
        else:
            wf.add_item(
                title="'%s' does not exists!" % abspath,
                valid=True,
                icon=ICON_NOT_FOUND,
            )

    return wf
