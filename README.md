# onnx-serving 

onnx-serving uses ONNX runtime for serving non-TensorFlow models and provides TFS compatible gRPC endpoint.

About Onnx: https://onnx.ai/

By using onnxtools (https://github.com/onnx/onnxmltools) someone can convert different models (LightGbm, XGBoost, other supported) into Onnx format and uses onnx-serving for deploying a model in production with TFS compatible gRPC endpoint

## Quick start 

Requirements:
* MODEL_SERVER_CONFIG_PATH
* Dadadog agent `datadog/agent:latest` (for collecting metrics)

Create python virtualenv and install required dependencies

```bash
# create py virtual environment using python 3.7
virtualenv -p `which python3` .py37
# activate venv
. .py37/bin/activate
# install required dependencies
pip install -r requirements.txt
```

Start gRPC server

```bash
MODEL_SERVER_CONFIG_PATH=s3://bucket-name/serving_conf \
./scripts/start-server.sh 
```

[out]:
```yaml
{
 label: [0]
 probabilities: [[0.87079114 0.12920886]]
}
```

Get model metadata (version)

```bash
./scripts/client.sh get-meta --model=model-name
```

[out]:
```yaml
model_spec {
  name: "model-name"
  version {
    value: 1567736600973
  }
  signature_name: "predict"
}
```

Make gRPC predict call

```bash
python -m cli.client predict --model=model-name --tensor="[[0.24297877, 0.61013395, 0.99115646, 0.5074596 , 0.19657457, 0.21933426, 0.19351557, 0.3501961 , 0.85869753, 0.36713797, 0.48622116, 0.9020422 , 0.9859382 , 0.9725097 , 0.5156128 , 0.7225592 , 0.19482191, 0.19482191, 0.19482191, 0.19482191]]"

```

## Model server configuration

onnx-serving has a TFS compartible serving configuration (https://www.tensorflow.org/tfx/serving/serving_config)

Example

```bash
model_config_list: {
  config: {
    name: 'gs-match-pred'
    base_path: 's3://bucket-name/model-name/models/'
    model_platform: 'onnx'
  }
}
```

Where:
* name is a model name and should be unique within a deployment scope
* base_path is a model location (model base folder with version folders (int)); currently supported s3 source.
* model_platform is a type of custom servable (currently support only onnx); custom servables can be created and registered (see `ModelBase` and `ModelLoaderBase` abstraction)

## Monitoring 

gRPC server collects following metrics:
* DD_STATSD_PREF.predict.[success|failure|exec_time_ms]

## Configuration

Following envs are supported:
* PROCESS_COUNT - number of processes with gRPC server (default eq to `multiprocessing.cpu_count`)
* THREAD_CONCURRENCY - number of threads in `ThreadPoolExecutor` per gRPC preocess
* MODEL_SERVER_CONFIG_PATH - model serving config path (s3://)
* DD_STATSD_HOST (or STATSD_HOST) - statsd host ip
* DD_STATSD_PREF - metrics prefix (default: `onnx_serving`)
* DD_STATSD_CONSTANT_TAGS - metrics constant tags (default: `env:dev`)

## Dockerization

Build docker image

```bash
make docker-build
```

Run docker container

```bash
docker run -it --rm \
    -p 8500:8500 \
    -e MODEL_SERVER_CONFIG_PATH=$MODEL_SERVER_CONFIG_PATH \
    -v $HOME/.aws:/root/.aws \
    dmitryb/onnx-serving:latest
```

## Deploy on k8s

Deploy/upgrade
```bash
helm upgrade --install ${DEPLOYMENT_NAME} ${PACKAGE_URL} \
    --namespace ${K8S_NS}  \
    --set image.repository=dmitryb/onnx-serving \
    --set image.tag=latest \
    --set image.pullPolicy=Always \
    --set service.port=8500 \
    --set kube2iam.enabled=true \
    --set kube2iam.role=datalake-dev-stg \
    --set resources.limits.cpu=3800m \
    --set resources.limits.memory=7Gi \
    --set resources.requests.cpu=3800m \
    --set resources.requests.memory=7Gi \
    --set nodeSelector.kubelet\\.kubernetes\\.io/group=apps \
    --set envs.AWS_DEFAULT_REGION=ap-southeast-1 \
    --set envs.MODEL_SERVER_CONFIG_PATH=s3://bucket-name/serving_conf \
    --set hpa.enabled=true \
    --set hpa.min_replicas=2 \
    --set hpa.max_replicas=5
    
    # add for debugging 
    #--debug --dry-run
```

Remove

```bash
helm delete --purge ${DEPLOYMENT_NAME}
```

Publish via Ambassador (update svc)

```bash
metadata:
  annotations:    
    getambassador.io/config: |
      ---
      apiVersion: ambassador/v0
      kind: Mapping
      name: pred-onnx
      grpc: true
      prefix: /tensorflow.serving.PredictionService/
      rewrite: /tensorflow.serving.PredictionService/
      service: svc-name.ns.svc.cluster.local:8500
      ---
```

