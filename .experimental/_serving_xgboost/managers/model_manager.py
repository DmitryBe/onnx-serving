import logging as logger
from loaders.model_loader import ModelLoader
from sources.source_factory import *
from models.model_base import ModelBase
from tensorflow_serving.config import model_server_config_pb2


class ModelManager:

    def __init__(self, model_server_config: model_server_config_pb2.ModelConfig) -> None:

        # dict of loaded models
        self.loaded_models = {}

        # list of model config
        model_config_list = [m for m in model_server_config.model_config_list.config]

        for model_config in model_config_list:
            source = SourceFactory.get(model_config)
            model_bytes = source.load()
            model = ModelLoader.load(model_config, model_bytes)
            self.loaded_models[model_config.name] = model

    def get_model(self, name) -> ModelBase:
        """
        :return: ModelBase or None
        """
        return self.loaded_models.get(name)
