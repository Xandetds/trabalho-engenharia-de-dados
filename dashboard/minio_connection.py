import os
import boto3
from botocore.client import Config
from dotenv import load_dotenv

load_dotenv()


def get_minio_client():
    endpoint = os.getenv("MINIO_DASHBOARD_ENDPOINT", "http://localhost:9020")
    access_key = os.getenv("MINIO_ACCESS_KEY")
    secret_key = os.getenv("MINIO_SECRET_KEY")

    return boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )


def list_buckets():
    client = get_minio_client()
    response = client.list_buckets()
    return [bucket["Name"] for bucket in response.get("Buckets", [])]
