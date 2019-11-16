import onnxruntime
from tensorflow_serving.apis.predict_pb2 import PredictResponse, PredictRequest
from internal.log import create_logger
from internal.models.base import ModelBase
from internal.utils.tensor_utils import *

logger = create_logger(__name__)

class OnnxModel(ModelBase):
    """
    onnx serving implementation
    """
    def __init__(self, data: bytes):
        self.sess = onnxruntime.InferenceSession(data)
        self.input_vars = list(map(lambda x: x.name, self.sess.get_inputs()))
        self.output_vars = list(map(lambda x: x.name, self.sess.get_outputs()))
        logger.info('onnx model initialised; inputs: {}, outputs: {}'.format(self.input_vars, self.output_vars))        
        
    def predict(self, request: PredictResponse) -> PredictResponse:
        
        # convert request to onnx input
        onnx_request = {}
        for input_var in self.input_vars:
            input_var_tf_tensor = request.inputs.get(input_var)
            if input_var_tf_tensor is None:
                raise Exception('required parameter {} is missing'.format(input_var))
            onnx_request[input_var] = make_np_array(input_var_tf_tensor).astype(np.float32)
    
        # make onnx inference
        outs = self.sess.run(self.output_vars, onnx_request)

        # convert to predict response
        outputs = {}
        for idx, output_var in enumerate(self.output_vars):
            output_var_val = outs[idx]
            if isinstance(output_var_val, np.ndarray):
                # convert ndarray to tf-sensor
                outputs[output_var] = make_tensor_proto(output_var_val)
            elif isinstance(output_var_val, list) and output_var_val.__len__() > 0 and isinstance(output_var_val[0], dict):
                # list of dict
                # convert list of dict to ndarray of values (we assume that every dict has same key/val)
                np_array_nd = np.array(list(map(lambda x: list(x.values()), output_var_val)))
                # convert to tf-tensor
                outputs[output_var] = make_tensor_proto(np_array_nd)
            else:
                raise Exception('cannot convert {} to tf tensor; unsupported type {}'.format(output_var, type(output_var_val)))

        # upstream
        return PredictResponse(outputs=outputs)