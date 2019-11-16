import re
from internal.log import create_logger
from internal.sources.base import *
from internal.sources.s3 import S3Source

logger = create_logger(__name__)

class SourceFactory(SourceFactoryBase):
    """    
    """

    SOURCE_PROVIDERS = {
        "s3": S3Source        
    }

    @staticmethod
    def resolve(path: str) -> SourceBase:
        """
        returns proper source for specified path
        """        
        r = re.match('(\w+):', path)
        protocol = r.group(1)

        source_class = SourceFactory.SOURCE_PROVIDERS.get(protocol)
        if source_class is None:            
            raise Exception("cannot identify source provider for path {}".format(path))
            
        # create source instance
        return source_class()

    def register(protocol: str, source_provider: SourceBase):
        """
        registers source for protocol
        (can be used for debugging)
        """
        logger.info('register source: {} -> {}'.format(protocol, type(source_provider)))
        SourceFactory.SOURCE_PROVIDERS[protocol] = source_provider