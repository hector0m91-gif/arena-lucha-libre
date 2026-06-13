import streamlit as st
import queue
import random
import time

# --- COPIA DEL BACKEND INTEGRADA ---
class Aficionado:
    contador = 1

    def __init__(self):
        self.__id = Aficionado.contador
        Aficionado.contador += 1
        nombres = ["Juan", "Pedro", "Ana", "Luis", "Carlos",
                   "María", "Sofía", "Diego", "José", "Elena"]
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

    # Métodos modificados para retornar las listas y poder visualizarlas en Streamlit
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


# --- CONFIGURACIÓN DE LA INTERFAZ DE STREAMLIT ---
st.set_page_config(page_title="Arena Lucha Libre", page_icon="🤼‍♂️", layout="wide")

st.title("🤼‍♂️ Simulador de Taquilla: Arena Lucha Libre")
st.markdown("¡Bienvenido a la simulación de venta de boletos! Controla la fila de aficionados en tiempo real.")

# Inicializar la arena en el estado de la sesión si no existe
if 'arena' not in st.session_state:
    st.session_state.arena = ArenaLuchaLibre()
    # Reiniciar el contador de aficionados por si se recarga la app
    Aficionado.contador = 1

# Inicializar historial de eventos en pantalla
if 'registro' not in st.session_state:
    st.session_state.registro = []

# --- BARRA LATERAL (CONTROLES) ---
st.sidebar.header("⚙️ Controles de la Arena")

# Control para agregar aficionados de golpe
cantidad_aficionados = st.sidebar.slider("Aficionados a generar:", min_value=1, max_value=20, value=5)
if st.sidebar.button("🏟️ Llegar a la fila"):
    for _ in range(cantidad_aficionados):
        nuevo_aficionado = Aficionado()
        st.session_state.arena.agregar_aficionado(nuevo_aficionado)
        st.session_state.registro.insert(0, f"🎵 Llegó -> {nuevo_aficionado}")
    st.rerun()

st.sidebar.markdown("---")

# Control de simulación automática
st.sidebar.subheader("⚡ Simulación Automática")
velocidad = st.sidebar.slider("Velocidad de atención (segundos):", min_value=0.1, max_value=2.0, value=0.5)

if st.sidebar.button("🎟️ Vender todos los boletos"):
    # Contenedor dinámico para ver el progreso
    status_text = st.sidebar.empty()
    
    while len(st.session_state.arena.get_cola_entrada_list()) > 0:
        atendido = st.session_state.arena.atender_siguiente()
        if atendido:
            st.session_state.registro.insert(0, f"✅ Boleto vendido a: {atendido}")
            # Forzar actualización visual recreando el layout en cada iteración
            status_text.text(f"Atendiendo a... {atendido.get_nombre()}")
            time.sleep(velocidad)
            st.rerun()
    status_text.success("¡Todos atendidos!")

if st.sidebar.button("🗑️ Reiniciar Arena"):
    st.session_state.arena = ArenaLuchaLibre()
    st.session_state.registro = []
    Aficionado.contador = 1
    st.rerun()


# --- CUERPO PRINCIPAL (VISUALIZACIÓN) ---
col1, col2, col3 = st.columns(3)

# Obtener los datos actuales de las colas
fila_espera = st.session_state.arena.get_cola_entrada_list()
boletos_vendidos = st.session_state.arena.get_boletos_vendidos_list()

with col1:
    st.header(f"🚶 Fila de Espera ({len(fila_espera)})")
    if fila_espera:
        for idx, aficionado in enumerate(fila_espera):
            # Resaltar al primero de la fila
            if idx == 0:
                st.info(f"👉 **{aficionado}** (Siguiente en pasar)")
            else:
                st.write(f"• {aficionado}")
    else:
        st.caption("No hay nadie en la fila. ¡Agrega aficionados desde la barra lateral!")

with col2:
    st.header(f"🎟️ Boletos Vendidos ({len(boletos_vendidos)})")
    if boletos_vendidos:
        for aficionado in boletos_vendidos:
            st.success(f"🎟️ {aficionado}")
    else:
        st.caption("Aún no se han vendido boletos.")

with col3:
    st.header("📜 Bitácora en vivo")
    if st.session_state.registro:
        # Mostrar los últimos movimientos
        for evento in st.session_state.registro[:15]:  # Limitado a los últimos 15 para no saturar
            st.code(evento, language="text")
    else:
        st.caption("La arena está en silencio...")