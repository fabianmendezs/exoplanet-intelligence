# 🪐 Exoplanet Intelligence

Plataforma de análisis de exoplanetas con datos reales de NASA, estadística avanzada e inteligencia artificial integrada.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://exoplanet-intelligence.streamlit.app)

## Demo

🔗 **App en vivo:** https://exoplanet-intelligence.streamlit.app

## ¿Qué hace este proyecto?

Descarga y analiza 6,000+ exoplanetas reales de la NASA Exoplanet Archive, identifica candidatos en zona habitable, y usa un agente de IA para generar reportes científicos en lenguaje natural sobre cualquier planeta.

## Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Lenguaje | Python 3.11 |
| Datos | NASA Exoplanet Archive TAP API |
| Análisis | Pandas, NumPy, SciPy |
| Base de datos | DuckDB |
| Transformaciones | dbt |
| Visualizaciones | Plotly |
| Agente IA | Groq API + Llama 3.3 |
| App web | Streamlit |
| Control de versiones | Git + GitHub |

## Estructura del proyecto
exoplanet-intelligence/
├── src/
│   ├── download_exoplanets.py    # Descarga datos desde NASA API
│   └── agente_exoplanetas.py     # Agente IA por terminal
├── notebooks/
│   └── exploracion.ipynb         # Análisis estadístico exploratorio
├── dashboard/
│   └── app.py                    # App web Streamlit
├── exoplanet_dbt/
│   └── models/                   # Transformaciones SQL con dbt
└── README.md

## Instalación local

```bash
# Clonar repositorio
git clone https://github.com/fabianmendezs/exoplanet-intelligence.git
cd exoplanet-intelligence

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Agregar NASA_API_KEY y GROQ_API_KEY en .env

# Descargar datos
python src/download_exoplanets.py

# Ejecutar app
streamlit run dashboard/app.py
```

## Análisis incluidos

- Distribución de radios y masas planetarias
- Métodos de descubrimiento (Transit, Radial Velocity, etc.)
- Evolución temporal de descubrimientos (1992–2026)
- Correlación Pearson vs Spearman entre masa y radio
- Identificación de planetas en zona habitable
- Ranking de planetas por tipo con window functions SQL

## Autor

**Fabián Méndez** — Analista de datos  
[LinkedIn](https://linkedin.com/in/fabianmendezs) · [GitHub](https://github.com/fabianmendezs)

## Recursos

- [NASA Exoplanet Archive — Columnas disponibles](https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html)
- [API TAP](https://exoplanetarchive.ipac.caltech.edu/TAP/sync)
