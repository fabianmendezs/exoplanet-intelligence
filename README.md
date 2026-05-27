# 🪐 Exoplanet Intelligence

Plataforma de análisis de exoplanetas con datos reales de NASA, estadística avanzada e inteligencia artificial integrada.

## Demo

🔗 **App en vivo:** https://exoplanet.frmendez.com

## ¿Qué hace este proyecto?

Descarga y analiza 6,000+ exoplanetas reales de la NASA Exoplanet Archive, identifica candidatos en zona habitable, y usa un agente de IA para generar reportes científicos en lenguaje natural sobre cualquier planeta.

## Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Lenguaje | Python 3.11 |
| Datos | NASA Exoplanet Archive TAP API |
| Análisis | Pandas, NumPy, SciPy, scikit-learn |
| Base de datos | DuckDB |
| Transformaciones | dbt |
| Visualizaciones | Plotly |
| Agente IA | Groq API + Llama 3.3 70B |
| App web | Streamlit |
| Control de versiones | Git + GitHub |

## Estructura del proyecto

```
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
├── .env.example                  # Plantilla de variables de entorno
└── README.md
```

## Instalación local

```bash
# Clonar repositorio
git clone https://github.com/fabianmendezs/exoplanet-intelligence.git
cd exoplanet-intelligence

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux / Mac

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env y agregar la GROQ_API_KEY (obtener en console.groq.com)

# Descargar datos
python src/download_exoplanets.py

# Ejecutar app
streamlit run dashboard/app.py
```

## Variables de entorno requeridas

| Variable | Descripción | Cómo obtenerla |
|---|---|---|
| `GROQ_API_KEY` | API key de Groq para el agente IA | [console.groq.com](https://console.groq.com) → API Keys |
| `NASA_API_KEY` | API key de NASA (opcional) | La TAP API es pública y no requiere key |

> **Nunca commitear el archivo `.env`.** Está incluido en `.gitignore`.

## Análisis incluidos

- Distribución de radios y masas planetarias
- Métodos de descubrimiento (Transit, Radial Velocity, etc.)
- Evolución temporal de descubrimientos (1992–2026)
- Predicción de temperatura por regresión logarítmica (R²=0.982)
- Clustering K-means — 5 grupos naturales de exoplanetas
- Identificación de planetas en zona habitable (200–320 K, radio ≤ 1.5 R⊕)
- Ranking de planetas por tipo con window functions SQL (dbt)
- Agente IA conversacional con contexto de los datos filtrados

## Despliegue en servidor (DigitalOcean)

El proyecto corre como servicio systemd en el servidor personal.

**Servicio:** `exoplanet.service`  
**Puerto:** 8501  
**URL:** https://exoplanet.frmendez.com  
**Ruta en servidor:** `/var/www/exoplanet-intelligence/`

### Actualizar el servidor tras un push

```bash
# En el servidor (SSH: ssh root@143.244.153.241)
cd /var/www/exoplanet-intelligence
git pull
systemctl restart exoplanet
```

### Ver logs del servicio

```bash
journalctl -u exoplanet -f        # Logs en tiempo real
journalctl -u exoplanet --since today  # Logs del día
```

### Verificar seguridad del servidor

```bash
# .env no debe ser accesible públicamente (debe devolver 404)
curl https://exoplanet.frmendez.com/.env
```

## Seguridad

Este proyecto sigue las prácticas definidas en la [guía de seguridad del stack](../README.md):

- ✅ Credenciales en `.env` (nunca en el código)
- ✅ `.env` en `.gitignore` — nunca se commitea
- ✅ `.env.example` con valores de placeholder para nuevos clones
- ✅ API keys cargadas con `os.getenv()` + `load_dotenv()`
- ✅ Requests HTTP con `timeout=60` para evitar bloqueos del servidor
- ✅ Nginx bloquea acceso a `.env` vía HTTP

> **Nota:** Si el agente IA muestra `Error: 401 Invalid API Key`, la `GROQ_API_KEY` en el servidor
> está vencida o inválida. Generar una nueva en [console.groq.com](https://console.groq.com)
> y actualizar `/var/www/exoplanet-intelligence/.env` en el servidor.

## Autor

**Fabián Méndez** — Analista de datos  
[LinkedIn](https://linkedin.com/in/fabianmendezs) · [GitHub](https://github.com/fabianmendezs)

## Recursos

- [NASA Exoplanet Archive — Columnas disponibles](https://exoplanetarchive.ipac.caltech.edu/docs/API_PS_columns.html)
- [API TAP](https://exoplanetarchive.ipac.caltech.edu/TAP/sync)
- [Groq Console](https://console.groq.com)
