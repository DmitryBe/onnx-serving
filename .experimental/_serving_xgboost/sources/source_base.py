import abc


class SourceBase(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def load(self):
        raise NotImplemented('method is not implemented')
