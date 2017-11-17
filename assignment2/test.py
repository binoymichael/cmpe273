import grpc
import replicator_pb2

PORT = 3000

class ReplicatorTest():
    def __init__(self, host='0.0.0.0', port=PORT):
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = replicator_pb2.ReplicatorStub(self.channel)

    def put(self, key, data):
        return self.stub.put(replicator_pb2.Request(key=key, data=data))

    def delete(self, key):
        return self.stub.delete(replicator_pb2.Request(key=key))

def main():
    test = ReplicatorTest()
    print('Test 1: put foo:bar')
    resp = test.put('foo', 'bar')
    print(resp.data)
    print('Test 2: delete foo')
    resp = test.delete('foo')
    print(resp.data)
    print('Test 3: put moo:bar')
    resp = test.put('moo', 'bar')
    print(resp.data)

if __name__ == "__main__":
    main()


