from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import os
import logging
import datetime
import multiprocessing

# fix module path
app_root = os.getcwd()
sys.path.append('{}/generated'.format(app_root))

# --- params ---

ONE_DAY = datetime.timedelta(days=1)
PROCESS_COUNT = int(os.environ.get('PROCESS_COUNT', multiprocessing.cpu_count() * 2))
THREAD_CONCURRENCY = int(os.environ.get('THREAD_CONCURRENCY', 64))
# grpc server binding
GRPC_PORT = int(os.environ.get('GRPC_PORT', 8500))
GRPC_IP = os.environ.get('GRPC_IP', 'localhost')
# model server config path s3://...
MODEL_SERVER_CONFIG_PATH = os.environ.get('MODEL_SERVER_CONFIG_PATH')
# datadog statsd config
STATSD_HOST = os.environ.get('STATSD_HOST', '127.0.0.1')
DD_STATSD_HOST = os.environ.get('DD_STATSD_HOST', STATSD_HOST)
DD_STATSD_PORT = int(os.environ.get('DD_STATSD_PORT', 8125))
DD_STATSD_PREF = os.environ.get('DD_STATSD_PREF', 'onnx_serving')
DD_STATSD_CONSTANT_TAGS = os.environ.get('DD_STATSD_CONSTANT_TAGS', 'env:dev').split(',')
