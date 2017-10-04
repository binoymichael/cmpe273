Assuming the ubuntu-python3.6-rocksdb-grpc image is available locally

### Build the image from the Dockerfile
docker build -t flask-app:latest .

### Run the flask app container
docker run --rm -it -p8000:5000 flask-app

### Upload a script
curl -i -X POST -H "Content-Type: multipart/form-data" -F "data=@foo.py" http://localhost:8000/api/v1/scripts

### Run the uploaded script
curl -i http://localhost:8000/api/v1/scripts/<script-id>

