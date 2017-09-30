'''
################################## client.py #############################
# 
################################## client.py #############################
'''
import grpc
import datastore_pb2

class DatastoreClient():
    '''
    '''

    def __init__(self, host='0.0.0.0', port=3000):
        '''
        '''
        # TODO
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = datastore_pb2.DatastoreStub(self.channel)

    def put(self, key, data):
        '''
        '''
        print("put {} at {}".format(data, key))
        req = datastore_pb2.Request(key=key, data=data)
        return self.stub.put(req)

    def get(self, key):
        '''
        '''
        print("get value at {}".format(key))
        req = datastore_pb2.Request(key=key)
        return self.stub.get(req)


print("Client is running...")
client = DatastoreClient('grpc_server')
resp = client.put('foo', 'bar')
print(resp)
resp = client.get('foo')
print(resp)

