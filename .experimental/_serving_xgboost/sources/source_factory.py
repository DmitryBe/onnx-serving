from sources.source_base import SourceBase
from sources.file_system_source import FileSystemSource
from tensorflow_serving.config import model_server_config_pb2


class SourceFactory:

    @staticmethod
    def get(model_config: model_server_config_pb2.ModelConfig) -> SourceBase:

        base_path = model_config.base_path
        if base_path.startswith("file:/"):
            model_local_path = base_path.replace('file:/', '')
            loader = FileSystemSource(model_local_path)
        else:
            raise NotImplemented('storage type is not supported')

        return loader
