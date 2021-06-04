#!/usr/bin/env bash
pip install -r requirements.txt
cd ./project/
export FLASK_APP=__init__.py
export FLASK_ENV=development
flask run
exit 0