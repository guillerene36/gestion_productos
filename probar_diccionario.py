import json
import urllib.request
import urllib.error
import base64
import os

# --- DATOS DEL REPORTE ---
mi_diccionario = {
    "cliente": "Cliente Final (Localhost)",
    "fecha": "2026-06-20",
    "items": [
        {"nombre": "Prueba Final localhost", "cantidad": 1, "precio": 5000, "total": 5000}
    ],
    "total_final": 5000
}

# --- CONFIGURACIÓN DE CONEXIÓN ---
# 1. Usamos 'localhost' como pediste
HOST = "localhost"
PORT = "8070"
DB = "mi_practica"
ROUTE = "/mi_reporte"

# Construimos la URL
URL = f"http://{HOST}:{PORT}{ROUTE}?db={DB}"

# Evitamos problemas de Proxy
os.environ['NO_PROXY'] = 'localhost,127.0.0.1'

print(f"📡 Conectando a: {URL}")

try:
    # Preparamos el paquete JSON
    json_bytes = json.dumps(mi_diccionario).encode('utf-8')
    req = urllib.request.Request(URL, data=json_bytes, headers={'Content-Type': 'application/json'})
    
    # Enviamos la petición
    with urllib.request.urlopen(req) as response:
        datos = response.read().decode()
        
        # Analizamos la respuesta
        try:
            respuesta = json.loads(datos)
        except json.JSONDecodeError:
            print(f"⚠️ Recibí respuesta, pero no es JSON: {datos[:100]}...")
            exit()

        if 'result' in respuesta:
            nombre_archivo = "reporte_final_localhost.pdf"
            with open(nombre_archivo, "wb") as f:
                f.write(base64.b64decode(respuesta['result']['pdf_base64']))
            print(f"\n✅ ¡ÉXITO TOTAL! PDF generado correctamente.")
            print(f"📂 Archivo guardado: {nombre_archivo}")
        elif 'error' in respuesta:
            print(f"❌ Odoo respondió con error: {respuesta['error']}")
        else:
            print(f"⚠️ Respuesta extraña: {respuesta}")

except urllib.error.HTTPError as e:
    print(f"\n❌ Error HTTP {e.code}: {e.reason}")
    if e.code == 404:
        print("   -> Odoo no encuentra la ruta. Posibles causas:")
        print("      1. La base de datos 'mi_practica' no es la correcta.")
        print("      2. El módulo FINAL8 no terminó de cargar (revisa los logs).")
except urllib.error.URLError as e:
    print(f"\n❌ No se pudo conectar a {HOST}:{PORT}")
    print(f"   -> Razón: {e.reason}")
    print("   -> Verifica que Docker esté corriendo.")
