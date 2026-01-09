import pandas as pd
import json
import urllib.request
import random

# CONFIGURACIÓN
HOST, PORT, DB, USER, PASS = 'localhost', 8070, 'mi_practica', 'admin', 'admin'
URL = f"http://{HOST}:{PORT}/jsonrpc"

def json_rpc(service, method, args):
    payload = {"jsonrpc": "2.0", "method": "call", "params": {"service": service, "method": method, "args": args}, "id": random.randint(0, 1000000)}
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        if 'error' in result: raise Exception(result['error']['data']['message'])
        return result['result']
    except Exception as e:
        print(f"Error RPC: {e}")
        return None

print("Conectando...")
uid = json_rpc("common", "login", [DB, USER, PASS])
def execute(model, method, args_list): return json_rpc("object", "execute_kw", [DB, uid, PASS, model, method, args_list])

# MAPA UNIDADES
unidades_map = {u['name']: u['id'] for u in execute('gestion.unidad.negocio', 'search_read', [[], ['name', 'id']])}

print("Cargando 'productos_reales.xlsx'...")
# Leemos el EXCEL NUEVO
df_prod = pd.read_excel('productos_reales.xlsx', sheet_name='Productos', dtype={'codigo': str})
df_part = pd.read_excel('productos_reales.xlsx', sheet_name='Partes', dtype={'ref_producto': str})

for index, row in df_prod.iterrows():
    unidad_ids = []
    if pd.notna(row['unidades']):
        for nombre in str(row['unidades']).split(','):
            nombre = nombre.strip()
            if nombre in unidades_map:
                unidad_ids.append((4, unidades_map[nombre]))

    vals = {
        'name': row['nombre'],
        'codigo': row['codigo'],
        'tipo': row['tipo'],
        'origen': row['origen'],
        'cantidad_vendida': int(row['cantidad_vendida']),
        'unidad_negocio_ids': unidad_ids
    }

    try:
        prod_id = execute('gestion.productos', 'create', [vals])
        print(f"✅ {row['nombre']} (Jumbo/Easy/Paris)")

        mis_partes = df_part[df_part['ref_producto'] == row['codigo']]
        for _, p in mis_partes.iterrows():
            execute('gestion.partes', 'create', [{'name': p['nombre_parte'], 'producto_id': prod_id}])
            
    except Exception as e:
        print(f"❌ Error en {row['nombre']}: {e}")

print("--- CARGA REAL FINALIZADA ---")
