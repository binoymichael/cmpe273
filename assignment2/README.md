### Replicator

- Assuming rocksdb, grpcio-tools is installed in the system run the following
  commands
```
# Generate the stubs using the proto file
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./replicator.proto
# Run the master service
python3 master.py 
# Run the slave. Slave connects to master
python3 slaver.py
# Run the test script. It sends data to master db. Master db replicates data to slave db
python3 test.py
```

