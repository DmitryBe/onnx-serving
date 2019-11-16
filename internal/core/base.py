from abc import ABC, abstractmethod 
from internal.config import *
from internal.log import create_logger
from internal.models.base import *

class ModelsCtrlBase(ABC):
    """
    models controller
    """    

    @abstractmethod
    def get_model(self, model_name, version: int = None) -> ModelBase:
        """
        returns: ModelBase or None
        """
        pass

    @abstractmethod
    def get_model_info(self, model_name) -> dict:
        """
        returns: dict {version: <int>}
        """
        pass

class ModelVersionCtrlBase(ABC):
    """
    model versions controller
    """

    @abstractmethod
    def get_model(self, version: int = None) -> ModelBase:
        """
        returns: ModelBase or None
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> dict:
        """
        returns: dict {version: <int>}
        """
        pass

class ModelsResolverBase(ABC):
    """
    manages model loaders for model platform
    """
    
    @abstractmethod
    def resolve(model_platform: str) -> ModelLoaderBase:
        """
        returns: ModelLoader
        """
        pass