import os
import boto3
import urllib.request as request
import zipfile
from textSummarizer.logging import logger
from textSummarizer.utils.common import get_size
from pathlib import Path
from textSummarizer.entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            s3 = boto3.client(
                's3',
                aws_access_key_id=self.config.access_key,
                aws_secret_access_key=self.config.secret_access_key,
                region_name=self.config.region
            )
            bucket_name = self.config.bucket_name
            s3_file_key= self.config.object_key
            local_file_path= self.config.local_data_file
            
            try:
                s3.download_file(bucket_name, s3_file_key, local_file_path)
                logger.info(f"File {s3_file_key} downloaded to {local_file_path}")
            except BoxValueError:
                raise ValueError("Unable to download file from s3")
        else:
            logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")

    def extract_zip_file(self):
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)