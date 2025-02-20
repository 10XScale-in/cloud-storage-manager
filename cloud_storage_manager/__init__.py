"""
Cloud Storage Manager Package
"""
import logging
from .storage_provider import StorageProvider
logger = logging.getLogger(__name__)

__all__ = ['StorageProvider',"logger"]