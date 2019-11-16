from abc import ABC, abstractmethod 
from internal.sources.base import SourceBase
from tensorflow_serving.config import model_server_config_pb2
from tensorflow_serving.apis.predict_pb2 import PredictResponse, PredictRequest

class ModelBase(ABC):
    """
    abstract model serving 
    """    

    @abstractmethod
    def predict(self, request: PredictResponse) -> PredictResponse:
        pass


class ModelLoaderBase(ABC):
    """
    abstract model loader
    """    

    @abstractmethod
    def load_model(self, source: SourceBase, model_cfg: model_server_config_pb2.ModelConfig) -> (int, ModelBase):
        """
        returns: version, model_serving
        """
        pass