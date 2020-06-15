#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import logging
import os

import boto3
from flask.cli import FlaskGroup

from app import create_app
from config import config
from data import goals, teachers


current_config = config.get(os.getenv('FLASK_ENV'))
if current_config is None:
    raise RuntimeError(
        "Unknown configuration: check FLASK_ENV environment variable value"
    )

app = create_app(current_config)
cli = FlaskGroup(app)


@app.cli.command('create_storage')
def create_storage():
    data = {
        "goals": [{
            "code": code,
            "title": title,
        } for code, title in goals.items()],
        "teachers": teachers,
    }

    if current_config.APP_STORAGE_LOCATION == 'local':
        data_path = current_config.get_storage_path()
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        logging.info(f"The data were written to {data_path}")

    elif current_config.APP_STORAGE_LOCATION == 's3':
        s3 = boto3.resource(
            's3',
            region_name=current_config.APP_STORAGE_S3_REGION,
            aws_access_key_id=current_config.APP_STORAGE_S3_ACCESS_KEY_ID,
            aws_secret_access_key=current_config.APP_STORAGE_S3_SECRET_KEY_ID
        )

        s3.Object(
            current_config.APP_STORAGE_S3_BUCKET,
            current_config.APP_STORAGE_FILE
        ).put(Body=json.dumps(
                data,
                indent=4,
                ensure_ascii=False
            )
        )

        logging.info(
            f"The data were written to s3 bucket {current_config.APP_STORAGE_S3_BUCKET}"
        )


if __name__ == '__main__':
    cli()
