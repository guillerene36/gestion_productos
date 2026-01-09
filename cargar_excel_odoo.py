import pandas as pd
import json
import urllib.request
import random

# --- CONFIGURACIÓN ---
HOST = 'localhost'
PORT = 8070
DB = 'mi_practica'
USER = 'admin'
PASS = 'admin'
URL = f"http://{HOST}:{PORT}/jsonrpc"

def json_rpc(service, method, args):
    payload = {
        "jsonrpc": "2.0", "method": "call",
        "params": {"service": service, "method": method, "args": args},
        "id": random.randint(0, 1000000),
    }
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        if 'error' in result: raise Exception(result['error']['data']['message'])
        return result['result']
    except Exception as e:
        print(f"Error RPC: {e}")
        return None

# --- LOGIN ---
print("1. Conectando...")
uid = json_rpc("common", "login", [DB, USER, PASS])
if not uid: 
    print("Error de login.")
    exit()

def execute(model, method, args_list):
    return json_rpc("object", "execute_kw", [DB, uid, PASS, model, method, args_list])

# --- CACHE DE UNIDADES ---
print("2. Leyendo Unidades...")
unidades_map = {u['name']: u['id'] for u in execute('gestion.unidad.negocio', 'search_read', [[], ['name', 'id']])}

# --- LECTURA EXCEL ---
print("3. Leyendo Excel...")
try:
    # Leemos forzando tipo String (dtype=str) para que el cruce sea exacto
    df_prod = pd.read_excel('datos_prueba.xlsx', sheet_name='Productos', dtype={'codigo': str})
    df_part = pd.read_excel('datos_prueba.xlsx', sheet_name='Partes', dtype={'ref_producto': str})
except Exception as e:
    print(f"Error leyendo Excel: {e}")
    exit()

print(f"4. Cargando {len(df_prod)} productos...")

for index, row in df_prod.iterrows():
    # A. Unidades
    unidad_ids = []
    if pd.notna(row['unidades']):
        for nombre in str(row['unidades']).split(','):
            nombre = nombre.strip()
            if nombre in unidades_map:
                unidad_ids.append((4, unidades_map[nombre]))

    # B. Producto
    vals_prod = {
        'name': row['nombre'],
        'codigo': row['codigo'],
        'tipo': row['tipo'],
        'origen': row['origen'],
        'cantidad_vendida': int(row['cantidad_vendida']),
        'unidad_negocio_ids': unidad_ids
    }

    try:
        prod_id = execute('gestion.productos', 'create', [vals_prod])
        print(f"   [PROD] Creado ID {prod_id}: {row['nombre']}")

        # C. PARTES (Aquí estaba el problema, ahora lo hacemos explícito)
        # Filtramos las partes que tienen el MISMO código de referencia
        mis_partes = df_part[df_part['ref_producto'] == row['codigo']]
        
        cantidad_partes = len(mis_partes)
        if cantidad_partes > 0:
            print(f"       -> Encontradas {cantidad_partes} partes. Cargando...")
            for _, p_row in mis_partes.iterrows():
                vals_parte = {
                    'name': p_row['nombre_parte'],
                    'producto_id': prod_id  # Vinculamos al padre recién creado
                }
                execute('gestion.partes', 'create', [vals_parte])
        else:
            print("       -> [ALERTA] Este producto no tiene partes en el Excel.")

    except Exception as e:
        print(f"   [ERROR] Falló {row['nombre']}: {e}")

print("\n--- FIN DEL PROCESO ---")
