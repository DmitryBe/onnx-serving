import os
from sources.source_base import SourceBase


class FileSystemSource(SourceBase):

    def __init__(self, base_path):
        if os.path.exists(base_path) is False:
            raise FileNotFoundError('model not found in {}'.format(base_path))
        self.base_path = base_path

    def load(self) -> bytes:
        bytes_read = open(self.base_path, "rb").read()
        return bytes_read
