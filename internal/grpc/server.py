from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import contextlib
import datetime
import logging
import math
import multiprocessing
import socket
import grpc
import sys
import time
import os
from concurrent import futures

from internal.log import create_logger

logger = create_logger(__name__)
ONE_DAY = datetime.timedelta(days=1)

def start_multiprocess_grpc_server(register_servicer_func, 
                                   grpc_ip: int = 'localhost',
                                   grpc_port: int = 9000,
                                   n_processes: int = 4,
                                   n_threads_per_process: int = 64):
    """
    starts multi-process grpc server (multiple processes with grpc server inside)
    """
    with _reserve_port(grpc_port) as port:        
        bind_address = '{}:{}'.format(grpc_ip, port)
        logger.info('bind address: {}'.format(bind_address))
        
        # bind multiple processes to one port
        options = (('grpc.so_reuseport', 1),)

        # start multiple processes with grpc server inside
        sys.stdout.flush()
        workers = []        
        for _ in range(n_processes):
            # NOTE: It is imperative that the worker subprocesses be forked before
            # any gRPC servers start up. See
            # https://github.com/grpc/grpc/issues/16001 for more details.
            worker = multiprocessing.Process(
                target=start_grpc_server, args=(register_servicer_func, grpc_ip, grpc_port, n_threads_per_process, options,)
            )
            worker.start()
            workers.append(worker)

        for worker in workers:
            worker.join()

def start_grpc_server(register_servicer_func,
                      grpc_ip: int = 'localhost',
                      grpc_port: int = 9000,
                      n_threads: int = 64,
                      options: tuple = None):
    """
    starts grpc server (current process)
    """
    bind_address = '{}:{}'.format(grpc_ip, grpc_port)
    logger.info('starting gRPC server on: {}'.format(bind_address))

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=n_threads,),
        options=options
    )    
    register_servicer_func(server)
    server.add_insecure_port(bind_address)
    server.start()
    _wait_forever(server)

def _wait_forever(server):
    """
    waits forever
    """
    try:
        while True:
            time.sleep(ONE_DAY.total_seconds())
    except KeyboardInterrupt:
        server.stop(None)

@contextlib.contextmanager
def _reserve_port(port=9000):
    """
    find and reserve a port for all subprocesses to use.
    """
    sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    if sock.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT) == 0:
        raise RuntimeError("Failed to set SO_REUSEPORT.")
    sock.bind(('', port))
    try:
        yield sock.getsockname()[1]
    finally:
        sock.close()