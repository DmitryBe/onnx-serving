import os
import sys
import grpc
import unittest
import numpy as np
import atexit

from tensorflow_serving.apis.predict_pb2 import PredictResponse, PredictRequest
from tensorflow_serving.apis.model_pb2 import ModelSpec
from tensorflow_serving.apis.prediction_service_pb2_grpc import add_PredictionServiceServicer_to_server, PredictionServiceStub
from tensorflow_serving.apis.get_model_metadata_pb2 import GetModelMetadataRequest, GetModelMetadataResponse
from tensorflow_serving.apis.model_pb2 import ModelSpec
from google.protobuf.wrappers_pb2 import Int64Value

from internal.log import create_logger
from internal.utils.tensor_utils import *

logger = create_logger()

# Each worker process initializes a single channel after forking.
# It's regrettable, but to ensure that each subprocess only has to instantiate
# a single channel to be reused across all RPCs, we use globals.
_worker_channel_singleton = None
_worker_stub_singleton = None

def _initialize_worker(server_address):
    global _worker_channel_singleton  # pylint: disable=global-statement
    global _worker_stub_singleton  # pylint: disable=global-statement
    logger.info('Initializing worker process.')
    _worker_channel_singleton = grpc.insecure_channel(server_address)
    _worker_stub_singleton = PredictionServiceStub(_worker_channel_singleton)
    # atexit.register(_shutdown_worker)

def _shutdown_worker():
    logger.info('Shutting worker process down.')
    if _worker_channel_singleton is not None:
        _worker_channel_singleton.stop()

class TestSandbox(unittest.TestCase):

    def test_predict(self):
        """
        python -m unittest tests.sandbox_test.TestSandbox.test_predict
        """        
        _initialize_worker("localhost:8500")

        for i in range(10):
            np_array = np.random.rand(1,20)        
            request_tensor = make_tensor_proto(np_array)

            # make a call
            request = PredictRequest(
                model_spec=ModelSpec(name='gs-mp-227'),
                inputs={
                    'input': request_tensor
                }
            )
            response = _worker_stub_singleton.Predict(request)
            logger.info("+")
        assert True


if __name__ == '__main__':
    unittest.main()
