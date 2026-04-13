import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px
import os
from groq import Groq
from dotenv import load_dotenv
import requests

load_dotenv()

st.set_page_config(
    page_title="Exoplanet Intelligence",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');
    html, body, .stApp {
        background: #050a1a !important;
        font-family: 'Rajdhani', sans-serif;
        color: #ffffff;
    }
    header[data-testid="stHeader"] {
        background: #050a1a !important;
        border-bottom: 1px solid rgba(0,212,255,0.1);
    }
    section[data-testid="stSidebar"] { display: none; }
    h1, h2, h3 {
        font-family: 'Orbitron', monospace !important;
        color: #00d4ff !important;
        text-shadow: 0 0 20px rgba(0,212,255,0.4);
    }
    p, span, label, li { color: #ffffff !important; }
    .metric-box {
        background: rgba(0,212,255,0.05);
        border: 1px solid rgba(0,212,255,0.2);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .metric-box h2 { font-size: 2em !important; margin: 0 !important; color: #00d4ff !important; }
    .metric-box p { color: rgba(0,212,255,0.7) !important; margin: 4px 0 0 0; font-size: 0.85em; letter-spacing: 2px; }
    .planet-card {
        background: rgba(0,212,255,0.04);
        border: 1px solid rgba(0,212,255,0.2);
        border-radius: 16px;
        padding: 24px;
        margin: 12px 0;
    }
    .habitable-badge {
        background: linear-gradient(135deg, #00ff87, #00d4ff);
        color: #000 !important;
        padding: 3px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 11px;
        letter-spacing: 1px;
    }
    div[data-baseweb="select"] > div {
        background: #0d1b3e !important;
        border: 1px solid rgba(0,212,255,0.3) !important;
        color: #ffffff !important;
    }
    div[data-baseweb="select"] span { color: #ffffff !important; }
    div[data-baseweb="popover"],
    div[data-baseweb="popover"] > div,
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] li,
    div[role="listbox"],
    div[role="option"],
    li[role="option"] {
        background: #0d1b3e !important;
        color: #ffffff !important;
    }
    li[role="option"]:hover,
    div[role="option"]:hover {
        background: rgba(0,212,255,0.2) !important;
        color: #00d4ff !important;
    }
    input, textarea {
        background: #0d1b3e !important;
        border: 1px solid rgba(0,212,255,0.3) !important;
        color: #ffffff !important;
        font-family: 'Rajdhani', sans-serif !important;
    }
    input::placeholder, textarea::placeholder { color: rgba(255,255,255,0.7) !important; }
    .stButton > button {
        background: linear-gradient(135deg, #0d4f8c, #0099cc) !important;
        color: #ffffff !important;
        border: 1px solid rgba(0,212,255,0.4) !important;
        border-radius: 8px !important;
        font-family: 'Orbitron', monospace !important;
        font-size: 11px !important;
        letter-spacing: 1px !important;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Orbitron', monospace !important;
        font-size: 11px !important;
        letter-spacing: 1px;
        color: rgba(0,212,255,0.6) !important;
        background: transparent !important;
    }
    .stTabs [aria-selected="true"] {
        color: #00d4ff !important;
        border-bottom: 2px solid #00d4ff !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 1px solid rgba(0,212,255,0.15);
    }
    .chat-user {
        background: rgba(0,212,255,0.08);
        border-left: 3px solid #00d4ff;
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
    }
    .chat-agent {
        background: rgba(157,111,255,0.08);
        border-left: 3px solid #9d6fff;
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def cargar_datos():
    if not os.path.exists("data/exoplanets.db"):
        url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
        params = {
            "query": "SELECT pl_name,hostname,pl_masse,pl_rade,pl_orbper,pl_eqt,st_teff,discoverymethod,disc_year FROM ps WHERE default_flag=1",
            "format": "json"
        }
        response = requests.get(url, params=params)
        df = pd.DataFrame(response.json())
        df = df.rename(columns={
            'pl_name': 'nombre_planeta',
            'hostname': 'estrella',
            'pl_masse': 'masa_terrestre',
            'pl_rade': 'radio_terrestre',
            'pl_orbper': 'periodo_orbital_dias',
            'pl_eqt': 'temperatura_k',
            'st_teff': 'temperatura_estrella_k',
            'discoverymethod': 'metodo_descubrimiento',
            'disc_year': 'año_descubrimiento'
        })
        df['tipo_planeta'] = df.apply(lambda r:
            'Habitable' if pd.notna(r['temperatura_k']) and pd.notna(r['radio_terrestre']) and 200 <= r['temperatura_k'] <= 320 and r['radio_terrestre'] <= 1.5
            else 'Rocoso' if pd.notna(r['radio_terrestre']) and r['radio_terrestre'] <= 1.5
            else 'Super-Tierra' if pd.notna(r['radio_terrestre']) and r['radio_terrestre'] <= 4
            else 'Gigante gaseoso' if pd.notna(r['radio_terrestre']) and r['radio_terrestre'] <= 10
            else 'Gigante extremo', axis=1)
        return df
    else:
        conn = duckdb.connect("data/exoplanets.db")
        df = conn.execute("SELECT * FROM main.stg_exoplanets").df()
        conn.close()
        return df

df = cargar_datos()

COLORES = {
    'Habitable': '#00ff87',
    'Rocoso': '#4da6ff',
    'Super-Tierra': '#a78bfa',
    'Gigante gaseoso': '#fbbf24',
    'Gigante extremo': '#fb7185'
}

LAYOUT_BASE = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    title_font=dict(color='#ffffff', size=14),
    font=dict(color='#ffffff'),
    legend=dict(font=dict(color='#ffffff'), bgcolor='rgba(0,0,0,0)'),
    xaxis=dict(color='#ffffff', gridcolor='rgba(255,255,255,0.1)'),
    yaxis=dict(color='#ffffff', gridcolor='rgba(255,255,255,0.1)')
)

año_min = int(df['año_descubrimiento'].min())
año_max = int(df['año_descubrimiento'].max())

# HEADER
st.markdown("""
<div style='text-align:center; padding:48px 0 24px 0;'>
    <h1 style='font-size:3em; letter-spacing:6px; margin-bottom:8px'>🪐 EXOPLANET INTELLIGENCE</h1>
    <p style='color:rgba(0,212,255,0.6); font-size:1.1em; letter-spacing:3px'>
        ANÁLISIS DE EXOPLANETAS · DATOS REALES NASA · IA INTEGRADA
    </p>
</div>
""", unsafe_allow_html=True)

# FILTROS GLOBALES
f1, f2, f3 = st.columns(3)
with f1:
    tipo_op = ["— Todos los tipos —"] + sorted(df['tipo_planeta'].unique().tolist())
    tipo_sel = st.selectbox("Tipo de planeta", options=tipo_op, index=0)
with f2:
    df_por_tipo = df[df['tipo_planeta'] == tipo_sel] if tipo_sel != "— Todos los tipos —" else df
    metodo_op = ["— Todos los métodos —"] + sorted(df_por_tipo['metodo_descubrimiento'].unique().tolist())
    metodo_sel = st.selectbox("Método de descubrimiento", options=metodo_op, index=0)
with f3:
    rango_años = st.slider("Rango de años", año_min, año_max, (año_min, año_max))

# Recalcular tipos disponibles según método
if metodo_sel != "— Todos los métodos —":
    tipos_disponibles = sorted(df[df['metodo_descubrimiento'] == metodo_sel]['tipo_planeta'].unique().tolist())
    tipo_op_actualizado = ["— Todos los tipos —"] + tipos_disponibles
    if tipo_sel not in tipo_op_actualizado:
        tipo_sel = "— Todos los tipos —"

# APLICAR FILTROS
df_filtrado = df.copy()
if tipo_sel != "— Todos los tipos —":
    df_filtrado = df_filtrado[df_filtrado['tipo_planeta'] == tipo_sel]
if metodo_sel != "— Todos los métodos —":
    df_filtrado = df_filtrado[df_filtrado['metodo_descubrimiento'] == metodo_sel]
df_filtrado = df_filtrado[
    (df_filtrado['año_descubrimiento'] >= rango_años[0]) &
    (df_filtrado['año_descubrimiento'] <= rango_años[1])
].sort_values('nombre_planeta').reset_index(drop=True)

st.markdown("<br>", unsafe_allow_html=True)

# MÉTRICAS REACTIVAS
c1, c2, c3, c4 = st.columns(4)
estilo_num = "font-size:2em;font-family:Orbitron,monospace;color:#00d4ff;line-height:1.2"
estilo_box = "class='metric-box' style='min-height:110px;display:flex;flex-direction:column;justify-content:center'"

with c1:
    st.markdown(f"<div {estilo_box}><div style='{estilo_num}'>{len(df_filtrado):,}</div><p>PLANETAS</p></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div {estilo_box}><div style='{estilo_num}'>{len(df_filtrado[df_filtrado['tipo_planeta']=='Habitable'])}</div><p>HABITABLES</p></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div {estilo_box}><div style='{estilo_num}'>{df_filtrado['metodo_descubrimiento'].nunique()}</div><p>MÉTODOS</p></div>", unsafe_allow_html=True)
with c4:
    if len(df_filtrado) > 0:
        año_desde = int(df_filtrado['año_descubrimiento'].min())
        año_hasta = int(df_filtrado['año_descubrimiento'].max())
        st.markdown(f"<div {estilo_box}><div style='font-size:1.5em;font-family:Orbitron,monospace;color:#00d4ff;line-height:1.2'>{año_desde}–{año_hasta}</div><p>AÑO DESC.</p></div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div {estilo_box}><div style='{estilo_num}'>—</div><p>AÑO DESC.</p></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# PESTAÑAS
tab1, tab2, tab3 = st.tabs(["🔭  EXPLORADOR", "📊  VISUALIZACIONES", "🤖  AGENTE IA"])

with tab1:
    st.markdown("<br>", unsafe_allow_html=True)

    if len(df_filtrado) == 0:
        st.warning("No hay planetas con los filtros seleccionados.")
    else:
        opciones = ["— Selecciona un planeta —"] + df_filtrado['nombre_planeta'].tolist()
        key_dinamico = f"exp_{tipo_sel}_{metodo_sel}_{rango_años[0]}_{rango_años[1]}"
        planeta_sel = st.selectbox("Selecciona un planeta", options=opciones, index=0, key=key_dinamico)

        if planeta_sel == "— Selecciona un planeta —":
            st.markdown("""
            <div class='planet-card' style='text-align:center; padding:40px'>
                <p style='color:rgba(0,212,255,0.4); font-size:1.2em'>Selecciona un planeta de la lista para ver sus datos</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            idx = opciones.index(planeta_sel) - 1
            datos = df_filtrado.iloc[idx]
            badge = "<span class='habitable-badge'>🌍 ZONA HABITABLE</span>" if datos['tipo_planeta'] == 'Habitable' else ""

            st.markdown(f"""
            <div class='planet-card'>
                <h2 style='margin-bottom:4px'>{datos['nombre_planeta']} {badge}</h2>
                <p style='color:rgba(0,212,255,0.6); margin-bottom:0'>
                    Estrella: {datos['estrella']} · {datos['metodo_descubrimiento']} · {int(datos['año_descubrimiento']) if pd.notna(datos['año_descubrimiento']) else 'N/A'}
                </p>
            </div>
            """, unsafe_allow_html=True)

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                v = f"{datos['radio_terrestre']} R⊕" if pd.notna(datos['radio_terrestre']) else "Sin datos"
                st.markdown(f"<div class='metric-box'><h2>{v}</h2><p>RADIO</p></div>", unsafe_allow_html=True)
            with m2:
                v = f"{datos['masa_terrestre']} M⊕" if pd.notna(datos['masa_terrestre']) else "Sin datos"
                st.markdown(f"<div class='metric-box'><h2>{v}</h2><p>MASA</p></div>", unsafe_allow_html=True)
            with m3:
                v = f"{round(datos['periodo_orbital_dias'],1)} días" if pd.notna(datos['periodo_orbital_dias']) else "Sin datos"
                st.markdown(f"<div class='metric-box'><h2>{v}</h2><p>PERÍODO ORBITAL</p></div>", unsafe_allow_html=True)
            with m4:
                v = f"{datos['temperatura_k']} K" if pd.notna(datos['temperatura_k']) else "Sin datos"
                st.markdown(f"<div class='metric-box'><h2>{v}</h2><p>TEMPERATURA</p></div>", unsafe_allow_html=True)

            st.markdown(f"""
            <div class='planet-card' style='margin-top:16px'>
                <p><b style='color:#00d4ff'>Tipo:</b> {datos['tipo_planeta']}</p>
                <p style='margin:0'><b style='color:#00d4ff'>Temperatura estrella:</b> {datos['temperatura_estrella_k']} K</p>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.markdown("<br>", unsafe_allow_html=True)

    if len(df_filtrado) == 0:
        st.warning("No hay planetas con los filtros seleccionados.")
    else:
        col_a, col_b = st.columns(2)
        with col_a:
            conteo = df_filtrado['tipo_planeta'].value_counts().reset_index()
            conteo.columns = ['tipo', 'cantidad']
            fig1 = px.bar(conteo, x='tipo', y='cantidad', color='tipo',
                color_discrete_map=COLORES, title='Distribución por tipo de planeta',
                template='plotly_dark')
            fig1.update_layout(**LAYOUT_BASE, showlegend=False)
            st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})

        with col_b:
            m_count = df_filtrado['metodo_descubrimiento'].value_counts().reset_index()
            m_count.columns = ['metodo', 'cantidad']
            fig2 = px.pie(m_count, values='cantidad', names='metodo',
                title='Métodos de descubrimiento', template='plotly_dark', hole=0.4)
            fig2.update_layout(**LAYOUT_BASE)
            fig2.update_traces(textfont_color='#ffffff')
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})

        por_año = df_filtrado.groupby('año_descubrimiento').size().reset_index()
        por_año.columns = ['año', 'cantidad']
        fig3 = px.area(por_año, x='año', y='cantidad', title='Descubrimientos por año',
            template='plotly_dark', color_discrete_sequence=['#00d4ff'],
            markers=True)
        fig3.update_layout(**LAYOUT_BASE)
        fig3.update_traces(fill='tozeroy', fillcolor='rgba(0,212,255,0.1)')
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})

        df_sc = df_filtrado.dropna(subset=['radio_terrestre', 'temperatura_k'])
        if len(df_sc) > 0:
            fig4 = px.scatter(df_sc, x='temperatura_k', y='radio_terrestre',
                color='tipo_planeta', color_discrete_map=COLORES,
                hover_name='nombre_planeta',
                title='Mapa de habitabilidad — Temperatura vs Radio',
                template='plotly_dark',
                labels={'temperatura_k': 'Temperatura (K)', 'radio_terrestre': 'Radio (R⊕)'})
            fig4.add_vrect(x0=200, x1=320, fillcolor='rgba(0,255,135,0.08)',
                layer='below', line_width=0,
                annotation_text="Zona habitable", annotation_font_color='#00ff87')
            fig4.update_layout(**LAYOUT_BASE)
            st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False, 'staticPlot': True})

