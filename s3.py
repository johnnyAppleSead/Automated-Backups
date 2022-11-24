import boto3
from botocore.exceptions import ClientError
import os
from config_util import ConfigUtil
from engine_util import empty, log
import json


class S3:
    def __init__(self, bucket, keys=None):
        self.bucket = bucket

        self.keys = keys
        if keys is None:
            target_dirs = ConfigUtil().get_value("target_directories")
            s3 = target_dirs["s3"]
            if not empty(s3):
                creds = s3["credentials"]
                if not empty(creds):
                    log("Attempting to open S3 config file", "HIGH")
                    file = open(creds, 'r')
                    self.keys = json.loads(file.read())
                    file.close()
                    log("S3 config file successfully loaded.", "HIGH")

    def upload(self, file):
        try:
            self.client = boto3.client('s3',
                                       aws_access_key_id=self.keys["access_key_id"],
                                       aws_secret_access_key=self.keys["secret_key"])

            response = self.client.upload_file(file.source, self.bucket, file.target_file_name)

        except:
            log("AWS Error Occurred", "HIGH")


