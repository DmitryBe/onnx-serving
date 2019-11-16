import numpy as np

from models.model_base import ModelBase
import lightgbm as lgb


class LightGBMModel(ModelBase):

    def __init__(self, model_path: str):
        self.model = lgb.Booster(model_file=model_path)

    def predict(self, features: np.ndarray) -> np.ndarray:
        # if features.shape
        if features.shape.__len__() != 2:
            raise Exception('required features dims: 2d')
        return self.model.predict(features)


