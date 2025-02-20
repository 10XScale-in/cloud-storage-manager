# Cloud Storage Manager

A Python package for seamlessly managing file uploads across AWS S3 and Google Cloud Storage platforms.

## Features

- Unified interface for AWS S3 and Google Cloud Storage
- Async operations support
- Pre-signed URL generation
- Easy file upload and deletion
- Type-safe configuration using Pydantic
- Comprehensive error handling
- Logging support

## Installation

```bash
pip install cloud-storage-manager
```

## Quick Start

### AWS S3 Example

```python
import asyncio
from cloud_storage_manager import CloudStorageFactory, StorageProvider, StorageConfig, AwsConfig

async def main():
    # Configure AWS
    config = StorageConfig(
        aws=AwsConfig(
            bucket_name="my-bucket",
            access_key_id="your-access-key",
            secret_access_key="your-secret-key",
            region="us-east-1"  # optional, defaults to us-east-1
        )
    )
    
    # Create storage client
    storage = CloudStorageFactory.get_storage(StorageProvider.AWS, config)
    
    # Upload file
    cloud_path = await storage.upload("local/path/file.txt", "remote/path/file.txt")
    
    # Generate temporary URL
    url = await storage.get_public_url(cloud_path, expiration=3600)  # 1 hour expiration
    
    # Delete file
    success = await storage.delete(cloud_path)

asyncio.run(main())
```

### Google Cloud Storage Example

```python
import asyncio
from cloud_storage_manager import CloudStorageFactory, StorageProvider, StorageConfig, GcpConfig

async def main():
    # Configure GCP
    config = StorageConfig(
        gcp=GcpConfig(
            bucket_name="my-bucket",
            project_id="your-project-id",
            credentials={
                # Your service account credentials dictionary
            }
        )
    )
    
    # Create storage client
    storage = CloudStorageFactory.get_storage(StorageProvider.GCP, config)
    
    # Upload file
    cloud_path = await storage.upload("local/path/file.txt", "remote/path/file.txt")
    
    # Generate temporary URL
    url = await storage.get_public_url(cloud_path, expiration=3600)  # 1 hour expiration
    
    # Delete file
    success = await storage.delete(cloud_path)

asyncio.run(main())
```

## Error Handling

The package provides specific exceptions for different types of errors:

```python
from cloud_storage_manager import UploadError, DeleteError, DownloadError

try:
    await storage.upload("file.txt", "remote/file.txt")
except UploadError as e:
    print(f"Upload failed: {e}")
```

## Configuration

### AWS Configuration
- `bucket_name`: Name of your S3 bucket
- `access_key_id`: AWS access key ID
- `secret_access_key`: AWS secret access key
- `region`: AWS region (optional, defaults to us-east-1)

### GCP Configuration
- `bucket_name`: Name of your GCP bucket
- `project_id`: Your GCP project ID
- `credentials`: Service account credentials dictionary

## Development

To contribute to the project:

```bash
# Clone the repository
git clone https://github.com/yourusername/cloud-storage-manager.git

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.