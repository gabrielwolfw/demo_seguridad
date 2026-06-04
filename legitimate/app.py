from flask import Flask, request, session, redirect, url_for, render_template, jsonify
import pyotp
import os

app = Flask(__name__)
app.secret_key = "demo-secret-key"

# Usuario hardcodeado para la demo
USERS = {
    "usuario": {
        "password": "password123",
        "totp_secret": "JBSWY3DPEHPK3PXP"  # secreto fijo para que el QR sea siempre el mismo
    }
}

@app.route("/")
def index():
    if "logged_in" in session:
        return render_template("dashboard.html", username=session["username"])
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        totp_code = request.form.get("totp_code")

        user = USERS.get(username)
        if user and user["password"] == password:
            totp = pyotp.TOTP(user["totp_secret"])
            if totp.verify(totp_code):
                session["logged_in"] = True
                session["username"] = username
                return redirect(url_for("index"))
            else:
                error = "Código TOTP incorrecto o expirado."
        else:
            error = "Usuario o contraseña incorrectos."

    return render_template("login.html", error=error)

# Endpoint interno que usa el sitio de phishing para hacer relay
@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    totp_code = data.get("totp_code")

    user = USERS.get(username)
    if user and user["password"] == password:
        totp = pyotp.TOTP(user["totp_secret"])
        if totp.verify(totp_code):
            return jsonify({"success": True, "message": "Login exitoso en sitio legítimo"})
        else:
            return jsonify({"success": False, "message": "TOTP incorrecto o expirado"}), 401
    return jsonify({"success": False, "message": "Credenciales incorrectas"}), 401

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/qr")
def qr():
    secret = USERS["usuario"]["totp_secret"]
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name="usuario@banco-demo.com", issuer_name="BancoDemo")
    return render_template("qr.html", uri=uri, secret=secret)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
