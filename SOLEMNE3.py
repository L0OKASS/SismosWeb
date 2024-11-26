import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from streamlit_option_menu import option_menu

### Configuración de la página ###
st.set_page_config(page_title="Sismos en Chile", layout="wide")

### CSS personalizado ###
st.markdown(
    """
    <style>
    /* Fondo del menú lateral */
    [data-testid="stSidebar"] {
        background: url("https://images.myguide-cdn.com/chile/companies/san-pedro-de-atacama-valle-de-la-luna-sunset-tour/large/san-pedro-de-atacama-valle-de-la-luna-sunset-tour-1188322.jpg");
        background-size: cover;
        background-attachment: fixed;
        color: white;
    }

    /* Fondo del contenido principal */
    [data-testid="stAppViewContainer"] {
        background-color: #001f3f;
    }

    /* Títulos y subtítulos con silueta negra */
    h1, h2, h3 {
        color: white;
        text-shadow: 2px 2px 4px black;
    }

    /* Marcos blancos para gráficos */
    .plot-container {
        border: 4px solid white;
        padding: 10px;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

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
    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    st.plotly_chart(fig_bar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

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
    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    st.plotly_chart(fig_pie, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

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
    st.markdown('<div class="plot-container">', unsafe_allow_html=True)
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

elif selected == "Contacto":
    st.title("📧 Contacto")
    st.markdown("### Correo Institucional: lchongv@correo.uss.cl")
    st.markdown("### Correo Personal: lucaschongv69@gmail.com")
    st.image("https://cdn-icons-png.flaticon.com/512/732/732200.png", width=100)

with st.sidebar:
    # Agregar el logo de la universidad
    st.image("https://upload.wikimedia.org/wikipedia/en/thumb/3/3e/Universidad_San_Sebasti%C3%A1n_%28logo%29.png/600px-Universidad_San_Sebasti%C3%A1n_%28logo%29.png", 
             width=200)
    # Menú principal
    selected = option_menu(
        menu_title="Menú Principal",
        options=["Datos", "Gráficos", "Contacto"],
        icons=["table", "bar-chart", "envelope"],
        menu_icon="cast",
        default_index=0,
    )
