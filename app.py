import streamlit as st
import queue
import random
import time

# --- 1. CLASES DEL BACKEND (LÓGICA) ---
class Aficionado:
    contador = 1
    
    def __init__(self):
        self.__id = Aficionado.contador
        Aficionado.contador += 1
        nombres = ["Juan", "Pedro", "Ana", "Luis", "Carlos", "María", "Sofía", "Diego", "José", "Elena"]
        self.__nombre = random.choice(nombres)
        
    def get_id(self): 
        return self.__id
        
    def get_nombre(self): 
        return self.__nombre
        
    def __str__(self): 
        return f"Aficionado {self.__id}: {self.__nombre}"

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

# --- 2. CONFIGURACIÓN DE LA INTERFAZ ---
st.set_page_config(page_title="Taquilla Arena Lucha Libre", page_icon="🤼‍♂️", layout="wide")

st.title("🤼‍♂️ Control de Flujo: Taquilla Lucha Libre")
st.markdown("Una interfaz sencilla para gestionar la fila de aficionados paso a paso.")

# Inicializar estados de manera segura
if 'arena' not in st.session_state:
    st.session_state.arena = ArenaLuchaLibre()
if 'registro' not in st.session_state:
    st.session_state.registro = []

# --- 3. BOTONES DE ACCIÓN (PANEL SUPERIOR) ---
st.subheader("🕹️ Panel de Control")
col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)

with col_btn1:
    if st.button("🏟️ Agregar 1 Persona a la Fila", use_container_width=True):
        nuevo = Aficionado()
        st.session_state.arena.agregar_aficionado(nuevo)
        st.session_state.registro.insert(0, f" Walk-in: Llegó {nuevo.get_nombre()} (ID: {nuevo.get_id()})")

with col_btn2:
    if st.button("👥 Agregar 5 Personas", use_container_width=True):
        for _ in range(5):
            nuevo = Aficionado()
            st.session_state.arena.agregar_aficionado(nuevo)
            st.session_state.registro.insert(0, f" Fila: Llegó {nuevo.get_nombre()} (ID: {nuevo.get_id()})")

with col_btn3:
    if st.button("🎟️ Atender Siguiente", use_container_width=True):
        atendido = st.session_state.arena.atender_siguiente()
        if atendido:
            st.session_state.registro.insert(0, f" Taquilla: Boleto entregado a {atendido.get_nombre()}")
        else:
            st.toast("⚠️ ¡No hay nadie en la fila para atender!")

with col_btn4:
    if st.button("🗑️ Vaciar / Reiniciar Arena", use_container_width=True):
        st.session_state.arena = ArenaLuchaLibre()
        st.session_state.registro = []
        Aficionado.contador = 1
        st.toast("🏟️ ¡Arena vacía y lista!")

st.markdown("---")

# --- 4. REPRESENTACIÓN VISUAL DEL FLUJO ---
col_fila, col_taquilla, col_exito = st.columns(3)

fila_actual = st.session_state.arena.get_cola_entrada_list()
vendidos_actual = st.session_state.arena.get_boletos_vendidos_list()

# COLUMNA 1: FILA DE ESPERA
with col_fila:
    st.header(f"🚶 1. Fila de Espera ({len(fila_actual)})")
    if fila_actual:
        for idx, persona in enumerate(fila_actual):
            if idx == 0:
                st.warning(f"🏽 **Siguiente en pasar:** {persona.get_nombre()} (ID: {persona.get_id()})")
            else:
                st.info(f"• {persona.get_nombre()} (ID: {persona.get_id()})")
    else:
        st.caption("Fila vacía. Usa los botones de arriba para meter gente.")

# COLUMNA 2: LA TAQUILLA (QUIÉN ESTÁ SIENDO ATENDIDO)
with col_taquilla:
    st.header("🏪 2. Estado de Taquilla")
    if fila_actual:
        en_ventanilla = fila_actual[0]
        st.success(f"Atendiendo justo ahora a:\n\n### **{en_ventanilla.get_nombre()}**\n*(ID: {en_ventanilla.get_id()})*")
        st.caption("Haz clic en 'Atender Siguiente' para darle su boleto.")
    else:
        st.markdown("### Ventanilla Cerrada 🛑")
        st.caption("No hay nadie esperando en este momento.")

# COLUMNA 3: BOLETOS EN MANO
with col_exito:
    st.header(f"🎟️ 3. Boletos Vendidos ({len(vendidos_actual)})")
    if vendidos_actual:
        for persona in vendidos_actual:
            st.markdown(f"💚 **{persona.get_nombre()}** (ID: {persona.get_id()}) ya entró al evento.")
    else:
        st.caption("Nadie ha comprado boleto todavía.")

# --- 5. LOG / BITÁCORA AL FINAL ---
st.markdown("---")
st.subheader("📜 Historial de Movimientos")
if st.session_state.registro:
    for item in st.session_state.registro[:8]: # Muestra los últimos 8 eventos
        st.text(item)
else:
    st.caption("Esperando acciones...")
