from tensorflow_serving.config import model_server_config_pb2
from internal.config import *
from internal.log import create_logger
from internal.models.base import ModelLoaderBase, ModelBase
from internal.core.base import *
from internal.sources.base import *
from internal.di_root import DIRoot

logger = create_logger(__name__)


class ModelVersionCtrl(ModelVersionCtrlBase):
    """
    """

    def __init__(self, source: SourceBase, model_cfg: model_server_config_pb2.ModelConfig):
        """
        """        
        models_resolver = DIRoot.resolve(ModelsResolverBase)
        model_loader = models_resolver.resolve(model_cfg.model_platform)
        model_version, model_serving = model_loader.load_model(source, model_cfg)
        self.model_info = {
            'version': model_version
        }
        self.model_serving = model_serving
        
    def get_model(self, version: int = None) -> ModelBase:
        """
        returns model
        """
        return self.model_serving

    def get_model_info(self) -> dict:
        """
        returns model_info (dict)
        """
        return self.model_info