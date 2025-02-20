from enum import Enum

from .aws_s3_storage import AWSClientStorage
from .base_storage import BaseCloudStorage
from .gcp_storage import GcpClientStorage
from .storage_schema import StorageConfig


class StorageProvider(Enum):
    """Enumeration of supported cloud storage providers."""

    AWS = "aws"
    GCP = "gcp"


class CloudStorageFactory:
    """Factory class for creating cloud storage client instances.

    This class manages the mapping between storage providers and their
    implementations, providing a centralized way to instantiate storage clients.

    Attributes:
        _providers: A dictionary mapping StorageProvider enums to their
            corresponding implementation classes.

    Example:
        >>> config = StorageConfig(...)
        >>> storage = CloudStorageFactory.get_storage(StorageProvider.AWS, config)
        >>> storage.upload_file(...)
    """

    _providers: dict[StorageProvider, type[BaseCloudStorage]] = {
        StorageProvider.AWS: AWSClientStorage,
        StorageProvider.GCP: GcpClientStorage,
    }

    @classmethod
    def get_storage(cls, provider: StorageProvider, config: StorageConfig) -> BaseCloudStorage:
        """Creates and returns a cloud storage instance for the specified provider.

        Args:
            provider: The cloud storage provider to use (AWS or GCP).
            config: Configuration parameters for initializing the storage client.

        Returns:
            A concrete implementation of BaseCloudStorage for the specified provider.

        Raises:
            ValueError: If the specified provider is not supported.
        """
        storage_class = cls._providers.get(provider)
        if not storage_class:
            raise ValueError(f"Unsupported storage provider: {provider}")
        return storage_class(config)
