import grpc
import time
import logging as logger
from concurrent import futures
from tensorflow_serving.apis.prediction_service_pb2_grpc import add_PredictionServiceServicer_to_server, PredictionServiceStub

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def start_grpc_server(servicer, max_workers, port):
    """
    Starts grpc server
    :param servicer: instance of PredictionServiceServicer
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers))
    add_PredictionServiceServicer_to_server(servicer, server)
    server.add_insecure_port('[::]:{}'.format(port))
    server.start()
    logger.info('listening port: {}'.format(port))
    logger.info('running')
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        logger.info('stopping')
        server.stop(0)


def create_prediction_service_stub(ip:str, port: int) -> PredictionServiceStub:
    """
    :return: PredictionServiceStub
    """
    channel = grpc.insecure_channel('{}:{}'.format(ip, port))
    return PredictionServiceStub(channel)
