import os
import sys
import unittest
import numpy as np
from internal.utils.tensor_utils import *


class TestTensorUtils(unittest.TestCase):

    def test_tensor_to_ndarray_conversion(self):
        """
        convert ndarray to tensor and back
        """

        # original array
        data = np.array([
            [1, 2, 3],
            [1, 2, 3],
            [1, 2, 3]
        ])

        # convert to tensor
        tensor = make_tensor_proto(data)

        # convert back
        data_r = make_np_array(tensor)

        # shape eq
        assert data.shape == data_r.shape

        # data and data_r are identical
        f = False in data.__eq__(data_r).flatten()
        assert f is False


if __name__ == '__main__':
    unittest.main()