with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class='planet-card'>
        <p style='color:rgba(0,212,255,0.9); margin-bottom:12px; font-size:1.1em'><b>Pregúntame cualquier cosa sobre los exoplanetas:</b></p>
        <p style='color:rgba(255,255,255,0.7)'>• ¿Cuáles son los planetas en zona habitable?</p>
        <p style='color:rgba(255,255,255,0.7)'>• ¿Qué planeta tiene la temperatura más similar a la Tierra?</p>
        <p style='color:rgba(255,255,255,0.7)'>• ¿Cuántos planetas rocosos se descubrieron después del 2020?</p>
        <p style='color:rgba(255,255,255,0.7)'>• Analiza el exoplaneta Kepler-1649 c</p>
    </div>
    """, unsafe_allow_html=True)

    if 'historial' not in st.session_state:
        st.session_state.historial = []

    for msg in st.session_state.historial:
        if msg['rol'] == 'usuario':
            st.markdown(f"<div class='chat-user'><b style='color:#00d4ff'>TÚ:</b> <span style='color:#ffffff'>{msg['texto']}</span></div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-agent'><b style='color:#9d6fff'>🤖 AGENTE:</b><br><span style='color:#ffffff'>{msg['texto']}</span></div>", unsafe_allow_html=True)

    pregunta = st.text_input("", placeholder="Escribe tu pregunta aquí...", key="pregunta_ia")

    col_e, col_l = st.columns([1, 5])
    with col_e:
        enviar = st.button("ENVIAR →")
    with col_l:
        if st.button("LIMPIAR"):
            st.session_state.historial = []
            st.rerun()

    if enviar and pregunta:
        filtros_activos = []
        if tipo_sel != "— Todos los tipos —":
            filtros_activos.append(f"tipo: {tipo_sel}")
        if metodo_sel != "— Todos los métodos —":
            filtros_activos.append(f"método: {metodo_sel}")
        if rango_años != (año_min, año_max):
            filtros_activos.append(f"años: {rango_años[0]}–{rango_años[1]}")

        filtros_texto = ", ".join(filtros_activos) if filtros_activos else "ninguno (mostrando todos los planetas)"

        hab = df_filtrado[df_filtrado['tipo_planeta'] == 'Habitable'][
            ['nombre_planeta', 'radio_terrestre', 'temperatura_k', 'estrella']
        ].to_string(index=False)

        resumen = f"""
