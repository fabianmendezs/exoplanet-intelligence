import requests
import pandas as pd
from dotenv import load_dotenv
import os
import duckdb

load_dotenv()

url = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"

params = {
    "query": "SELECT pl_name,hostname,pl_masse,pl_rade,pl_orbper,pl_eqt,st_teff,discoverymethod,disc_year,pl_insol,sy_dist,sy_pnum,st_rad,st_mass FROM ps WHERE default_flag=1",
    "format": "json"
}

print("Descargando exoplanetas desde NASA...")
response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/exoplanets.csv", index=False)
    print(f"Descargados {len(df)} exoplanetas")
    print(df.head())

    conn = duckdb.connect("data/exoplanets.db")
    conn.execute("DROP TABLE IF EXISTS exoplanets")
    conn.execute("CREATE TABLE exoplanets AS SELECT * FROM df")
    result = conn.execute("SELECT COUNT(*) FROM exoplanets").fetchone()
    print(f"Exoplanetas en DuckDB: {result[0]}")
    conn.close()
else:
    print(f"Error {response.status_code}: {response.text}")