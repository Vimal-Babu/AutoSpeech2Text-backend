from flask import Flask,request,jsonify
from transcriber import transcribe_audio
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER,exist_ok=True)

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.after_request
def apply_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response

@app.route("/")
def home():
    return "Backend is live!"

@app.route("/transcribe", methods = ["POST","OPTIONS"])
def upload_file():
    if request.method == "OPTIONS":
        return '',204
    
    if "file" not in request.files:
        return jsonify({"error":"No file uploaded"}), 400
    
    file = request.files["file"]
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"],filename)
    file.save(file_path)
    
    try:
        transcription = transcribe_audio(file_path)
        return jsonify({"transcription": transcription })
    except Exception as e :
        return jsonify({"error":str(e)}), 500
    






if __name__ == "__main__":
    app.run(debug=False)
    