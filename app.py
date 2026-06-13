import streamlit as st
import queue
import random
import time

# ==========================================
# 1. BACKEND CORREGIDO (LÓGICA DEL SISTEMA)
# ==========================================
class Aficionado:
    contador = 1

    def __init__(self):
        self._id = Aficionado.contador
        Aficionado.contador += 1
        nombres = ["Juan", "Pedro", "Ana", "Luis", "Carlos",
                   "María", "Sofía", "Diego", "José", "Elena"]
        self._nombre = random.choice(nombres)

    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def __str__(self):
        return f"Aficionado {self._id}: {self._nombre}"


class ArenaLuchaLibre:
    def __init__(self):
        # Cambiado de __ a _ para evitar el Name Mangling que rompía Streamlit
        self._cola_entrada = queue.Queue()
        self._cola_boletos = queue.Queue()

    def agregar_aficionado(self, aficionado):
        self._cola_entrada.put(aficionado)

    def atender_siguiente(self):
        if not self._cola_entrada.empty():
            aficionado = self._cola_entrada.get()
            self._cola_boletos.put(aficionado)
            return aficionado
        return None

    # Métodos limpios para que el Frontend pueda mirar dentro de las colas sin romperlas
    def obtener_lista_espera(self):
        return list(self._cola_entrada.queue)

    def obtener_lista_vendidos(self):
        return list(self._cola_boletos.queue)


# ==========================================
# 2. FRONTEND (INTERFAZ DE STREAMLIT)
# ==========================================
st.set_page_config(page_title="Arena Lucha Libre", page_icon="🤼‍♂️", layout="wide")

st.title("🤼‍♂️ Sistema de Taquilla: Arena Lucha Libre")
st.markdown("Gestión interactiva de colas de aficionados utilizando las clases de tu Backend.")

# Mantener el estado de la arena guardado en la sesión web
if 'arena' not in st.session_state:
    st.session_state.arena = ArenaLuchaLibre()
if 'historial' not in st.session_state:
    st.session_state.historial = []

# --- PANEL DE ACCIONES (BARRA LATERAL) ---
st.sidebar.header("⚙️ Operaciones de Taquilla")

# Input para meter múltiples aficionados
cantidad = st.sidebar.number_input("Aficionados a registrar:", min_value=1, max_value=50, value=5)

if st.sidebar.button("🏟️ Hacer ingresar a la Fila", use_container_width=True):
    for _ in range(cantidad):
        nuevo_aficionado = Aficionado()
        st.session_state.arena.agregar_aficionado(nuevo_aficionado)
        st.session_state.historial.insert(0, f"🚶 Llegó -> {nuevo_aficionado}")

st.sidebar.markdown("---")

# Botón para simular la taquilla paso a paso
if st.sidebar.button("🎟️ Procesar Siguiente Cliente", use_container_width=True):
    atendido = st.session_state.arena.atender_siguiente()
    if atendido:
        st.session_state.historial.insert(0, f"✅ Boleto vendido a -> {atendido}")
    else:
        st.sidebar.warning("¡No hay nadie más en la fila!")

# Botón de reset de emergencia
if st.sidebar.button("🗑️ Reiniciar Simulador", use_container_width=True):
    st.session_state.arena = ArenaLuchaLibre()
    st.session_state.historial = []
    Aficionado.contador = 1
    st.toast("Arena restablecida por completo")

# --- ÁREA VISUAL PRINCIPAL (COLUMNAS DE FLUJO) ---
col_fila, col_boletos, col_bitacora = st.columns(3)

# Solicitamos de forma segura las listas al backend corregido
fila_actual = st.session_state.arena.obtener_lista_espera()
boletos_actual = st.session_state.arena.obtener_lista_vendidos()

with col_fila:
    st.header(f"🚶 Fila de Espera ({len(fila_actual)})")
    if fila_actual:
        for idx, persona in enumerate(fila_actual):
            if idx == 0:
                st.info(f"🏽 **Al frente:** {persona}")
            else:
                st.write(f"• {persona}")
    else:
        st.caption("Fila vacía. Agrega aficionados desde la barra lateral.")

with col_boletos:
    st.header(f"🎟️ Boletos Entregados ({len(boletos_actual)})")
    if boletos_actual:
        for persona in boletos_actual:
            st.success(f"🎟️ {persona}")
    else:
        st.caption("Aún no se registran ventas.")

with col_bitacora:
    st.header("📜 Bitácora de Eventos")
    if st.session_state.historial:
        for evento in st.session_state.historial[:10]: # Limitado a los últimos 10 movimientos
            st.text(evento)
    else:
        st.caption("Sin actividad reciente.")
