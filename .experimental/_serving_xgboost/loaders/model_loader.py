import os
import time
from tensorflow_serving.config import model_server_config_pb2
from models.model_base import ModelBase
from models.lightgbm_model import LightGBMModel


class ModelLoader:

    @staticmethod
    def load(model_config: model_server_config_pb2.ModelConfig, model_bytes: bytes) -> ModelBase:

        if model_config.model_platform == 'lightgbm':
            return ModelLoader.load_lightgbm(model_bytes)
        else:
            raise NotImplementedError('model_platform {} is not supported'.format(model_config.model_platform))

    @staticmethod
    def load_lightgbm(model_bytes: bytes) -> ModelBase:
        model_path = ModelLoader.save_model_to_tmp_file(model_bytes)
        model = LightGBMModel(model_path)
        os.remove(model_path)
        return model

    @staticmethod
    def save_model_to_tmp_file(model_bytes: bytes, tmp_folder: str = '/tmp') -> str:

        tmp_model_path = '{}/model-{}'.format(tmp_folder, int(time.time()))
        with open(tmp_model_path, 'wb') as f:
            f.write(model_bytes)

        return tmp_model_path

