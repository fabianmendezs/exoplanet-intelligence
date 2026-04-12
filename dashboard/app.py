import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import plotly.io as pio
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Exoplanet Intelligence",
    page_icon="🪐",
    layout="wide"
)

@st.cache_data
def cargar_datos():
    import os
    import requests

    if not os.path.exists("data/exoplanets.db"):
        url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
        params = {
            "query": "SELECT pl_name,hostname,pl_masse,pl_rade,pl_orbper,pl_eqt,st_teff,discoverymethod,disc_year FROM ps WHERE default_flag=1",
            "format": "json"
        }
        response = requests.get(url, params=params)
        df = pd.DataFrame(response.json())
        return df
    else:
        conn = duckdb.connect("data/exoplanets.db")
        df = conn.execute("SELECT * FROM main.stg_exoplanets").df()
        conn.close()
        return df

df = cargar_datos()

st.title("🪐 Exoplanet Intelligence")
st.markdown("Análisis de exoplanetas con datos reales de NASA")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total planetas", f"{len(df):,}")
col2.metric("Con zona habitable", len(df[df['tipo_planeta'] == 'Habitable']))
col3.metric("Métodos detección", df['metodo_descubrimiento'].nunique())
col4.metric("Años de datos", f"{int(df['año_descubrimiento'].min())}–{int(df['año_descubrimiento'].max())}")

st.divider()

tab1, tab2, tab3 = st.tabs(["Explorar", "Visualizaciones", "Agente IA"])

with tab1:
    st.subheader("Buscar planeta")
    planeta_seleccionado = st.selectbox(
        "Selecciona un planeta",
        options=sorted(df['nombre_planeta'].tolist())
    )
    
    datos = df[df['nombre_planeta'] == planeta_seleccionado].iloc[0]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Radio", f"{datos['radio_terrestre']} R⊕" if pd.notna(datos['radio_terrestre']) else "Sin datos")
    c2.metric("Temperatura", f"{datos['temperatura_k']} K" if pd.notna(datos['temperatura_k']) else "Sin datos")
    c3.metric("Período orbital", f"{round(datos['periodo_orbital_dias'], 1)} días" if pd.notna(datos['periodo_orbital_dias']) else "Sin datos")
    
    st.info(f"**Tipo:** {datos['tipo_planeta']} | **Descubierto:** {datos['año_descubrimiento']} | **Método:** {datos['metodo_descubrimiento']}")

with tab2:
    st.subheader("Distribución por tipo de planeta")
    conteo = df['tipo_planeta'].value_counts().reset_index()
    conteo.columns = ['tipo', 'cantidad']
    fig1 = px.bar(conteo, x='tipo', y='cantidad', color='tipo')
    st.plotly_chart(fig1, use_container_width=True)
    
    st.subheader("Descubrimientos por año")
    por_año = df.groupby('año_descubrimiento').size().reset_index()
    por_año.columns = ['año', 'cantidad']
    fig2 = px.line(por_año, x='año', y='cantidad', markers=True)
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("Análisis con IA")
    planeta_ia = st.selectbox(
        "Selecciona un planeta para analizar",
        options=sorted(df['nombre_planeta'].tolist()),
        key="ia_select"
    )
    
    if st.button("Generar reporte con IA"):
        datos_ia = df[df['nombre_planeta'] == planeta_ia].iloc[0]
        
        prompt = f"""Eres un astrónomo experto. Analiza estos datos reales de NASA y genera 
un reporte científico breve en español sobre el exoplaneta {datos_ia['nombre_planeta']}.

Datos:
- Tipo: {datos_ia['tipo_planeta']}
- Radio: {datos_ia['radio_terrestre']} radios terrestres
- Temperatura: {datos_ia['temperatura_k']} K
- Período orbital: {datos_ia['periodo_orbital_dias']} días
- Estrella: {datos_ia['estrella']} ({datos_ia['temperatura_estrella_k']} K)
- Descubierto: {datos_ia['año_descubrimiento']} por {datos_ia['metodo_descubrimiento']}

Incluye comparación con la Tierra y posibilidad de habitabilidad."""

        with st.spinner("Generando análisis..."):
            client = Groq(api_key=os.getenv("GROQ_API_KEY"))
            respuesta = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}]
            )
            st.markdown(respuesta.choices[0].message.content)