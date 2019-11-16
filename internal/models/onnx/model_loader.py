from tensorflow_serving.config import model_server_config_pb2
from internal.utils.url_utils import urljoin
from internal.sources.base import SourceBase
from internal.models.base import ModelBase, ModelLoaderBase
from internal.models.onnx.model import OnnxModel

class OnnxModelLoader(ModelLoaderBase):
    """
    onnx serving loader
    """
    def load_model(self, source: SourceBase, model_cfg: model_server_config_pb2.ModelConfig) -> (int, ModelBase):
        """
        """
        # expected model name (probably shoul be param)
        model_object_name = 'model.onnx'
        
        # base model folder (example: s3://bucket/tf/project/model-name)
        base_path = model_cfg.base_path
        # int (example: 1)
        last_version = source.get_last_version(base_path)
        # example: s3://bucket/tf/project/model-name/1
        model_version_path = urljoin(base_path, last_version)        
        # example: s3://bucket/tf/project/model-name/1/model.onnx
        model_object_path = urljoin(model_version_path, model_object_name)
        if source.is_object_exists(model_object_path) is False:
            raise Exception('model object cannot be found at {}'.format(model_object_path))
        
        # load model object
        data_bytes = source.load_object(model_object_path)
        model_serving = OnnxModel(data_bytes)
        return (last_version, model_serving)
