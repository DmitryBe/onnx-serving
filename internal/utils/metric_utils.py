import time
from internal.config import *
from internal.monitoring.base import MonitoringBase
from internal.di_root import DIRoot

def measurable(metric_base_name, tags = []):
    """
    decorator factory
    returns decorator that collects metrics: success/failures/latency
    """
    monitoring = DIRoot.resolve(MonitoringBase)

    def measurable_decorator(func):        
        def wrapper(*args, **kwargs):
            start = time.time()
            try:            
                return func(*args, **kwargs)
            except:
                monitoring.increment('{}.failure'.format(metric_base_name), tags)
            finally:
                exec_time_ms = (time.time() - start) * 1000
                monitoring.increment('{}.success'.format(metric_base_name), tags)
                monitoring.histogram('{}.exec_time_ms'.format(metric_base_name), exec_time_ms, tags)
        return wrapper

    return measurable_decorator
