from io import BytesIO

from apps.core.settings import settings

from fastapi import UploadFile, HTTPException
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from apps.es.elasticsearch_logger import logger

class MinioClient:
    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket_name: str, secure: bool = True):
        self.bucket_name = bucket_name

        self.client = boto3.resource(
            's3',
            endpoint_url=endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=boto3.session.Config(signature_version='s3v4'),
            verify=secure
        )

    def list_buckets(self):
        try:
            return [bucket.name for bucket in self.client.buckets.all()]
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Error listing buckets: {e}")
            return []

    def create_bucket(self):
        try:
            if not any(bucket.name == self.bucket_name for bucket in self.client.buckets.all()):
                self.client.create_bucket(Bucket=self.bucket_name)
                logger.info(f"Bucket {self.bucket_name} created successfully.")
            else:
                logger.warning(f"Bucket {self.bucket_name} already exists.")
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Error creating bucket: {e}")

    def list_objects(self):
        try:
            bucket = self.client.Bucket(self.bucket_name)
            return [obj.key for obj in bucket.objects.all()]
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Error listing objects in {self.bucket_name}: {e}")
            return []

    def read_object(self, object_name: str) -> BytesIO:
        """
        Retrieve an object from the bucket and return its content as a BytesIO object.
        """
        try:
            obj = self.client.Object(self.bucket_name, object_name)
            response = obj.get()
            data = response['Body'].read()
            logger.info(f"Object {object_name} read successfully from {self.bucket_name}.")
            return BytesIO(data)
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Error reading object {object_name}: {e}")
            raise HTTPException(status_code=500, detail=f"Error reading file: {e}")

    def upload_object(self, object_name: str, file: UploadFile) -> str:
        try:
            file_content = file.file.read()
            self.client.Bucket(self.bucket_name).put_object(Key=f"{object_name}", Body=file_content)
            logger.info(f"Object {object_name} uploaded successfully to {self.bucket_name}.")
            return object_name
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Error uploading object {object_name}: {e}")
            raise HTTPException(status_code=500, detail=f"Error uploading file: {e}")

    def delete_object(self, object_name: str):
        try:
            self.client.Object(self.bucket_name, object_name).delete()
            logger.info(f"Object {object_name} deleted successfully from {self.bucket_name}.")
        except (BotoCoreError, ClientError) as e:
            logger.error(f"Error deleting object {object_name}: {e}")


minio_client = MinioClient(endpoint=settings.MINIO_URL, access_key=settings.MINIO_ACCESS_KEY,
                           secret_key=settings.MINIO_SECRET_KEY, bucket_name=settings.MINIO_BUCKET_NAME)
