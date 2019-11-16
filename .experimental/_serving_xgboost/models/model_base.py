import abc
import numpy as np


class ModelBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def predict(self, features: np.ndarray) -> np.ndarray:
        raise NotImplemented('method is not implemented')
