'''
################################## server.py #############################
# 
################################## server.py #############################
'''
import time
import grpc
import datastore_pb2
import datastore_pb2_grpc
import rocksdb

from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class MyDatastoreServicer(datastore_pb2.DatastoreServicer):
    '''
    '''

    def __init__(self):
        '''
        '''
        print("init server")
        self.db = rocksdb.DB("test.db", rocksdb.Options(create_if_missing=True))

    def put(self, request, context):
        '''
        '''
        print("put {} at {}".format(request.data, request.key))
        self.db.put(request.key.encode(), request.data.encode())
        return datastore_pb2.Response(data='success')

    def get(self, request, context):
        '''
        '''
        print("get value at {}".format(request.key))
        data = self.db.get(request.key.encode())
        return datastore_pb2.Response(data=data)


def run(host, port):
    '''
    Run the GRPC server
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    datastore_pb2_grpc.add_DatastoreServicer_to_server(MyDatastoreServicer(), server)
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
