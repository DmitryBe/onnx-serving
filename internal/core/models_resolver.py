from internal.config import *
from internal.log import create_logger
from internal.core.base import *
from internal.models.base import *
from internal.models.onnx.model_loader import OnnxModelLoader

logger = create_logger(__name__)

class ModelsResolver(ModelsResolverBase):
    """
    manages model loaders for model platform
    """

    LOADERS = {
        "onnx": OnnxModelLoader
    }

    @staticmethod
    def resolve(model_platform: str) -> ModelLoaderBase:
        logger.info("create model loader for platform {}".format(model_platform))
        model_loader_type = ModelsResolver.LOADERS.get(model_platform)
        if model_loader_type is None:
            raise Exception("cannot find ModelLoader for platform {}".format(model_platform))
        # returns instance of model loader
        return model_loader_type()
