from abc import ABC, abstractmethod
from pathlib import Path

from .storage_schema import StorageConfig


class BaseCloudStorage(ABC):
    """Abstract base class for cloud storage operations.

    This class defines the interface for cloud storage operations that should be
    implemented by specific cloud provider classes.

    Attributes:
        config (StorageConfig): Configuration object for the cloud storage.
    """

    def __init__(self, config: StorageConfig):
        """Initialize the cloud storage interface.

        Args:
            config (StorageConfig): Configuration object for the cloud storage.
        """
        self.config = config

    @abstractmethod
    async def upload(self, file_path: Path | str, cloud_path: str) -> str:
        """Upload a file to cloud storage.

        Args:
            file_path (Path | str): Local path to the file to be uploaded.
            cloud_path (str): Destination path in cloud storage.

        Returns:
            str: The URL or path of the uploaded file in cloud storage.

        Raises:
            NotImplementedError: This is an abstract method that must be implemented.
        """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    async def delete(self, cloud_path: str) -> bool:
        """Delete a file from cloud storage.

        Args:
            cloud_path (str): Path to the file in cloud storage to be deleted.

        Returns:
            bool: True if deletion was successful, False otherwise.

        Raises:
            NotImplementedError: This is an abstract method that must be implemented.
        """
        raise NotImplementedError("Method not implemented")

    @abstractmethod
    async def get_public_url(self, cloud_path: str, expiration: int = 3600) -> str:
        """Generate a public/signed URL for the file.

        Args:
            cloud_path (str): Path to the file in cloud storage.
            expiration (int, optional): URL expiration time in seconds. Defaults to 3600.

        Returns:
            str: Public/signed URL for accessing the file.

        Raises:
            NotImplementedError: This is an abstract method that must be implemented.
        """
        raise NotImplementedError("Method not implemented")
