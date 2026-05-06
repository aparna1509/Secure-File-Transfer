Secure File Transfer Web App
A full-stack web application for secure file sharing using AES encryption. Upload any file, protect it with a password, and share an encrypted download link — all with real-time password breach detection.

Features:
1. AES Encryption (Fernet) — Files are encrypted before storage; only the correct password decrypts them
2. Shareable Encrypted Links — Generate a unique link for each uploaded file
3. Password Breach Detection — Real-time check via Pwned Passwords API using SHA-1 k-anonymity (your password is never sent in plain text)
4. Password Strength Analyzer — Instant frontend feedback on password quality
5. Responsive UI — Clean, mobile-friendly interface built with Bootstrap

Tech Stack:
Backend: Python, Flask
Frontend: HTML, CSS, JavaScript, Bootstrap
Encryption: Cryptography library (Fernet / AES)
Hashing: Hashlib (SHA-1)
API: Pwned Passwords REST API
Version Control: Git, GitHub

How It Works:
User uploads file + sets password
        ↓
Password checked against Pwned Passwords API (SHA-1, k-anonymity)
        ↓
File encrypted using AES (Fernet) with password-derived key
        ↓
Unique shareable download link generated
        ↓
Recipient enters password → file decrypted and downloaded

Security Highlights:
1. Passwords are never stored — only used to derive the encryption key
2. Breach detection uses k-anonymity — only the first 5 chars of the SHA-1 hash are sent to the API
3. Files are stored encrypted at rest — unreadable without the correct password

Getting Started(Prerequisites)
- Python 3.8+
- pip

Installation
# 1. Clone the repository
git clone https://github.com/yourusername/secure-file-transfer.git
cd secure-file-transfer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
