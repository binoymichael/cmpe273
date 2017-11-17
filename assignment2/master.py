import time
import grpc
import replicator_pb2
import replicator_pb2_grpc
import queue
import rocksdb

from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class MyReplicatorServicer(replicator_pb2.ReplicatorServicer):
    def __init__(self):
        self.db = rocksdb.DB("assignment2-master.db", rocksdb.Options(create_if_missing=True))
        self.operations_queue = queue.Queue()

    def push_to_slave(func):
        def func_wrapper(self, request, context):
            op = replicator_pb2.SyncOperation(
                    op=func.__name__, 
                    key=request.key.encode(), 
                    data=request.data.encode()
                 ) 
            self.operations_queue.put(op)
            return func(self, request, context)
        return func_wrapper

    @push_to_slave
    def put(self, request, context):
        print("Put {}:{} to master db".format(request.key, request.data))
        self.db.put(request.key.encode(), request.data.encode())
        return replicator_pb2.Response(data='ok')

    @push_to_slave
    def delete(self, request, context):
        print("Delete {} from master db".format(request.key))
        self.db.delete(request.key.encode())
        return replicator_pb2.Response(data='ok')
        
    def get(self, request, context):
        print("Get {} from master db".format(request.key))
        value = self.db.get(request.key.encode())
        return replicator_pb2.Response(data=value)


    def sync(self, request, context):
        print("Slave connected")
        while True:
            operation = self.operations_queue.get()
            print("Sending operation ({}, {}, {}) to slave".format(operation.op, operation.key, operation.data))
            yield operation

def run(host, port):
    '''
    Run the GRPC server
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    replicator_pb2_grpc.add_ReplicatorServicer_to_server(MyReplicatorServicer(), server)
    server.add_insecure_port('%s:%d' % (host, port))
    server.start()

    try:
        while True:
            print("Server started at...%d" % port)
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run('0.0.0.0', 3000)



