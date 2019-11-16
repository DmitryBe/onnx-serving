from google.protobuf import text_format as tf
from tensorflow_serving.config import model_server_config_pb2
from internal.config import *
from internal.log import create_logger
from internal.di_root import DIRoot
from internal.core.base import *
from internal.core.model_version_ctrl import ModelVersionCtrl
from internal.sources.base import *
from internal.sources.s3 import S3Source


logger = create_logger(__name__)


class ModelsCtrl(ModelsCtrlBase):
    """
    """

    def __init__(self, model_config_path: str):
        """
        """
                
        # dict: (model_name: str) -> ModelVersionCtrl
        self.loaded_models = {}
        
        source_factory = DIRoot.resolve(SourceFactoryBase)
        source = source_factory.resolve(model_config_path)
        models_config = self._load_model_config(model_config_path, source)
        # for each model_config create ModelVersionCtrl        
        for model_cfg in models_config.model_config_list.config:            
            self.loaded_models[model_cfg.name] = ModelVersionCtrl(source, model_cfg)

    def get_model_info(self, model_name: str) -> dict:
        """
        returns model information (meta)
        """
        model_version_ctrl = self.loaded_models.get(model_name)
        if model_version_ctrl is None:
            raise Exception("model {} is not registered".format(model_name))
        model_info = model_version_ctrl.get_model_info()
        return model_info

    def get_model(self, model_name: str, version: int = None) -> ModelBase:
        """
        return: ModelBase or None
        """
        model_version_ctrl = self.loaded_models.get(model_name)
        if model_version_ctrl is None:
            raise Exception("model {} is not registered".format(model_name))
        # model version returns active model (latest|specific) according to serving policy
        return model_version_ctrl.get_model(version)

    def _load_model_config(self, model_config_path: str, source: SourceBase) -> model_server_config_pb2.ModelServerConfig:
        """
        returns ModelServerConfig
        """
        # load and parse        
        model_config_data = source.load_object(model_config_path)                
        models_config = model_server_config_pb2.ModelServerConfig()
        tf.Parse(model_config_data, models_config)

        return models_config