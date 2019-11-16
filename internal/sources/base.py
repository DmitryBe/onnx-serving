from abc import ABC, abstractmethod 

class SourceBase(ABC):
    """
    abstract source (s3, file, ...)
    """    

    @abstractmethod
    def is_object_exists(self, path) -> bool:        
        '''
        path s3://<bucket>/path/ exists
        returns True if object exists
        '''
        pass

    @abstractmethod
    def list_versions(self, path, last_n = 1) -> []:
        """
        returns last n_versions
        """
        pass

    @abstractmethod
    def get_last_version(self, path) -> int:
        """
        returns last found version
        """
        pass

    @abstractmethod
    def load_object(self, path) -> bytes:
        """
        returns object as bytes
        """
        pass

class SourceFactoryBase(ABC):
    """
    """

    @abstractmethod
    def resolve(path: str) -> SourceBase:
        pass

    @abstractmethod
    def register(protocol: str, source_provider: SourceBase):
        pass