import boto3
import re
import time
from urllib.parse import urlparse, urljoin
from internal.log import create_logger
from internal.sources.base import SourceBase

logger = create_logger(__name__)

class S3Source(SourceBase):
    """
    # bucket='grab-ds-users', key='dmitry.b/onnx-serving/test-model/serving_conf'
    """
    _s3_client = boto3.client('s3')
        
    def is_object_exists(self, path) -> bool:        
        '''
        path s3://<bucket>/path
        returns True if object exists
        '''        
        bucket, key = self._parse_path(path)
        r = S3Source._s3_client.list_objects_v2(
            Bucket=bucket, 
            Prefix=key, 
            Delimiter='/'
        )
        return r['KeyCount'] != 0

    def get_last_version(self, path) -> int:
        """
        returns last version
        """
        return self.list_versions(path)[0]

    def list_versions(self, path, last_n = 1) -> []:
        """
        returns last found version (must be int)
        """
        bucket, key = self._parse_path(path)
        key = self._fix_key(key, False)

        last_pref = ''
        _continue = True
        while _continue:
            r = S3Source._s3_client.list_objects_v2(
                Bucket=bucket, 
                Prefix=key, 
                Delimiter='/',
                MaxKeys=100, 
                StartAfter=last_pref           
            )
            if 'CommonPrefixes' in r:
                objects = r['CommonPrefixes']
                last_object = objects[-1]
                last_pref = last_object['Prefix']
            else:
                # no keys found
                pass

            # if not keys remained
            if 'NextContinuationToken' not in r:
                _continue = False

        if last_pref != '':
            last_version = int(last_pref.replace(key, '').replace('/', ''))
        else:
            last_version = None

        # returns last version
        return [last_version]

    def load_object(self, path) -> bytes:
        """
        returns object as bytes
        """
        bucket, key = self._parse_path(path)
        key = self._fix_key(key, True)
        r = S3Source._s3_client.get_object(Bucket=bucket, Key=key)
        return r['Body'].read()        

    def _parse_path(self, path) -> (str, str):
        r = re.match('(\w+):\/\/([\w\-\_]+)\/(.+)', path)
        bucket = r.group(2)
        key = r.group(3)
        return bucket, key

    def _fix_key(self, key, is_object = False):
        """
        key have not to:
        1. not start with /
        2. finish with /
        """
        key = key[1:] if key[0] == '/' else key
        if is_object is False:
            key = '{}/'.format(key) if key[-1] != '/' else key
        return key