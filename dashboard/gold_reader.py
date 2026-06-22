import os

from minio_connection import get_minio_client


GOLD_BUCKET = os.getenv("MINIO_GOLD_BUCKET", "gold")
GOLD_PREFIX = os.getenv("MINIO_GOLD_PREFIX", "")
EXPECTED_GOLD_TABLES = (
    "fato_candidatura",
    "fato_bem_candidato",
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


def inspect_expected_gold_paths() -> list[dict]:
    objects = list_gold_objects()
    object_keys = [item["key"] for item in objects]

    return [
        {
            "table": table,
            "path": path,
            "has_objects": any(key.startswith(path) for key in object_keys),
        }
        for table, path in get_expected_gold_paths().items()
    ]


def read_gold_sample(key: str | None = None) -> dict | None:
    objects = list_gold_objects()
    readable_objects = [item for item in objects if not item["key"].endswith("/")]

    if not readable_objects:
        return None

    object_key = key or os.getenv("MINIO_GOLD_SAMPLE_KEY") or readable_objects[0]["key"]
    client = get_minio_client()
    response = client.get_object(Bucket=GOLD_BUCKET, Key=object_key)
    content = response["Body"].read()

    try:
        preview = content[:500].decode("utf-8")
    except UnicodeDecodeError:
        preview = "<arquivo binario: pre-visualizacao textual indisponivel>"

    return {
        "bucket": GOLD_BUCKET,
        "key": object_key,
        "size": len(content),
        "content_type": response.get("ContentType"),
        "preview": preview,
    }