Dataset filtrado: {len(df_filtrado)} planetas
Filtros activos: {filtros_texto}
- Habitables: {len(df_filtrado[df_filtrado['tipo_planeta']=='Habitable'])}
- Rocosos: {len(df_filtrado[df_filtrado['tipo_planeta']=='Rocoso'])}
- Super-Tierras: {len(df_filtrado[df_filtrado['tipo_planeta']=='Super-Tierra'])}
- Gigantes gaseosos: {len(df_filtrado[df_filtrado['tipo_planeta']=='Gigante gaseoso'])}
- Temperatura promedio: {round(df_filtrado['temperatura_k'].mean(), 1)} K
- Radio promedio: {round(df_filtrado['radio_terrestre'].mean(), 2)} R⊕

Planetas habitables en el filtro actual:
{hab}

IMPORTANTE: Si el usuario pregunta por planetas fuera del filtro actual, indícale que tiene filtros activos y que debe cambiarlos para ver esos planetas.
"""
        prompt = f"""Eres un astrónomo experto con acceso a la base de datos NASA de exoplanetas.

Contexto:
{resumen}

Pregunta: {pregunta}

Responde en español de forma clara y precisa."""

        st.session_state.historial.append({'rol': 'usuario', 'texto': pregunta})

        with st.spinner("Analizando..."):
            try:
                client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                resp = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "user", "content": prompt}]
                )
                texto = resp.choices[0].message.content
            except Exception as e:
                texto = f"Error: {str(e)}"

        st.session_state.historial.append({'rol': 'agente', 'texto': texto})
        st.rerun()