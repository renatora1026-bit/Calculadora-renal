import streamlit as st
import plotly.graph_objects as go

def calcular_cockcroft_gault(edad, peso, creatinina, sexo):
    """
    Calcula el aclaramiento de creatinina usando la fórmula de Cockcroft-Gault.
    """
    constante_sexo = 0.85 if sexo == 'Mujer' else 1.0
    
    if creatinina == 0:
        return 0.0
        
    numerador = (140 - edad) * peso
    denominador = 72 * creatinina
    
    resultado = (numerador / denominador) * constante_sexo
    return resultado

def obtener_recomendacion(clearence):
    if clearence > 90:
        return "Normal", "Todo ok compadre/comadre, riñones al 100."
    elif 60 <= clearence <= 90:
        return "Leve", "A echarle una miradita, pero piola."
    elif 30 <= clearence < 60:
        return "Moderada", "Ojo ahí, ajustar dosis."
    elif 15 <= clearence < 30:
        return "Severa", "La cosa se puso peluda, control estricto."
    else:
        return "Terminal", "Situación crítica, a urgencias."

def crear_gauge(valor):
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = valor,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Aclaramiento (mL/min)"},
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

# Configuración de la página
st.set_page_config(page_title="Calculadora Renal Chilensis", page_icon="🩺")

# Título y descripción
st.title("🩺 Calculadora de Riñones (Cockcroft-Gault)")
st.write("Bienvenido a la herramienta pa' ver cómo andan los filtros.")

# Inputs en la barra lateral o principal
col1, col2 = st.columns(2)

with col1:
    edad = st.number_input("Edad (años)", min_value=1, max_value=120, value=40)
    peso = st.number_input("Peso (kg)", min_value=1.0, max_value=300.0, value=70.0)

with col2:
    creatinina = st.number_input("Creatinina Sérica (mg/dL)", min_value=0.1, max_value=20.0, value=1.0)
    sexo = st.radio("Sexo", ["Hombre", "Mujer"])

# Botón de cálculo
if st.button("Calcular ahora ya"):
    resultado = calcular_cockcroft_gault(edad, peso, creatinina, sexo)
    estado, consejo = obtener_recomendacion(resultado)
    
    st.divider()
    
    # Mostrar resultados
    st.header(f"Resultado: {resultado:.2f} mL/min")
    st.subheader(f"Estado: {estado}")
    st.info(f"💡 {consejo}")
    
    # Gráfico
    st.plotly_chart(crear_gauge(resultado), use_container_width=True)
    
    st.caption("*Nota: Esto es solo referencial, consulte a su doc.*")
