import os

import requests
import asyncio
import boto3
import hashlib
from smart_open import open as s_open
from multiprocessing.dummy import Pool as ThreadPool
from loguru import logger


MEDIA_S3_AWS_ACCESS_KEY_ID = os.environ.get("MEDIA_S3_AWS_ACCESS_KEY_ID")
MEDIA_S3_AWS_SECRET_ACCESS_KEY = os.environ.get("MEDIA_S3_AWS_SECRET_ACCESS_KEY")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")


class MediaS3(object):
    def __init__(self):
        self.s3 = self._s3_client()
        self.bucket_name = "dropship-lead-crawler"

    @staticmethod
    def _s3_client():
        """Get session variable for work with S3"""
        for _ in range(1, 51):
            try:
                session = boto3.Session(
                    aws_access_key_id=MEDIA_S3_AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=MEDIA_S3_AWS_SECRET_ACCESS_KEY,
                )
                s3 = session.client("s3")
                return s3
            except Exception as e:
                logger.warning(f"Fail connection to get boto3 client::try {_}")
                logger.exception(e)


    def thread_save_on_s3(self, filepath, html_str, s3):
        """
        """

        try:
            s3.put_object(
                Bucket=self.bucket_name,
                Key=filepath,
                Body=html_str,
                ContentType='text/html'
            )
            # s3.upload_file(filename, self.bucket_name, object_name)
            return True
        except Exception as e:
            logger.exception(f"Error saving data: {e}")
            print(e)
            return False

    def thread_read_from_s3(self, filepath):
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=filepath)
            html_str = response['Body'].read().decode('utf-8')
            return html_str
        except Exception as e:
            logger.exception(f"Error reading data from S3: {e}")
            return None

    def save_on_s3_thread(self, values):
        """
        Save media to S3 and return the generated link.
        """
        with ThreadPool(15) as p:
            list_s3 = p.map(self.thread_save_on_s3, values)
        return list_s3

    def upload_to_s3(self, filepath, html_str):
        result_s3_link = self.thread_save_on_s3(filepath, html_str, self.s3)
        return result_s3_link

    async def async_upload_to_s3(self, filepath, html_str):
        result_s3_link = await self.async_thread_save_on_s3(filepath, html_str, self.s3)
        return result_s3_link

    async def async_thread_save_on_s3(self, filepath, html_str, s3):
        if not html_str:
            return False
        try:
            await asyncio.to_thread(
                s3.put_object,
                Bucket=self.bucket_name,
                Key=filepath,
                Body=html_str,
                ContentType='text/html'
            )
            return True
        except Exception as e:
            logger.exception(f"Error saving data: {e}")
            print(e)
            return False
