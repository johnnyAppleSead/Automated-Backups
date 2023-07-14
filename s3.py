import boto3
from config_util import ConfigUtil
import json

from engine_util import Util


class S3:
    def __init__(self, bucket, keys=None):
        self.bucket = bucket
        self.util = Util()

        self.keys = keys
        if keys is None:
            target_dirs = ConfigUtil().get_value("target_directories")
            s3 = target_dirs["s3"]
            if not self.util.empty(s3):
                creds = s3["credentials"]
                if not self.util.empty(creds):
                    self.util.log("Attempting to open S3 config file")
                    file = open(creds, 'r')
                    self.keys = json.loads(file.read())
                    file.close()
                    self.util.log("S3 config file successfully loaded")

    def upload(self, file):
        try:
            self.client = boto3.client('s3',
                                       aws_access_key_id=self.keys["access_key_id"],
                                       aws_secret_access_key=self.keys["secret_key"])

            response = self.client.upload_file(file.source, self.bucket, file.target_file_name)

        except:
            self.util.log("AWS Error Occurred")


