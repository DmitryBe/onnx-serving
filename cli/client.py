import sys
import os
import click
import grpc
from internal.config import *
from internal.utils.tensor_utils import *

from tensorflow_serving.apis.predict_pb2 import PredictResponse, PredictRequest
from tensorflow_serving.apis.model_pb2 import ModelSpec
from tensorflow_serving.apis.prediction_service_pb2_grpc import add_PredictionServiceServicer_to_server, PredictionServiceStub
from tensorflow_serving.apis.get_model_metadata_pb2 import GetModelMetadataRequest, GetModelMetadataResponse
from tensorflow_serving.apis.model_pb2 import ModelSpec
from google.protobuf.wrappers_pb2 import Int64Value


@click.group()
def cli():
    pass

@cli.command()
@click.option('--url', default='localhost:8500', help='grpc server url (example: localhost:8500)')
@click.option('--model', required=True, help='model name')
def get_meta(url, model):
    '''
    '''
    host, port = url.split(':')
    stub = _create_prediction_service_stub(host, port)

    request = GetModelMetadataRequest(
        model_spec = ModelSpec(
            name = model
        )
    )
    response = stub.GetModelMetadata(request)
    click.echo('results')
    click.echo('{}'.format(response))


@cli.command()
@click.option('--url', default='localhost:8500', help='grpc server url (example: localhost:8500)')
@click.option('--model', required=True, help='model name')
@click.option('--tensor', required=True, help='example: [[1, 2, 3],[1, 2, 3],[1, 2, 3]]')
def predict(url, model, tensor):
    '''    
    '''
    host, port = url.split(':')
    stub = _create_prediction_service_stub(host, port)

    # str -> np array
    np_array = np.array(eval(tensor))
    # -> tf tensor
    request_tensor = make_tensor_proto(np_array)

    # make a call
    request = PredictRequest(
        model_spec=ModelSpec(name=model),
        inputs={
            'input': request_tensor
        }
    )
    response = stub.Predict(request)

    # print results
    click.echo('results')
    for key, val_tf_tensor in response.outputs.items():        
        nd_array = make_np_array(val_tf_tensor)        
        click.echo(' {}: {}'.format(key, nd_array))

def _create_prediction_service_stub(ip:str, port: int) -> PredictionServiceStub:
    """
    :return: PredictionServiceStub
    """
    channel = grpc.insecure_channel('{}:{}'.format(ip, port))
    return PredictionServiceStub(channel)

if __name__ == '__main__':    
    cli()
