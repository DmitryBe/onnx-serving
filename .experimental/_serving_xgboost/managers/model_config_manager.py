import logging as logger
from google.protobuf import text_format as tf
from tensorflow_serving.config import model_server_config_pb2


class ModelConfigManager:

    @staticmethod
    def load(path: str) -> model_server_config_pb2.ModelConfig:
        """
        read model config in tf format https://www.tensorflow.org/tfx/serving/serving_config
        """
        logger.info('loading model config: {}'.format(path))

        # read serving config
        config_str = open(path)\
            .read()

        # parse
        model_server_config = model_server_config_pb2.ModelServerConfig()
        tf.Parse(config_str, model_server_config)
        
        

        return model_server_config

