from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import internal.config as svc_config
from internal.log import create_logger
from internal.di_root import DIRoot
from internal.grpc.predict_servicer import PredictionServiceServicer
from internal.grpc.server import start_multiprocess_grpc_server, start_grpc_server
from internal.di_config import configure_di

from tensorflow_serving.apis.prediction_service_pb2_grpc import add_PredictionServiceServicer_to_server

logger = create_logger(__name__)

if __name__ == '__main__':

    configure_di()
    # start single process grpc server
    start_grpc_server(
        lambda server: add_PredictionServiceServicer_to_server(PredictionServiceServicer(n_processes=svc_config.PROCESS_COUNT), server),
        svc_config.GRPC_IP,
        svc_config.GRPC_PORT,         
        svc_config.THREAD_CONCURRENCY,
        None
    )
    # start multiprocess grpc server
    # start_multiprocess_grpc_server(
    #     lambda server: add_PredictionServiceServicer_to_server(PredictionServiceServicer(n_processes=PROCESS_COUNT), server),
    #     svc_config.GRPC_IP,
    #     svc_config.GRPC_PORT, 
    #     svc_config.PROCESS_COUNT, 
    #     svc_config.THREAD_CONCURRENCY
    # )