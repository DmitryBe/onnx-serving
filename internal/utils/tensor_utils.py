import numpy as np
from tensorflow.core.framework.tensor_pb2 import TensorProto
from tensorflow.core.framework.tensor_shape_pb2 import TensorShapeProto
import tensorflow.core.framework.types_pb2 as tf_types


def make_tensor_proto(np_array: np.ndarray) -> TensorProto:
    """
    Converts numpy array to tf tensor
    """
    dim = [TensorShapeProto.Dim(size=i) for i in np_array.shape]

    if np_array.dtype == np.float32:
        out_tensor = TensorProto(
            dtype=tf_types.DT_FLOAT,
            tensor_shape=TensorShapeProto(dim=dim),
            float_val=np_array.flatten()
        )
    elif np_array.dtype == np.int:
        out_tensor = TensorProto(
            dtype=tf_types.DT_INT32,
            tensor_shape=TensorShapeProto(dim=dim),
            int_val=np_array.flatten()
        )
    elif np_array.dtype == np.float64:
        out_tensor = TensorProto(
            dtype=tf_types.DT_DOUBLE,
            tensor_shape=TensorShapeProto(dim=dim),
            double_val=np_array.flatten()
        )
    elif np_array.dtype == np.bool:
        out_tensor = TensorProto(
            dtype=tf_types.DT_BOOL,
            tensor_shape=TensorShapeProto(dim=dim),
            bool_val=np_array.flatten()
        )
    elif np_array.dtype.type == np.unicode_:
        out_tensor = TensorProto(
            dtype=tf_types.DT_STRING,
            tensor_shape=TensorShapeProto(dim=dim)            
        )        
        out_tensor.string_val.extend([v.encode('utf-8') for v in np_array.flatten()])
    else:
        raise NotImplemented("type is not supported")

    return out_tensor


def make_np_array(tensor: TensorProto) -> np.ndarray:
    """
    Converts tf tensor to numpy array
    """
    shape = [d.size for d in tensor.tensor_shape.dim]

    if tensor.dtype == tf_types.DT_FLOAT:
        flat_data = tensor.float_val
    elif tensor.dtype == tf_types.DT_INT32:
        flat_data = tensor.int_val
    elif tensor.dtype == tf_types.DT_DOUBLE:
        flat_data = tensor.double_val
    elif tensor.dtype == tf_types.DT_BOOL:
        flat_data = tensor.bool_val
    else:
        raise NotImplemented("type is not supported")

    return np.array(flat_data).reshape(shape)
