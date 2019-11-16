
REPO=dmitryb/onnx-serving
TAG=latest

generate:
	mkdir -p ./generated
	python -m grpc_tools.protoc \
        -I./protos \
        --python_out=./generated/ \
        --grpc_python_out=./generated/ \
        protos/tensorflow/core/protobuf/*.proto \
		protos/tensorflow/core/framework/*.proto \
		protos/tensorflow/core/example/*.proto \
		protos/tensorflow_serving/apis/*.proto \
		protos/tensorflow_serving/config/*.proto

docker-build:
	docker build -t $(REPO):$(TAG) -f ./deployment/docker_files/Dockerfile .

docker-push:
	docker push $(REPO):$(TAG)