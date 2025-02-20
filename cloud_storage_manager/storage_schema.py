from pydantic import BaseModel


class AwsConfig(BaseModel):
    bucket_name: str
    access_key_id: str
    secret_access_key: str


class GcpConfig(BaseModel):
    bucket_name: str
    credentials: dict


class StorageConfig(BaseModel):
    aws: AwsConfig | None = None
    gcp: GcpConfig | None = None
