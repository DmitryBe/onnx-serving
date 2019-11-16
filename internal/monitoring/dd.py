import os
from datadog import DogStatsd
from internal.config import *
from internal.log import create_logger
from internal.monitoring.base import MonitoringBase

logger = create_logger(__name__)


class DDStatsDMonitoring(MonitoringBase):
    """
    monitoring client uses statsd service (dd)
    """

    def __init__(self):                
        self.stats = DogStatsd(host=DD_STATSD_HOST, port=DD_STATSD_PORT, constant_tags=DD_STATSD_CONSTANT_TAGS)
        logger.info(
            'DDStatsDMonitoring initialised with params: DD_STATSD_HOST={}, DD_STATSD_PORT={}, DD_STATSD_PREF={}, DD_STATSD_CONSTANT_TAGS={}'.format(
                DD_STATSD_HOST, 
                DD_STATSD_PORT, 
                DD_STATSD_PREF, 
                DD_STATSD_CONSTANT_TAGS
            )
        )

    def increment(self, metric_name, tags=[]):
        try:            
            self.stats.increment('{}.{}'.format(DD_STATSD_PREF, metric_name), tags=tags)
        except Exception as ex:
            logger.warn(str(ex))

    def histogram(self, metric_name, value, tags=[]):
        try:            
            self.stats.histogram('{}.{}'.format(DD_STATSD_PREF, metric_name), value, tags=tags)
        except Exception as ex:
            logger.warn(str(ex))

    def alert(self, alert_title, alert_message, tags=[]):
        try:        
            self.stats.event(alert_title, alert_message, tags=tags)
        except Exception as ex:
            logger.warn(str(ex))

    def gauge(self, metric_name, value, tags=[]):
        try:            
            self.stats.gauge('{}.{}'.format(DD_STATSD_PREF, metric_name), value, tags=tags)
        except Exception as ex:
            logger.warn(str(ex))

    def count(self, metric_name, value, tags=[]):
        try:            
            self.stats.count('{}.{}'.format(DD_STATSD_PREF, metric_name), value, tags=tags)
        except Exception as ex:
            logger.warn(str(ex))
