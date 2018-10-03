# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from pathlib_mate import Path

HOME = Path.home()
ALFRED_FTS = Path(HOME, ".alfred-fts")
META_DB = Path(ALFRED_FTS, "metadata.sqlite")
