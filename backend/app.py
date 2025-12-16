from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import pdfplumber
from chat_model import chat_with_model
from job_suggester import suggest_jobs_from_resume
import docx
from model import analyze_resume_and_jd

app = Flask(__name__)
CORS(app)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5MB


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    resume = data.get("resume")
    jd = data.get("job_description")

    if not resume or not jd:
        return jsonify({"error": "Resume and Job Description required"}), 400

    return jsonify(analyze_resume_and_jd(resume, jd))


@app.route("/upload_resume", methods=["POST"])
def upload_resume():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    ext = secure_filename(file.filename).split(".")[-1].lower()
    text = ""

    if ext == "pdf":
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                if page.extract_text():
                    text += page.extract_text() + "\n"

    elif ext == "docx":
        doc = docx.Document(file)
        text = "\n".join(p.text for p in doc.paragraphs)

    elif ext == "txt":
        text = file.read().decode("utf-8", errors="ignore")

    else:
        return jsonify({"error": "Unsupported format"}), 400

    return jsonify({"text": text})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message")

    if not message:
        return jsonify({"reply": "Please enter a message."}), 400

    try:
        reply = chat_with_model(message)
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "AI error. Please try again."}), 500


@app.route("/suggest_jobs", methods=["POST"])
def suggest_jobs():
    data = request.json
    resume = data.get("resume")

    if not resume:
        return jsonify({"error": "Resume text required"}), 400

    try:
        result = suggest_jobs_from_resume(resume)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": "Job suggestion failed"}), 500


if __name__ == "__main__":
    app.run(debug=True)
