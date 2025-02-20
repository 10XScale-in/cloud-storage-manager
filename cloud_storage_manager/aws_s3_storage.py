from pathlib import Path

import aioboto3

from . import logger
from .base_storage import BaseCloudStorage
from .exceptions import DeleteError, DownloadError, UploadError
from .storage_schema import StorageConfig


class AWSClientStorage(BaseCloudStorage):
    """
    AWSClientStorage is a class for interacting with AWS S3 storage.
    It provides methods to upload, delete, and generate pre-signed URLs for files in an S3 bucket.
    Attributes:
        session (aioboto3.Session): The boto3 session for AWS S3 interactions.
        bucket (str): The name of the S3 bucket.
    Methods:
        __init__(config: StorageConfig):
            Initializes the AWS S3 storage client with the provided configuration.
        upload(file_path: Path | str, cloud_path: str) -> str:
            Uploads a file to the S3 bucket.
        delete(cloud_path: str) -> bool:
            Deletes a file from the S3 bucket.
        get_public_url(cloud_path: str, expiration: int = 3600) -> str:
            Generates a pre-signed URL for temporary access to a private S3 object.
        upload_file(file_path: Path | str, cloud_path: str) -> str:
            Internal method to handle file upload to S3.
        delete_file(cloud_path: str) -> bool:
            Internal method to handle file deletion from S3.
    """

    def __init__(self, config: StorageConfig):
        """Initialize AWS S3 storage client.

        Args:
            config (StorageConfig): Configuration containing AWS credentials and settings
                Must include aws.access_key_id, aws.secret_access_key, and aws.bucket_name

        Raises:
            ValueError: If AWS configuration is missing
        """
        if not config.aws:
            raise ValueError("AWS configuration is required")
        super().__init__(config)
        self.session = aioboto3.Session(
            aws_access_key_id=config.aws.access_key_id,
            aws_secret_access_key=config.aws.secret_access_key,
        )
        self.bucket = config.aws.bucket_name
        logger.info(f"AWSClientStorage initialized with bucket: {self.bucket}")

    async def upload(self, file_path: Path | str, cloud_path: str) -> str:
        """Upload a file to S3 bucket.

        Args:
            file_path (Path | str): Local file path to upload
            cloud_path (str | None): Target path in S3. If None, uses filename

        Returns:
            str: The S3 object path

        Raises:
            UploadError: If upload fails
        """

        logger.info(f"Starting upload of {file_path} to s3://{self.bucket}/{cloud_path}")
        return await self.upload_file(file_path, cloud_path)

    async def delete(self, cloud_path: str) -> bool:
        """Delete a file from S3 bucket.

        Args:
            cloud_path (str): S3 object path to delete

        Returns:
            bool: True if deletion successful

        Raises:
            DeleteError: If deletion fails
        """
        logger.info(f"Deleting s3://{self.bucket}/{cloud_path}")
        return await self.delete_file(cloud_path)

    async def get_public_url(self, cloud_path: str, expiration: int = 3600) -> str:
        """Generate a pre-signed URL for temporary access to a private S3 object.

        Args:
            cloud_path (str): S3 object path
            expiration (int): URL validity duration in seconds (default: 1 hour)

        Returns:
            str: Pre-signed URL for the object

        Raises:
            DownloadError: If URL generation fails
        """
        logger.info(f"Generating pre-signed URL for s3://{self.bucket}/{cloud_path}")
        async with self.session.client("s3") as s3:
            try:
                url = await s3.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": self.bucket, "Key": cloud_path},
                    ExpiresIn=expiration,
                )
                logger.debug(f"Generated pre-signed URL (expires in {expiration}s)")
                return url
            except Exception as e:
                logger.error(f"Failed to generate pre-signed URL: {e}")
                raise DownloadError(f"Failed to generate pre-signed URL: {e}")

    # Helper methods
    async def upload_file(self, file_path: Path | str, cloud_path: str) -> str:
        """Internal method to handle file upload to S3."""
        async with self.session.client("s3") as s3:
            try:
                if isinstance(file_path, str):
                    file_path = Path(file_path)

                with file_path.open("rb") as file_obj:
                    await s3.upload_fileobj(file_obj, self.bucket, cloud_path)
                    logger.debug(f"Successfully uploaded to s3://{self.bucket}/{cloud_path}")
                return cloud_path
            except Exception as e:
                logger.error(f"Upload failed: {e}")
                raise UploadError(f"Failed to upload file to S3: {e}")

    async def delete_file(self, cloud_path: str) -> bool:
        """Internal method to handle file deletion from S3."""
        async with self.session.client("s3") as s3:
            try:
                await s3.delete_object(Bucket=self.bucket, Key=cloud_path)
                logger.debug(f"Successfully deleted s3://{self.bucket}/{cloud_path}")
                return True
            except Exception as e:
                logger.error(f"Deletion failed: {e}")
                raise DeleteError(f"Failed to delete file from S3: {e}")
