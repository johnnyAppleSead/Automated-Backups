import boto3
from config_util import ConfigUtil
import json

from engine_util import Util


class S3:
    def __init__(self, bucket, keys=None):
        self.client = None
        self.bucket = bucket
        self.util = Util()

        self.keys = keys
        if self.keys is None:
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

    def connect(self):
        self.client = boto3.client('s3',
                                   aws_access_key_id=self.keys["access_key_id"],
                                   aws_secret_access_key=self.keys["secret_key"])

        self.util.log("S3 Connection Created", "HIGH")

    def close(self):
        self.util.log("S3 Connection Closed", "HIGH")
        self.client.close()

    def delete(self, folder):
        try:
            self.connect()


        except:
            self.util.log("AWS error occurred deleting S3 folder", folder)

    def cleaner(self, days):
        if days < 0:
            days = days * -1

        self.connect()
        objects = self.client.list_objects_v2(Bucket=self.bucket)

        for object in objects['Contents']:
            print(object)


    def upload(self, file, folder):
        try:
            self.connect()
            response = self.client.upload_file(file.source, self.bucket, folder + "/" + file.target_file_name)
            self.close()

            return response
        except:
            self.util.log("AWS error occurred uploading " + file + " into S3 folder " + folder, "HIGH")
