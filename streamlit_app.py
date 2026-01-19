import streamlit as st
import plotly.graph_objects as go

def calcular_cockcroft_gault(edad, peso, creatinina, sexo):
    """Calcula el aclaramiento de creatinina absoluto."""
    constante_sexo = 0.85 if sexo == 'Mujer' else 1.0
    if creatinina == 0:
        return 0.0
    numerador = (140 - edad) * peso
    denominador = 72 * creatinina
    return (numerador / denominador) * constante_sexo

def obtener_recomendacion(clearence, sexo):
    """Genera el estado y consejo personalizado con identidad local."""
    vocativo = "comadre" if sexo == "Mujer" else "compadre"
    if clearence > 90:
        return "Normal", f"Todo ok {vocativo}, riñones al 100."
    elif 60 <= clearence <= 90:
        return "Leve", f"A echarle una miradita {vocativo}, pero piola."
    elif 30 <= clearence < 60:
        return "Moderada", f"Ojo ahí {vocativo}, ajustar dosis."
    elif 15 <= clearence < 30:
        return "Severa", f"La cosa se puso peluda {vocativo}, control estricto."
    else:
        return "Terminal", f"Situación crítica {vocativo}, a urgencias."

def crear_gauge(valor):
    """Crea el gráfico de medidor visual."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = valor,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Aclaramiento Corregido (mL/min/1.73m²)"},
        gauge = {
            'axis': {'range': [None, 150]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 15], 'color': "red"},
                {'range': [15, 30], 'color': "orange"},
                {'range': [30, 60], 'color': "yellow"},
                {'range': [60, 90], 'color': "lightgreen"},
                {'range': [90, 150], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': valor
            }
        }
    ))
    return fig

# --- CONFIGURACIÓN DE INTERFAZ ---
st.set_page_config(page_title="Calculadora Renal QF Saavedra", page_icon="💊")

# Mostrar logo personalizado (Asegúrate de tener logo.png en tu repo)
try:
    st.image("logo.png", width=150)
except:
    st.warning("⚠️ No se encontró logo.png. Súbelo a GitHub para verlo.")

st.title("💊 Calculadora Renal QF Hosp Saavedra")
st.write("Herramienta avanzada para la estimación de función renal.")

# --- SECCIÓN DE ENTRADAS ---
col1, col2 = st.columns(2)

with col1:
    edad = st.number_input("Edad (años)", min_value=1, max_value=120, value=40)
    peso = st.number_input("Peso (kg)", min_value=1.0, max_value=300.0, value=70.0)
    talla = st.number_input("Talla (cm)", min_value=50.0, max_value=250.0, value=170.0)

with col2:
    creatinina = st.number_input("Creatinina Sérica (mg/dL)", min_value=0.1, max_value=20.0, value=1.0)
    sexo = st.radio("Sexo", ["Hombre", "Mujer"])
    
    # Cálculo automático de Superficie Corporal (BSA) - Fórmula de Mosteller
    bsa = ((peso * talla) / 3600)**0.5
    st.info(f"📍 Superficie Corporal: {bsa:.2f} m²")

# --- LÓGICA DE CÁLCULO ---
if st.button("🚀 Calcular ahora ya"):
    # 1. Cálculo del Cockcroft-Gault Absoluto
    resultado_abs = calcular_cockcroft_gault(edad, peso, creatinina, sexo)
    
    # 2. Ajuste por Superficie Corporal (Estandarizado a 1.73 m2)
    resultado_corr = (resultado_abs * 1.73) / bsa
    
    st.divider()
    
    # 3. Mostrar métricas duales
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.metric("ClCr Absoluto", f"{resultado_abs:.1f} mL/min")
    with m_col2:
        st.metric("ClCr Corregido", f"{resultado_corr:.1f} mL/min", help="Ajustado a 1.73 m²")
    
    # 4. Estado y Recomendación
    estado, consejo = obtener_recomendacion(resultado_abs, sexo)
    st.subheader(f"Estado Clínico: {estado}")
    st.success(f"💡 {consejo}")
    
    # 5. Gráfico Gauge basado en el valor corregido (Estándar clínico)
    st.plotly_chart(crear_gauge(resultado_corr), use_container_width=True)
    
    st.caption("🔍 *Nota: El valor corregido es útil para estandarizar estadios de ERC, pero el absoluto suele usarse para ajuste de dosis de fármacos según prospecto.*")
