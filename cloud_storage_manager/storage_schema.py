from pydantic import BaseModel, Field,model_validator

class AwsConfig(BaseModel):
    bucket_name: str = Field(..., description="AWS S3 bucket name")
    access_key_id: str = Field(..., description="AWS access key ID")
    secret_access_key: str = Field(..., description="AWS secret access key")
    region: str = Field(default="us-east-1", description="AWS region")

class GcpConfig(BaseModel):
    bucket_name: str = Field(..., description="GCP bucket name")
    credentials: dict = Field(..., description="GCP service account credentials")
    project_id: str = Field(..., description="GCP project ID")

class StorageConfig(BaseModel):
    aws: None| AwsConfig= Field(None, description="AWS configuration")
    gcp: None| GcpConfig = Field(None, description="GCP configuration")

    @model_validator(mode="after")
    def has_valid_provider(self) -> bool:
        return bool(self.aws or self.gcp)

    def validate_provider(self) -> None:
        if not self.has_valid_provider:
            raise ValueError("At least one storage provider (AWS or GCP) must be configured")