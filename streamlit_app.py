import streamlit as st
import sqlite3
import bcrypt
import random
import time

# =========================
# CONFIG
# =========================
st.set_page_config(page_title="PlaySupport Pro", layout="wide")

# =========================
# DB
# =========================
def conectar():
    return sqlite3.connect("ps5.db", check_same_thread=False)

def init_db():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password BLOB
    )
    """)

    conn.commit()
    conn.close()

init_db()

# =========================
# ESTILO PS5
# =========================
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0a0f1f, #020617 80%);
    color: #e5e7eb;
}
.stButton > button {
    border-radius: 12px;
    border: 1px solid #0ea5e9;
    background: #020617;
    color: #0ea5e9;
}
.stButton > button:hover {
    background: #0ea5e9;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION
# =========================
if "login" not in st.session_state:
    st.session_state.login = False

if "page" not in st.session_state:
    st.session_state.page = "login"

# =========================
# 🔐 REGISTRO
# =========================
def registro():
    st.title("📝 Crear cuenta PSN")

    user = st.text_input("Usuario")
    pwd = st.text_input("Contraseña", type="password")

    if st.button("Registrar"):

        if not user or not pwd:
            st.warning("Completa todo")
            return

        hashed = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())

        conn = conectar()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO usuarios(username,password) VALUES(?,?)",
                (user, hashed)
            )
            conn.commit()
            st.success("Cuenta creada ✔")
            st.session_state.page = "login"
            st.rerun()

        except:
            st.error("Usuario ya existe")

        finally:
            conn.close()

    if st.button("⬅ Volver"):
        st.session_state.page = "login"
        st.rerun()

# =========================
# 🔐 LOGIN
# =========================
def login():
    st.title("🔐 PlayStation Login")

    user = st.text_input("Usuario")
    pwd = st.text_input("Contraseña", type="password")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Ingresar"):

            conn = conectar()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT password FROM usuarios WHERE username=?",
                (user,)
            )

            data = cursor.fetchone()
            conn.close()

            if not data:
                st.error("Usuario no existe")
                return

            hashed = data[0]

            try:
                if bcrypt.checkpw(pwd.encode(), hashed):

                    st.session_state.login = True
                    st.session_state.user = user
                    st.session_state.page = "inicio"

                    st.success("Bienvenido 🎮")
                    st.rerun()

                else:
                    st.error("Contraseña incorrecta")

            except:
                st.error("Error en contraseña (hash corrupto)")

    with col2:
        if st.button("Crear cuenta"):
            st.session_state.page = "registro"
            st.rerun()

# =========================
# 🧠 IA SOPORTE
# =========================
def chat_ia():
    st.title("🤖 Soporte IA")

    pregunta = st.text_input("Describe tu problema")

    if st.button("Analizar"):
        if "internet" in pregunta.lower():
            st.success("Problema de red detectado")
        elif "control" in pregunta.lower():
            st.warning("Posible drift en control")
        else:
            st.info("Reinicia la consola")

# =========================
# 📊 DIAGNÓSTICO
# =========================
def diagnostico():
    st.title("🛠 Diagnóstico")

    if st.button("Ejecutar"):
        time.sleep(2)
        temp = random.randint(40, 80)
        st.write(f"Temp: {temp}°C")

        if temp > 70:
            st.error("Sobrecalentamiento")
        else:
            st.success("Todo OK")

# =========================
# 📡 INTERNET
# =========================
def red():
    st.title("📡 Test Internet")

    if st.button("Probar"):
        ping = random.randint(10, 120)
        st.write(f"Ping: {ping}")

# =========================
# 🎮 ERRORES
# =========================
def errores():
    st.title("🎮 Errores PS5")

    error = st.selectbox("Error", [
        "CE-108255-1",
        "NW-102307-3",
        "SU-101312-8"
    ])

    if st.button("Solución"):
        st.info("Solución automática aplicada")

# =========================
# 🏠 INICIO
# =========================
def inicio():
    st.title(f"🎮 Bienvenido {st.session_state.user}")

    if st.button("🛠 Diagnóstico"):
        st.session_state.page = "diag"

    if st.button("📡 Internet"):
        st.session_state.page = "red"

    if st.button("🤖 IA"):
        st.session_state.page = "ia"

    if st.button("🎮 Errores"):
        st.session_state.page = "errores"

    if st.button("🚪 Logout"):
        st.session_state.login = False
        st.session_state.page = "login"
        st.rerun()

# =========================
# ROUTER
# =========================
if not st.session_state.login:

    if st.session_state.page == "login":
        login()
    elif st.session_state.page == "registro":
        registro()

else:

    if st.session_state.page == "inicio":
        inicio()
    elif st.session_state.page == "diag":
        diagnostico()
    elif st.session_state.page == "red":
        red()
    elif st.session_state.page == "ia":
        chat_ia()
    elif st.session_state.page == "errores":
        errores()