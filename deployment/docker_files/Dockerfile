FROM python:3.7

RUN pip install grpcio==1.24.1 --no-binary grpcio \
    && pip install grpcio-tools==1.24.1 \
    && pip install numpy==1.17.0 \
    && pip install protobuf==3.10.0 \
    && pip install pytz==2019.2 \
    && pip install datadog==0.29.0 \
    && pip install boto3==1.9.215 \
    && pip install onnxruntime==0.5.0

ENV APP_DIR /app
ENV PYTHONPATH=./generated

# app root
RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}

# app artifacts
ADD ./generated ${APP_DIR}/generated
ADD ./internal ${APP_DIR}/internal
ADD ./scripts ${APP_DIR}/scripts
ADD ./tests ${APP_DIR}/tests
ADD ./README.md ${APP_DIR}

# app default env
ENV GRPC_IP '[::]'
ENV GRPC_PORT '8500'

ENTRYPOINT [ "bash", "-c", "./scripts/start-server.sh" ]
