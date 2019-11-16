import sys
import os
import multiprocessing
import argparse
import logging as logger

# fix module path
app_root = os.getcwd()
sys.path.append('{}/serving_core'.format(app_root))
sys.path.append('{}/serving_xgboost'.format(app_root))

# import generated artifacts
import tensorflow_serving.apis.prediction_service_pb2_grpc as ps
from tensorflow_serving.apis.predict_pb2 import PredictResponse
from utils.tensor_util import *
from utils.grpc_util import start_grpc_server

# model manager
from managers.model_config_manager import ModelConfigManager
from managers.model_manager import ModelManager


class XgBoostLightPredictionServicer(ps.PredictionServiceServicer):

    def __init__(self, config_path) -> None:
        logger.info('loading serving config')
        serving_config = ModelConfigManager.load(config_path)
        logger.info('serving config:')
        logger.info(serving_config)
        self.model_manager = ModelManager(serving_config)
        super().__init__()

    def Predict(self, request, context):

        model_spec = request.model_spec
        model_name = model_spec.name
        model = self.model_manager.get_model(model_name)
        if model is None:
            raise ModuleNotFoundError('model {} not found'.format(model_name))

        # get features
        features = make_np_array(request.inputs.get('features'))
        if features is None:
            raise Exception("features is required")

        # inference
        result_vector = model.predict(features)

        # response
        result_tensor = make_tensor_proto(result_vector)
        response = PredictResponse(outputs={"result": result_tensor})
        return response


if __name__ == '__main__':
    logger.basicConfig(level=logger.DEBUG)

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--n_workers', default=multiprocessing.cpu_count(), type=int, help='n_workers')
    arg_parser.add_argument('--grpc_port', default=50051, type=int, help='grpc port')
    arg_parser.add_argument('--config_path', default=None, type=str, help='serving config path')
    args = arg_parser.parse_args()

    if args.config_path is None:
        logger.info('config_path is required')
        exit(-1)

    logger.info('params:')
    logger.info(' n_workers: {}'.format(args.n_workers))
    logger.info(' grpc_port: {}'.format(args.grpc_port))
    logger.info(' config_path: {}'.format(args.config_path))

    start_grpc_server(XgBoostLightPredictionServicer(args.config_path), max_workers=args.n_workers, port=args.grpc_port)
