import streamlit as st
import queue
import random
import time

# --- CLASES DEL BACKEND ---
class Aficionado:
    contador = 1
    def __init__(self):
        self.__id = Aficionado.contador
        Aficionado.contador += 1
        nombres = ["Juan", "Pedro", "Ana", "Luis", "Carlos", "María", "Sofía", "Diego", "José", "Elena"]
        self.__nombre = random.choice(nombres)
    def get_id(self): return self.__id
    def get_nombre(self): return self.__nombre
    def __str__(self): return f"Aficionado {self.__id}: {self.__nombre}"

class ArenaLuchaLibre:
    def __init__(self):
        self.__cola_entrada = queue.Queue()
        self.__cola_boletos = queue.Queue()
    def agregar_aficionado(self, aficionado):
        self.__cola_entrada.put(aficionado)
    def get_cola_entrada_list(self):
        return list(self.__cola_entrada.queue)
    def atender_siguiente(self):
        if not self.__cola_entrada.empty():
            aficionado = self.__cola_entrada.get()
            self.__cola_boletos.put(aficionado)
            return aficionado
        return None
    def get_boletos_vendidos_list(self):
        return list(self.__cola_boletos.queue)

# --- CONFIGURACIÓN DE STREAMLIT ---
st.set_page_config(page_title="Arena Lucha Libre", page_icon="🤼‍♂️", layout="wide")

st.title("🤼‍♂️ Simulador de Taquilla: Arena Lucha Libre")

# Inicializar variables de estado de forma segura
if 'arena' not in st.session_state:
    st.session_state.arena = ArenaLuchaLibre()
if 'registro' not in st.session_state:
    st.session_state.registro = []

# --- BARRA LATERAL (CONTROLES DIRECTOS) ---
st.sidebar.header("⚙️ Controles")

cantidad = st.sidebar.slider("Aficionados a generar:", 1, 20, 5)

if st.sidebar.button("🏟️ Añadir a la fila"):
    for _ in range(cantidad):
        nuevo = Aficionado()
        st.session_state.arena.agregar_aficionado(nuevo)
        st.session_state.registro.insert(0, f"🎵 Llegó -> {nuevo}")
    # Nota: No usamos st.rerun(), Streamlit recarga la página automáticamente al hacer clic

if st.sidebar.button("🎟️ Atender Siguiente Persona"):
    atendido = st.session_state.arena.atender_siguiente()
    if atendido:
        st.session_state.registro.insert(0, f"✅ Boleto vendido a: {atendido}")
    else:
        st.sidebar.warning("¡Fila vacía!")

if st.sidebar.button("⚡ Vender TODO (Simulación Rápida)"):
    # Procesa la cola completa de un solo golpe sin pausar el renderizado
    while len(st.session_state.arena.get_cola_entrada_list()) > 0:
        atendido = st.session_state.arena.atender_siguiente()
        if atendido:
            st.session_state.registro.insert(0, f"✅ Boleto vendido a: {atendido}")

if st.sidebar.button("🗑️ Reiniciar Todo"):
    st.session_state.arena = ArenaLuchaLibre()
    st.session_state.registro = []
    Aficionado.contador = 1

# --- VISUALIZACIÓN DE COLUMNAS ---
col1, col2, col3 = st.columns(3)

fila_espera = st.session_state.arena.get_cola_entrada_list()
boletos_vendidos = st.session_state.arena.get_boletos_vendidos_list()

with col1:
    st.header(f"🚶 En Fila ({len(fila_espera)})")
    if fila_espera:
        for idx, af() in enumerate(fila_espera):
            if idx == 0:
                st.info(f"👉 **{af}** (Siguiente)")
            else:
                st.text(f"• {af}")
    else:
        st.caption("Fila vacía.")

with col2:
    st.header(f"🎟️ Vendidos ({len(boletos_vendidos)})")
    if boletos_vendidos:
        for af in boletos_vendidos:
            st.success(f"🎟️ {af}")
    else:
        st.caption("Ninguno vendido.")

with col3:
    st.header("📜 Bitácora")
    if st.session_state.registro:
        for evento in st.session_state.registro[:10]:
            st.code(evento, language="text")
    else:
        st.caption("Sin actividad.")
