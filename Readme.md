docker run -it --rm --name my-grpc-server -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 /bin/bash  -c "python3.6 -m grpc.tools.protoc -I. --python_out=. --grpc_python_out=. datastore.proto; python3.6 server.py"

docker run -it --rm --name my-grpc-client --link my-grpc-server:grpc_server -v "$PWD":/usr/src/myapp -w /usr/src/myapp ubuntu-python3.6-rocksdb-grpc:1.0 /bin/bash  -c "python3.6 -m grpc.tools.protoc -I. --python_out=. --grpc_python_out=. datastore.proto; python3.6 client.py"
