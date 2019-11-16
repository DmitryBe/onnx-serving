import unittest
import numpy as np
import os
import sys

# fix module path
app_root = os.getcwd()
sys.path.append('{}/serving_core'.format(app_root))
sys.path.append('{}/serving_xgboost'.format(app_root))

from managers.model_config_manager import ModelConfigManager
from managers.model_manager import ModelManager
from tensorflow_serving.apis.predict_pb2 import PredictResponse, PredictRequest
from tensorflow_serving.apis.model_pb2 import ModelSpec
from utils.tensor_util import *
from utils.grpc_util import *


class UseCases(unittest.TestCase):
    # assuming that we are in tests folder
    serving_path = './serving_xgboost/tests/serving_conf'

    def test_service_config_loading(self):
        serving_config = ModelConfigManager.load(UseCases.serving_path)
        assert list(serving_config.model_config_list.config).__len__() == 1

    def test_model_manager(self):
        serving_config = ModelConfigManager.load(UseCases.serving_path)
        model_manager = ModelManager(serving_config)
        assert model_manager.loaded_models.__len__() == 1

    def test_model_predict(self):
        serving_config = ModelConfigManager.load(UseCases.serving_path)
        model_manager = ModelManager(serving_config)
        model = model_manager.get_model('test_model')

        # inference
        features = np.random.rand(2, 20)
        prediction = model.predict(features)
        assert prediction.shape.__len__() == 1

    def test_model_over_grpc(self):

        # feature vectors (random)
        features = np.random.rand(2, 20)
        model_name = 'test_model'

        # request
        request = PredictRequest(
            model_spec=ModelSpec(name=model_name, signature_name='predict'),
            inputs={
                'features': make_tensor_proto(features)
            }
        )

        # call stub (run server first)
        stub = create_prediction_service_stub('localhost', 50051)
        try:
            response = stub.Predict(request)
            result_tensor = response.outputs.get('result')
            result_vector = make_np_array(result_tensor)
            print(result_vector)
        except Exception as ex:
            print(ex)

        assert result_vector.shape.__len__() == 1 # dims
        assert result_vector.__len__() == 2 # number of records


if __name__ == '__main__':
    unittest.main()
