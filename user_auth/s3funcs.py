import os  # type:ignore
import boto3  # type:ignore
import yaml  # type:ignore
from botocore.exceptions import ClientError  # type:ignore

AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "maximusml")

s3_client = boto3.client(
    "s3",
    region_name=AWS_DEFAULT_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

s3_resource = boto3.resource(
    "s3",
    region_name=AWS_DEFAULT_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def create_user_folder(username):
    folder_name = f"{username}/"
    try:
        s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=folder_name)
        print(
            f"Folder '{folder_name}' created successfully in bucket '{S3_BUCKET_NAME}'"
        )
    except ClientError as e:
        print(f"Error creating folder: {e}")


def save_yaml_to_s3(config):
    YAML_KEY = "credentials.yaml"
    yaml_data = yaml.dump(config, default_flow_style=False)

    try:
        s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=YAML_KEY, Body=yaml_data)
        print(f"YAML file saved successfully to {S3_BUCKET_NAME}/{YAML_KEY}")
    except ClientError as e:
        print(f"Error saving YAML to S3: {e}")


def load_yaml_from_s3():
    YAML_KEY = "credentials.yaml"
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=YAML_KEY)
        yaml_data = response["Body"].read().decode("utf-8")
        config = yaml.safe_load(yaml_data)
        return config
    except ClientError as e:
        print(f"Error loading YAML from S3: {e}")
        return None
