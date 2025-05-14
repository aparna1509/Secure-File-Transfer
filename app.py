from flask import Flask, render_template, request, send_file, redirect, url_for
from cryptography.fernet import Fernet
import os
import hashlib
import base64
import re
import uuid

app = Flask(__name__)

# Folder structure
UPLOAD_FOLDER = "uploads"
ENCRYPTED_FOLDER = "uploads/encrypted_files"
DECRYPTED_FOLDER = "uploads/decrypted_files"

# Create folders if not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)
os.makedirs(DECRYPTED_FOLDER, exist_ok=True)

# Generate key from password
def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

# Password strength checker
def check_password_strength(password):
    length_error = len(password) < 8
    digit_error = re.search(r"\d", password) is None
    uppercase_error = re.search(r"[A-Z]", password) is None
    lowercase_error = re.search(r"[a-z]", password) is None
    symbol_error = re.search(r"[!@#$%^&*(),.?\":{}|<>]", password) is None

    errors = {
        "Length Error": length_error,
        "Digit Error": digit_error,
        "Uppercase Error": uppercase_error,
        "Lowercase Error": lowercase_error,
        "Symbol Error": symbol_error,
    }

    strength = 5 - sum(errors.values())
    if strength == 5:
        return "Strong 💪"
    elif 3 <= strength < 5:
        return "Moderate ⚡"
    else:
        return "Weak 😢"

# Encrypt the file
def encrypt_file(file_path, password):
    key = generate_key(password)
    fernet = Fernet(key)

    with open(file_path, "rb") as file:
        file_data = file.read()

    encrypted_data = fernet.encrypt(file_data)
    encrypted_file_name = f"{uuid.uuid4().hex}.enc"
    encrypted_file_path = os.path.join(ENCRYPTED_FOLDER, encrypted_file_name)

    with open(encrypted_file_path, "wb") as file:
        file.write(encrypted_data)

    return encrypted_file_path, encrypted_file_name

# Decrypt the file
def decrypt_file(file_path, password):
    key = generate_key(password)
    fernet = Fernet(key)

    with open(file_path, "rb") as file:
        encrypted_data = file.read()

    try:
        decrypted_data = fernet.decrypt(encrypted_data)
    except Exception:
        return None

    decrypted_file_path = os.path.join(DECRYPTED_FOLDER, os.path.basename(file_path).replace(".enc", ""))
    with open(decrypted_file_path, "wb") as file:
        file.write(decrypted_data)

    return decrypted_file_path

# Home route
@app.route("/")
def index():
    return render_template("index.html")

# Sender route
@app.route("/send", methods=["GET", "POST"])
def sender():
    if request.method == "POST":
        file = request.files["file"]
        password = request.form["password"]

        if file and password:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            # Check password strength
            strength = check_password_strength(password)

            # Encrypt the file
            encrypted_file_path, encrypted_file_name = encrypt_file(file_path, password)

            # Generate a shareable link
            download_link = f"http://127.0.0.1:5000/download/{encrypted_file_name}"

            return render_template(
                "link_generated.html",
                link=download_link,
                strength=strength,
            )

    return render_template("sender.html")

# Receiver route
@app.route("/receive", methods=["GET", "POST"])
def receiver():
    if request.method == "POST":
        file = request.files["file"]
        password = request.form["password"]

        if file and password:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            # Decrypt the file
            decrypted_file_path = decrypt_file(file_path, password)

            if decrypted_file_path:
                return send_file(
                    decrypted_file_path,
                    as_attachment=True,
                    download_name=os.path.basename(decrypted_file_path),
                )
            else:
                return """
                <h2>❌ Decryption Failed!</h2>
                <p>Invalid password or corrupted file.</p>
                <a href="/">⬅️ Back to Home</a>
                """

    return render_template("receiver.html")

# Download encrypted file
@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join(ENCRYPTED_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found!", 404


if __name__ == "__main__":
    app.run(debug=True)
