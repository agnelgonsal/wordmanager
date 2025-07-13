from flask import Flask, render_template, request, redirect, send_from_directory, flash
import os
from werkzeug.utils import secure_filename
from docx import Document

app = Flask(__name__)
app.secret_key = "your-secret-key"
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def index():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("index.html", files=files)

@app.route("/create", methods=["POST"])
def create():
    filename = request.form["filename"]
    if not filename.endswith(".docx"):
        filename += ".docx"
    path = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(filename))
    Document().save(path)
    flash("Document created.")
    return redirect("/")

@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files["file"]
        if file and file.filename.endswith(".docx"):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            flash("File uploaded.")
            return redirect("/")
    return render_template("upload.html")

@app.route("/delete/<filename>")
def delete(filename):
    os.remove(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    flash("File deleted.")
    return redirect("/")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
