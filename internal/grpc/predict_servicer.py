import time
import numpy as np
import multiprocessing
from internal.config import *
from internal.log import create_logger
from internal.utils.tensor_utils import *
from internal.utils.metric_utils import measurable
from internal.core.base import ModelsCtrlBase
from internal.di_root import DIRoot
from internal.monitoring.base import MonitoringBase

logger = create_logger(__name__)

# import generated artifacts
import tensorflow_serving.apis.prediction_service_pb2_grpc as ps
from tensorflow_serving.apis.predict_pb2 import PredictResponse, PredictRequest
from tensorflow_serving.apis.prediction_service_pb2_grpc import add_PredictionServiceServicer_to_server, PredictionServiceStub
from tensorflow_serving.apis.get_model_metadata_pb2 import GetModelMetadataRequest, GetModelMetadataResponse
from tensorflow_serving.apis.model_pb2 import ModelSpec
from google.protobuf.wrappers_pb2 import Int64Value

from internal.di_config import configure_di

# model controller (initialised for each worker in multiprocessing.Pool)
_models_ctrl = None

def _predict(model_name, request):
    '''
    perform inference (multiprocessing.Pool)
    '''
    target_model = _models_ctrl.get_model(model_name)
    return target_model.predict(request)

def _get_metadata(model_name):
    '''
    get model metadata (multiprocessing.Pool)
    '''
    return _models_ctrl.get_model_info(model_name)

def _initialize_worker():
    '''
    initialise worker process
    '''
    global _models_ctrl
    logger.info('initialising worker')
    configure_di()    
    _models_ctrl = DIRoot.resolve(ModelsCtrlBase, MODEL_SERVER_CONFIG_PATH)    


class PredictionServiceServicer(ps.PredictionServiceServicer):
    """
    servicer for tensorflow_serving.apis.prediction_service
    """

    def __init__(self, n_processes: int = 8):
        logger.info("creating ModelsCtrl using {}".format(MODEL_SERVER_CONFIG_PATH))
        self.monitoring = DIRoot.resolve(MonitoringBase)
        self.worker_pool = multiprocessing.Pool(
            processes=n_processes,
            initializer=_initialize_worker
        )
    
    def GetModelMetadata(self, request: GetModelMetadataRequest, context):
        '''
        get model metadata
        '''
        # get model name
        model_spec = request.model_spec
        if model_spec is None:
            raise Exception("model_spec is required")

        model_name = model_spec.name
        logger.info("get model metadata for model: {}".format(model_name))
        
        # query using process pool
        model_info = self.worker_pool.apply(_get_metadata, args=(model_name,))

        # response
        return GetModelMetadataResponse(
            model_spec = ModelSpec(
                name = model_name,
                version = Int64Value(value = int(model_info['version'])),
                signature_name = 'predict'
            )
        )        

    def Predict(self, request: PredictRequest, context):
        '''
        inference
        '''
        # get model name and signature (predict)
        model_spec = request.model_spec
        if model_spec is None:
            raise Exception("model_spec is required")
        model_name = model_spec.name

        tags = ['model_name:{}'.format(model_name)]
        start = time.time()
        try:
            # perform inference using process pool            
            return self.worker_pool.apply(_predict, args=(model_name, request,))
        except Exception as err:
            logger.error(err)
            self.monitoring.increment('predict.failure', tags)
            raise err
        finally:
            exec_time_ms = (time.time() - start) * 1000
            self.monitoring.increment('predict.success', tags)
            self.monitoring.histogram('predict.exec_time_ms', exec_time_ms, tags)
