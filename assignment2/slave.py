import grpc
import replicator_pb2
import rocksdb

PORT = 3000

class ReplicatorSlave():
    def __init__(self, host='0.0.0.0', port=PORT):
        self.db = rocksdb.DB("assignment2-slave.db", rocksdb.Options(create_if_missing=True))
        self.channel = grpc.insecure_channel('%s:%d' % (host, port))
        self.stub = replicator_pb2.ReplicatorStub(self.channel)

    def sync(self):
        synchronizer = self.stub.sync(replicator_pb2.SyncRequest())
        print("Connected to master")
        for op in synchronizer:
            if op.op == 'put':
                print("Put {}:{} to slave db".format(op.key, op.data))
                self.db.put(op.key.encode(), op.data.encode())
            elif op.op == 'delete':
                print("Delete {} from slave db".format(op.key))
                self.db.delete(op.key.encode())
            else:
                # invalid operation
                pass

def main():
    slave = ReplicatorSlave()
    resp = slave.sync()

if __name__ == "__main__":
    main()

