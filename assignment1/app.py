import rocksdb
import uuid
import subprocess
from flask import Flask, request, jsonify
app = Flask(__name__)


@app.route("/api/v1/scripts", methods=['POST'])
def create_script():
    db = rocksdb.DB("test.db", rocksdb.Options(create_if_missing=True))
    script = request.files['data']
    uid = str(uuid.uuid4())
    db.put(uid.encode(), script.read())
    return jsonify({"script-id": uid})

@app.route("/api/v1/scripts/<script_id>", methods=['GET'])
def execute_script(script_id):
    try:
        db = rocksdb.DB("test.db", rocksdb.Options(create_if_missing=True))
        script = db.get(script_id.encode())
        if script:
            response = subprocess.check_output(["python3.6", "-c", script])
            return response
        else:
            return "Script not found", 404
    except subprocess.CalledProcessError as e: 
        return "Unexpected error occurred", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
