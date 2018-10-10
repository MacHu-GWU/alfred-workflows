# -*- coding: utf-8 -*-

import random
import string


def get_text_fingerprint(text, hash_meth, encoding="utf-8"):
    """
    Use default hash method to return hash value of a piece of string
    default setting use 'utf-8' encoding.
    """
    m = hash_meth()
    m.update(text.encode(encoding))
    return m.hexdigest()


DEFAULT_CHUNK_SIZE = 1 << 20


def get_file_fingerprint(abspath, hash_meth, nbytes=0, chunk_size=DEFAULT_CHUNK_SIZE):
    """

    :param abspath:
    :param hash_meth: one of ``hashlib.md5``, ``hashlib.sha256``, ``hashlib.sha512``
    :param nbytes:
    :param chunk_size:
    :return:
    """
    if nbytes < 0:
        raise ValueError("chunk_size cannot smaller than 0")
    if chunk_size < 1:
        raise ValueError("chunk_size cannot smaller than 1")
    if (nbytes > 0) and (nbytes < chunk_size):
        chunk_size = nbytes

    m = hash_meth()
    with open(abspath, "rb") as f:
        if nbytes:  # use first n bytes
            have_reads = 0
            while True:
                have_reads += chunk_size
                if have_reads > nbytes:
                    n = nbytes - (have_reads - chunk_size)
                    if n:
                        data = f.read(n)
                        m.update(data)
                    break
                else:
                    data = f.read(chunk_size)
                    m.update(data)
        else:  # use entire content
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                m.update(data)

    return m.hexdigest()


alpha_digits = string.ascii_letters + string.digits


def random_string(length):
    """
    Generate Random String.
    """
    return "".join([random.choice(alpha_digits) for _ in range(length)])
