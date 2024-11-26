import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from streamlit_option_menu import option_menu

# Configuración de la página
st.set_page_config(page_title="Sismos en Chile", layout="wide")

# CSS personalizado para el diseño
st.markdown(
    """
    <style>
    body {
        background-image: url('https://upload.wikimedia.org/wikipedia/commons/3/3a/Lago_General_Carrera%2C_Chile.jpg');
        background-size: cover;
        background-attachment: fixed;
        color: #FFFFFF;
    }
    .css-18e3th9 {
        background-color: rgba(0, 0, 0, 0.5);
    }
    .css-1d391kg {
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Obtener los datos de la API de sismos
url = "https://api.gael.cloud/general/public/sismos"
response = requests.get(url)
data = response.json()

# Convertir los datos a un DataFrame
df = pd.DataFrame(data)

# Convertir la columna 'Fecha' a tipo datetime
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Extraer las direcciones de la columna 'RefGeografica'
def extract_direction(ref):
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SO', 'O', 'NO']
    for direction in directions:
        if direction in ref:
            return direction
    return 'Desconocida'

# Aplicar la extracción de direcciones a la columna 'RefGeografica'
df['Direccion'] = df['RefGeografica'].apply(extract_direction)

# Calcular el porcentaje de sismos por dirección
direction_counts = df['Direccion'].value_counts()
direction_percentages = (direction_counts / len(df) * 100).round(2)

# Crear un DataFrame para las direcciones con sus porcentajes
direction_df = pd.DataFrame({
    'Direccion': direction_counts.index,
    'Cantidad': direction_counts.values,
    'Porcentaje': direction_percentages.values
})

# Menú lateral
with st.sidebar:
    selected = option_menu(
        menu_title="Menú Principal",
        options=["Datos", "Gráficos", "Contacto"],
        icons=["table", "bar-chart", "envelope"],
        menu_icon="cast",
        default_index=0,
    )

# Mostrar contenido según la selección
if selected == "Datos":
    st.title("Datos de Sismos")
    st.header("Aquí se muestran todos los sismos registrados")
    st.dataframe(df)

elif selected == "Gráficos":
    st.title("Gráficos de Sismos")
    st.header("Análisis Gráfico de los Sismos")

    # Gráfico de barras: Cantidad de sismos por magnitud
    st.subheader("Cantidad de Sismos por Magnitud")
    magnitudes = df['Magnitud'].value_counts().sort_index()

    # Crear un degradado de verde a rojo
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
    fig_bar.update_traces(marker=dict(color=colors))  # Aplicar los colores personalizados

    st.plotly_chart(fig_bar, use_container_width=True)

    # Gráfico de torta: Direcciones con porcentajes
    st.subheader("Distribución de Direcciones de Sismos")
    fig_pie = px.pie(direction_df, values='Cantidad', names='Direccion',
                     title="Direcciones de donde vienen los sismos",
                     hover_data=['Porcentaje'])
    fig_pie.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)

    # Gráfico de dispersión: Relación entre magnitud y profundidad
    st.subheader("Relación entre Magnitud y Profundidad")
    fig_scatter = px.scatter(
        df,
        x='Magnitud',
        y='Profundidad',
        title="Magnitud vs Profundidad",
        labels={'Magnitud': 'Magnitud', 'Profundidad': 'Profundidad (Km)'},
        size=[6] * len(df),  # Tamaño constante de los puntos aumentado
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

elif selected == "Contacto":
    st.title("Contacto")
    st.write("Puedes comunicarte con nosotros a través del correo electrónico.")
    st.image("https://cdn-icons-png.flaticon.com/512/732/732200.png", width=100)
    st.write("Correo Institucional: lchongv@correo.uss.cl")
    st.write("Correo Personal: lucaschongv69@gmail.com")
