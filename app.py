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
    Aficionado.contador = 1

# Inicializar historial de eventos en pantalla
if 'registro' not in st.session_state:
    st.session_state.registro = []

# --- BARRA LATERAL (CONTROLES) ---
st.sidebar.header("⚙️ Controles de la Arena")

# Control para agregar aficionados
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

# --- CREACIÓN DE ESPACIOS EN EL CUERPO PRINCIPAL ---
# Creamos las columnas y los contenedores dinámicos ANTES del proceso de simulación
col1, col2, col3 = st.columns(3)

with col1:
    st.header("🚶 Fila de Espera")
    contenedor_fila = st.empty()  # Contenedor dinámico

with col2:
    st.header("🎟️ Boletos Vendidos")
    contenedor_boletos = st.empty()  # Contenedor dinámico

with col3:
    st.header("📜 Bitácora en vivo")
    contenedor_bitacora = st.empty()  # Contenedor dinámico


# Función interna para refrescar los datos visuales sin recargar la app completa
def actualizar_pantalla():
    fila_espera = st.session_state.arena.get_cola_entrada_list()
    boletos_vendidos = st.session_state.arena.get_boletos_vendidos_list()
    
    # 1. Renderizar Fila de Espera
    with contenedor_fila.container():
        st.markdown(f"**Total en fila:** {len(fila_espera)}")
        if fila_espera:
            for idx, aficionado in enumerate(fila_espera):
                if idx == 0:
                    st.info(f"👉 **{aficionado}** (Siguiente)")
                else:
                    st.write(f"• {aficionado}")
        else:
            st.caption("No hay nadie en la fila.")

    # 2. Renderizar Boletos Vendidos
    with contenedor_boletos.container():
        st.markdown(f"**Total vendidos:** {len(boletos_vendidos)}")
        if boletos_vendidos:
            for aficionado in boletos_vendidos:
                st.success(f"🎟️ {aficionado}")
        else:
            st.caption("Aún no se han vendido boletos.")

    # 3. Renderizar Bitácora
    with contenedor_bitacora.container():
        if st.session_state.registro:
            for evento in st.session_state.registro[:15]:
                st.code(evento, language="text")
        else:
            st.caption("La arena está en silencio...")


# Botón para procesar la fila de manera animada
if st.sidebar.button("🎟️ Vender todos los boletos"):
    status_text = st.sidebar.empty()
    
    # El bucle ahora actualiza los elementos vivos en vez de forzar st.rerun()
    while len(st.session_state.arena.get_cola_entrada_list()) > 0:
        atendido = st.session_state.arena.atender_siguiente()
        if atendido:
            st.session_state.registro.insert(0, f"✅ Boleto vendido a: {atendido}")
            status_text.text(f"Atendiendo a... {atendido.get_nombre()}")
            
            # Refrescamos la UI dinámicamente
            actualizar_pantalla()
            time.sleep(velocidad)
            
    status_text.success("¡Todos atendidos!")
    st.rerun() # Un único rerun al final para estabilizar el estado

if st.sidebar.button("🗑️ Reiniciar Arena"):
    st.session_state.arena = ArenaLuchaLibre()
    st.session_state.registro = []
    Aficionado.contador = 1
    st.rerun()

# Carga inicial de la pantalla
actualizar_pantalla()
