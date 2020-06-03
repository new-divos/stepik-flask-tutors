#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os

from flask.cli import FlaskGroup

from app import create_app
from config import config
from data import goals, teachers


current_config = config.get(os.getenv('FLASK_ENV'))
if current_config is None:
    raise RuntimeError("Unknown configuration: check FLASK_ENV environment variable value")

app = create_app(current_config)
cli = FlaskGroup(app)


@app.cli.command('create_storage')
def create_storage():
    data = {
        "goals": goals,
        "teachers": teachers,
    }

    data_path = current_config.get_storage_path()
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"The data were written to {data_path}")


if __name__ == '__main__':
    cli()
