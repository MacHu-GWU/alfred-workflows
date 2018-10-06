# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from pathlib_mate import Path
from alfred_wf_fts_anything.constant import ALFRED_FTS
from alfred_wf_fts_anything.dataset import DataSet
from alfred_wf_fts_anything.helpers import dump


dataset = DataSet("d2skills")
dataset.update_data_from_file()
for doc in dataset.data:
    # print(doc)
    title = "{class_} - {skill_tab} - {name_en} ({name_cn}) - {code}".format(
        class_=doc["class"],
        skill_tab=doc["skill_tab"],
        name_en=doc["name_en"],
        name_cn=doc["name_cn"],
        code=doc["code"],
    )
    subtitle = "简称: {name_abbr}, 说明: {description}".format(
        name_abbr=doc["name_abbr"],
        description=doc["description"],
    )
    arg = doc["code"]
    doc["title"] = title
    doc["subtitle"] = subtitle
    doc["arg"] = arg

dump(dataset.data, "d2skills.json")