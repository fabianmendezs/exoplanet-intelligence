import duckdb
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def buscar_planeta(nombre):
    conn = duckdb.connect("data/exoplanets.db")
    resultado = conn.execute("""
        SELECT * FROM main.stg_exoplanets
        WHERE LOWER(nombre_planeta) = LOWER(?)
    """, [nombre]).fetchone()
    conn.close()
    return resultado

def generar_reporte(datos_planeta):
    nombre, estrella, masa, radio, periodo, temp_k, temp_estrella, metodo, año, tipo = datos_planeta

    prompt = f"""
Eres un astrónomo experto. Analiza estos datos reales de un exoplaneta de la base de datos NASA 
y genera un reporte científico breve en español.

Datos del planeta:
- Nombre: {nombre}
- Estrella anfitriona: {estrella}
- Tipo clasificado: {tipo}
- Masa: {masa} masas terrestres
- Radio: {radio} radios terrestres
- Período orbital: {periodo} días
- Temperatura de equilibrio: {temp_k} K
- Temperatura de la estrella: {temp_estrella} K
- Método de descubrimiento: {metodo}
- Año de descubrimiento: {año}

Incluye en tu análisis:
1. Características físicas del planeta
2. Comparación con la Tierra
3. Posibilidad de habitabilidad
4. Datos interesantes sobre su estrella y órbita
"""

    respuesta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return respuesta.choices[0].message.content

def main():
    print("=== Agente de Análisis de Exoplanetas ===\n")
    nombre = input("Ingresa el nombre del planeta: ")
    
    datos = buscar_planeta(nombre)
    
    if datos:
        print(f"\nPlaneta encontrado: {datos[0]}\n")
        print("Generando reporte con IA...\n")
        reporte = generar_reporte(datos)
        print(reporte)
    else:
        print(f"Planeta '{nombre}' no encontrado en la base de datos.")

if __name__ == "__main__":
    main()