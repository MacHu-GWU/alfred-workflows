#!/usr/bin/env bash
# -*- coding: utf-8 -*-

cd "$(dirname "$0")"
rm -r ./workflow
mkdir ./workflow
pip2.7 install Alfred-Workflow --target=./workflow
pip2.7 install . --target=./workflow/lib
cp ./main.py ./workflow/main.py
