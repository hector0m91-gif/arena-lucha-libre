import streamlit as st
import random

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Arena Lucha Libre", page_icon="🤼‍♂️", layout="wide")

st.title("🤼‍♂️ Control de Taquilla - Arena Lucha Libre")
st.markdown("Manejo de flujo de aficionados en tiempo real.")

# --- INICIALIZACIÓN DE VARIABLES DE ESTADO ---
# Usamos listas simples de Python guardadas en la sesión, 100% compatible con Streamlit Cloud
if 'fila_espera' not in st.session_state:
    st.session_state.fila_espera = []
if 'boletos_vendidos' not in st.session_state:
    st.session_state.boletos_vendidos = []
if 'contador_id' not in st.session_state:
    st.session_state.contador_id = 1

# --- FUNCIONES DE ACCIÓN ---
def agregar_aficionado():
    nombres = ["Juan", "Pedro", "Ana", "Luis", "Carlos", "María", "Sofía", "Diego", "José", "Elena"]
    nuevo = f"Aficionado {st.session_state.contador_id}: {random.choice(nombres)}"
    st.session_state.fila_espera.append(nuevo)
    st.session_state.contador_id += 1

def atender_siguiente():
    if st.session_state.fila_espera:
        atendido = st.session_state.fila_espera.pop(0) # Saca al primero de la fila
        st.session_state.boletos_vendidos.append(atendido) # Lo manda a boletos vendidos
    else:
        st.toast("⚠️ ¡La fila está vacía!")

def reiniciar_arena():
    st.session_state.fila_espera = []
    st.session_state.boletos_vendidos = []
    st.session_state.contador_id = 1
    st.toast("🏟️ Arena reiniciada")

# --- BOTONES PRINCIPALES ---
col_b1, col_b2, col_b3 = st.columns(3)
with col_b1:
    if st.button("🏟️ Llegar a la Fila (+1)", use_container_width=True):
        agregar_aficionado()
with col_b2:
    if st.button("🎟️ Atender Siguiente", use_container_width=True):
        atender_siguiente()
with col_b3:
    if st.button("🗑️ Reiniciar Todo", use_container_width=True):
        reiniciar_arena()

st.markdown("---")

# --- VISUALIZACIÓN DEL FLUJO ---
col_izq, col_der = st.columns(2)

with col_izq:
    st.header(f"🚶 Fila de Espera ({len(st.session_state.fila_espera)})")
    if st.session_state.fila_espera:
        for idx, persona in enumerate(st.session_state.fila_espera):
            if idx == 0:
                st.info(f"👉 **{persona}** (Siguiente en taquilla)")
            else:
                st.text(f"• {persona}")
    else:
        st.caption("No hay nadie en la fila.")

with col_der:
    st.header(f"🎟️ Boletos Vendidos ({len(st.session_state.boletos_vendidos)})")
    if st.session_state.boletos_vendidos:
        for persona in st.session_state.boletos_vendidos:
            st.success(f"✅ {persona} ya tiene su boleto")
    else:
        st.caption("Aún no se han vendido boletos.")
