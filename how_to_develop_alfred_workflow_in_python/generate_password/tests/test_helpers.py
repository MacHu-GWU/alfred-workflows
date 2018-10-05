# -*- coding: utf-8 -*-

import pytest
from alfred_wf_generate_password.helpers import random_password
from alfred_wf_generate_password.helpers import charset_upper, charset_symbols


def test_random_password():
    password = random_password(12, uppercase=True)
    assert len(charset_upper.intersection(password)) > 0

    password = random_password(12, symbol=True)
    assert len(charset_symbols.intersection(password)) > 0


if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
