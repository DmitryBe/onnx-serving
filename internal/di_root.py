from internal.config import *
from internal.log import create_logger
from internal.core.base import *
from internal.models.base import *
from internal.sources.base import *

logger = create_logger(__name__)

class DIRoot:
    """
    dependency resolver
    """

    DI_CONTAINER = {}

    @staticmethod
    def resolve(type, *args, **kwargs):
        """
        returns instance of type
        """
        r = DIRoot.DI_CONTAINER.get(type)
        if r is None:
            raise Exception("resolver for type {} not found".format(type))
        if callable(r):
            # is factory function
            return r(*args, **kwargs)
        else:
            # in class instance
            return r

    @staticmethod
    def register(type, provider):
        """
        registers provider for type
        """
        logger.info("register type {} -> {}".format(type, provider))
        DIRoot.DI_CONTAINER[type] = provider