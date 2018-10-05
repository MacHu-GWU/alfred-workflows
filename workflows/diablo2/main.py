# -*- coding: utf-8 -*-

import attr
import pandas as pd
from pathlib_mate import Path
from pandas_mate import transform
from attrs_mate import AttrsClass
from superjson import json


PWD = Path(__file__).parent
FILE_CLASS_CODE = Path(PWD, "class-code.txt")
FILE_SKILL_TAB_CODE = Path(PWD, "skill-tab-code.txt")
FILE_SKILL_CODE = Path(PWD, "skill-code.txt")

df_class_code = pd.read_csv(FILE_CLASS_CODE.abspath, sep="\t")
df_skill_tab_code = pd.read_csv(FILE_SKILL_TAB_CODE.abspath, sep="\t")
df_skill_code = pd.read_csv(FILE_SKILL_CODE.abspath, sep="\t")


@attr.s
class FTSData(AttrsClass):
    columns = attr.ib()
    searchable = attr.ib()
    data = attr.ib()

columns = list(df_skill_code.columns)
searchable = ["class", "skill_tab", "name_en", "name_cn", "name_abbr"]
data = transform.to_dict_list_generic_type(df_skill_code, int_col=["code",])

fts_data = FTSData(columns=columns, searchable=searchable, data=data)
json.dump(fts_data.to_dict(), "d2skill.json", pretty=True)