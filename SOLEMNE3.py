import streamlit as st
st.set_page_config(page_title="Sismos en Chile", layout="wide")

import pandas as pd
import requests
import plotly.express as px
from streamlit_option_menu import option_menu

### Estilo personalizado para la página ###
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

### Configuración inicial de la página ###
st.set_page_config(page_title="Sismos en Chile", layout="wide")

### Obtener los datos de la API de sismos ###
url = "https://api.gael.cloud/general/public/sismos"
response = requests.get(url)
data = response.json()

### Convertir los datos a un DataFrame ###
df = pd.DataFrame(data)
df['Fecha'] = pd.to_datetime(df['Fecha'])

### Extraer direcciones y calcular porcentajes ###
def extract_direction(ref):
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO']
    for direction in directions:
        if direction in ref:
            return direction
    return 'Desconocida'

df['Direccion'] = df['RefGeografica'].apply(extract_direction)
direction_counts = df['Direccion'].value_counts()
direction_percentages = (direction_counts / len(df) * 100).round(2)
direction_df = pd.DataFrame({
    'Direccion': direction_counts.index,
    'Cantidad': direction_counts.values,
    'Porcentaje': direction_percentages.values
})

### Menú lateral ###
with st.sidebar:
    selected = option_menu(
        menu_title="Menú Principal",
        options=["Datos", "Gráficos", "Contacto"],
        icons=["table", "bar-chart", "envelope"],
        menu_icon="cast",
        default_index=0,
    )

### Mostrar contenido según la selección ###
if selected == "Datos":
    st.title("📋 Datos de Sismos")
    st.dataframe(df)

elif selected == "Gráficos":
    st.title("📊 Gráficos de Sismos")
    
    ### Gráfico de barras con degradado de colores ###
    st.subheader("🔵 Cantidad de Sismos por Magnitud")
    magnitudes = df['Magnitud'].value_counts().sort_index()
    num_colors = len(magnitudes)
    colors = [
        f"rgb({int(255 - (255 * i / (num_colors - 1)))}, {int(255 * i / (num_colors - 1))}, 0)"
        for i in range(num_colors)
    ]
    fig_bar = px.bar(
        magnitudes, 
        x=magnitudes.index, 
        y=magnitudes.values, 
        labels={'x': 'Magnitud', 'y': 'Cantidad de Sismos'}, 
        title="Cantidad de Sismos por Magnitud",
    )
    fig_bar.update_traces(marker=dict(color=colors))
    st.plotly_chart(fig_bar, use_container_width=True)

    ### Gráfico de torta: Direcciones de sismos ###
    st.subheader("🧭 Distribución de Direcciones de Sismos")
    fig_pie = px.pie(
        direction_df, 
        values='Cantidad', 
        names='Direccion', 
        title="Direcciones de los Sismos",
        hover_data=['Porcentaje']
    )
    fig_pie.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

    ### Gráfico de dispersión: Magnitud vs Profundidad ###
    st.subheader("📍 Relación entre Magnitud y Profundidad")
    fig_scatter = px.scatter(
        df, 
        x='Magnitud', 
        y='Profundidad', 
        title="Magnitud vs Profundidad (en Km)",
        labels={'Magnitud': 'Magnitud', 'Profundidad': 'Profundidad (Km)'},
        size=[4] * len(df)
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

elif selected == "Contacto":
    st.title("📧 Contacto")
    st.markdown("### Correo Institucional: *lchongv@correo.uss.cl*")
    st.markdown("### Correo Personal: *lucaschongv69@gmail.com*")
    st.image("https://cdn-icons-png.flaticon.com/512/732/732200.png", width=100)
