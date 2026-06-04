# Demo: Phishing en tiempo real contra TOTP
CE-1115 Seguridad de la Información — Tema 3: MFA

---

## Requisitos

- Docker y Docker Compose instalados
- Puertos 5000 y 5001 libres
- Aegis, Google Authenticator o cualquier app TOTP en el celular

---

## Antes de la demo (hacer una sola vez)

**1. Levantar los contenedores**
```bash
docker compose up --build
```

**2. Registrar el autenticador**

Abrir en el browser: http://localhost:5000/qr

Escanear el QR con la app del celular. Esto registra la cuenta "BancoDemo" en el autenticador.

---

## Durante la demo

Abrir dos terminales y dos ventanas del browser.

**Terminal 1 — mantener corriendo:**
```bash
docker compose up
```

**Terminal 2 — consola del atacante (mostrar en la presentación):**
```bash
docker logs -f sitio-phishing
```

**Browser 1 — sitio legítimo:**
```
http://localhost:5000/login
```

**Browser 2 — sitio falso:**
```
http://localhost:5001
```

---

## Flujo de la presentación

**Paso 1 — mostrar el sitio legítimo**

En browser 1 hacer login con:
- Usuario: `usuario`
- Contraseña: `password123`
- TOTP: código actual del celular

Mostrar que funciona. Cerrar sesión.

**Paso 2 — mostrar el sitio falso**

Abrir browser 2. Señalar que se ve idéntico al legítimo.

**Paso 3 — el ataque**

En browser 2 llenar el form con las mismas credenciales y el código TOTP actual. Hacer submit rápido.

**Paso 4 — mostrar la terminal 2**

Aparece algo así:
```
[14:23:01] ====================================================
[14:23:01] >>> CREDENCIALES CAPTURADAS EN SITIO FALSO <<<
[14:23:01]     Usuario  : usuario
[14:23:01]     Password : password123
[14:23:01]     TOTP     : 482931
[14:23:01] Intentando relay al sitio legitimo...
[14:23:01] ✅ RELAY EXITOSO — Sesion comprometida en el sitio real
[14:23:01] ====================================================
```

**Paso 5 — mostrar lo que ve la víctima**

Browser 2 muestra "Credenciales incorrectas". La víctima no sabe que sus credenciales fueron robadas y usadas.

**Paso 6 — cerrar el argumento**

Volver a browser 1 e ingresar con las mismas credenciales y el mismo código TOTP (si no expiró). El banco real acepta el login.

---

## Si el relay falla

Si en la terminal aparece `❌ RELAY FALLIDO` significa que el código TOTP expiró antes de que llegara el relay. Eso también es útil para la demo: ilustra que la ventana de vulnerabilidad es de exactamente 30 segundos, que es el punto que discute Peeters et al. en el paper de SOS.

---

## Credenciales

| Campo | Valor |
|---|---|
| Usuario | `usuario` |
| Contraseña | `password123` |
| TOTP | código actual del celular |

