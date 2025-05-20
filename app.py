from flask import Flask,request,jsonify
from transcriber import transcribe_audio
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER,exist_ok=True)

app = Flask(__name__)
CORS(app,origins=["http://localhost:3000"])
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/transcribe", methods = ["POST"])
def upload_file():
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
    app.run(debug=True)
    