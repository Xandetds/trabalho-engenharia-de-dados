import os
import csv
import io
import json

import pandas as pd

from minio_connection import get_minio_client


GOLD_BUCKET = os.getenv("MINIO_GOLD_BUCKET", "gold")
GOLD_PREFIX = os.getenv("MINIO_GOLD_PREFIX", "tse")
EXPECTED_GOLD_TABLES = (
    "fato_candidatura_dashboard",
    "fato_bem_candidato_dashboard",
    "dim_partido",
    "dim_cargo",
    "dim_municipio",
)


def get_expected_gold_paths() -> dict[str, str]:
    prefix = GOLD_PREFIX.strip("/")

    return {
        table: f"{prefix}/{table}/" if prefix else f"{table}/"
        for table in EXPECTED_GOLD_TABLES
    }


def list_gold_objects(prefix: str | None = None) -> list[dict]:
    client = get_minio_client()
    object_prefix = GOLD_PREFIX if prefix is None else prefix

    response = client.list_objects_v2(Bucket=GOLD_BUCKET, Prefix=object_prefix)

    return [
        {
            "key": item["Key"],
            "size": item["Size"],
            "last_modified": item["LastModified"].isoformat(),
        }
        for item in response.get("Contents", [])
    ]


def list_gold_table_objects(table_name: str) -> list[dict]:
    table_path = get_expected_gold_paths()[table_name]

    return [
        item
        for item in list_gold_objects(table_path)
        if not item["key"].endswith("/")
        and "/_delta_log/" not in item["key"]
        and not item["key"].split("/")[-1].startswith("_")
    ]


def read_gold_table_records(table_name: str) -> list[dict]:
    client = get_minio_client()
    records = []

    for item in list_gold_table_objects(table_name):
        key = item["key"]
        response = client.get_object(Bucket=GOLD_BUCKET, Key=key)
        content = response["Body"].read()

        if key.endswith(".json"):
            loaded = json.loads(content.decode("utf-8"))
            records.extend(loaded if isinstance(loaded, list) else [loaded])
        elif key.endswith(".jsonl"):
            lines = content.decode("utf-8").splitlines()
            records.extend(json.loads(line) for line in lines if line.strip())
        elif key.endswith(".csv"):
            text = content.decode("utf-8-sig")
            records.extend(csv.DictReader(io.StringIO(text)))
        elif key.endswith(".parquet"):
            dataframe = pd.read_parquet(io.BytesIO(content))
            records.extend(dataframe.to_dict(orient="records"))

    return records
