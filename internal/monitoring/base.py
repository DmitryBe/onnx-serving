from abc import ABC, abstractmethod 


class MonitoringBase(ABC):

    @abstractmethod
    def increment(self, metric_name, tags=[]):
        pass

    @abstractmethod
    def histogram(self, metric_name, value, tags=[]):
        pass

    @abstractmethod
    def alert(self, alert_title, alert_message, tags=[]):
        pass

    @abstractmethod
    def gauge(self, metric_name, value, tags=[]):
        pass

    @abstractmethod
    def count(self, metric_name, value, tags=[]):
        pass
