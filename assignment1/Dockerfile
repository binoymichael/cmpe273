FROM ubuntu-python3.6-rocksdb-grpc:1.0

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python3.6"]
CMD ["app.py"]


