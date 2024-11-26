import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Estilo personalizado para la página
page_bg_img = '''
<style>
[data-testid="stAppViewContainer"] {
    background: url("https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Valle_de_la_Luna_San_Pedro_de_Atacama_Chile_Luca_Galuzzi_2006.JPG/1920px-Valle_de_la_Luna_San_Pedro_de_Atacama_Chile_Luca_Galuzzi_2006.JPG");
    background-size: cover;
    background-attachment: fixed;
    opacity: 0.9;
}
[data-testid="stSidebar"] {
    background-color: rgba(255, 255, 255, 0.8);
}
h1, h2, h3, .stMarkdown {
    color: #2c3e50;
    font-family: 'Arial', sans-serif;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Configuración de la página
st.set_page_config(page_title="Sismos en Chile", layout="wide")

# Título principal
st.title("🌍 Análisis de Sismos en Chile")
st.markdown("Explora datos de sismos en Chile con gráficos interactivos y un diseño amigable.")

# Cargar datos de la API
@st.cache
def obtener_datos():
    url = "https://api.gael.cloud/general/public/sismos"
    return pd.DataFrame(pd.json_normalize(requests.get(url).json()))

datos = obtener_datos()

# Sidebar con menú
with st.sidebar:
    opcion = st.radio(
        "Menú",
        options=["Datos de Sismos", "Gráficos", "Contacto"]
    )

if opcion == "Datos de Sismos":
    st.header("📋 Datos de Sismos")
    st.dataframe(datos)

elif opcion == "Gráficos":
    st.header("📊 Gráficos de Sismos")

    # Gráfico de barras - Magnitud de los sismos
    st.subheader("🔵 Magnitud de los sismos")
    fig_barras = px.bar(
        datos,
        x="Magnitud",
        y="RefGeografica",
        title="Magnitud por ubicación geográfica",
        color="Magnitud",
        color_continuous_scale=px.colors.sequential.Viridis_r
    )
    st.plotly_chart(fig_barras)

    # Gráfico de torta - Direcciones de los sismos
    st.subheader("🧭 Direcciones de donde vienen")
    direcciones = datos["RefGeografica"].str.extract(r'(\d+)\s+km\s+al\s+(\w+)')
    direcciones.columns = ["Distancia", "Direccion"]
    direcciones["Direccion"] = direcciones["Direccion"].replace({
        "N": "Norte", "S": "Sur", "E": "Este", "O": "Oeste",
        "NE": "Noreste", "SE": "Sureste", "NO": "Noroeste", "SO": "Suroeste"
    })
    conteo_direcciones = direcciones["Direccion"].value_counts()
    fig_torta = px.pie(
        conteo_direcciones,
        names=conteo_direcciones.index,
        values=conteo_direcciones.values,
        title="Distribución de direcciones de los sismos"
    )
    st.plotly_chart(fig_torta)

    # Gráfico de dispersión - Profundidad y Magnitud
    st.subheader("📍 Magnitud y Profundidad")
    fig_dispersion = px.scatter(
        datos,
        x="Magnitud",
        y="Profundidad",
        size="Magnitud",
        title="Relación entre Magnitud y Profundidad (en km)",
        labels={"Profundidad": "Profundidad (km)", "Magnitud": "Magnitud"}
    )
    st.plotly_chart(fig_dispersion)

elif opcion == "Contacto":
    st.header("📧 Contacto")
    st.markdown("*Correo:* contacto@ejemplo.com")
    st.image("https://upload.wikimedia.org/wikipedia/commons/8/89/Email_Icon.png", width=50)
