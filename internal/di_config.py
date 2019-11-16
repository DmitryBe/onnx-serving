from internal.config import *
from internal.log import create_logger
from internal.di_root import DIRoot

from internal.core.base import *
from internal.core.models_ctrl import ModelsCtrl
from internal.core.models_resolver import ModelsResolver
from internal.sources.factory import SourceFactory
from internal.sources.base import *
from internal.sources.s3 import S3Source
from internal.monitoring.base import MonitoringBase
from internal.monitoring.dd import DDStatsDMonitoring

logger = create_logger(__name__)

def configure_di():
    """
    config DI 
    """
    logger.info("configuring DI")
    DIRoot.register(ModelsCtrlBase, lambda model_config_name: ModelsCtrl(model_config_name))
    DIRoot.register(SourceFactoryBase, SourceFactory()) # singleton
    DIRoot.register(ModelsResolverBase, ModelsResolver())
    DIRoot.register(MonitoringBase, DDStatsDMonitoring())
    