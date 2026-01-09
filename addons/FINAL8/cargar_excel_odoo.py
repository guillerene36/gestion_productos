import pandas as pd
import json
import urllib.request
import random

# --- CONFIGURACIÓN ODOO ---
HOST = 'localhost'
PORT = 8070
DB = 'mi_practica'
USER = 'admin'
PASS = 'admin'
URL = f"http://{HOST}:{PORT}/jsonrpc"

# --- CONEXIÓN JSON-RPC ---
def json_rpc(service, method, args):
    payload = {
        "jsonrpc": "2.0", "method": "call",
        "params": {"service": service, "method": method, "args": args},
        "id": random.randint(0, 1000000000),
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

# --- INICIO DE SESIÓN ---
print("1. Conectando a Odoo...")
uid = json_rpc("common", "login", [DB, USER, PASS])
if not uid: exit()
print(f"   Login OK. UID: {uid}")

def execute(model, method, args_list):
    return json_rpc("object", "execute_kw", [DB, uid, PASS, model, method, args_list])

# --- HELPER: BUSCAR IDs DE UNIDADES DE NEGOCIO ---
# Cacheamos las unidades para no buscarlas 50 veces
print("2. Cacheando Unidades de Negocio...")
unidades_map = {}
todas_unidades = execute('gestion.unidad.negocio', 'search_read', [[], ['name', 'id']])
for u in todas_unidades:
    unidades_map[u['name']] = u['id']
print(f"   Unidades encontradas: {unidades_map}")

# --- LECTURA DEL EXCEL ---
print("3. Leyendo Excel con Pandas...")
try:
    df_prod = pd.read_excel('datos_prueba.xlsx', sheet_name='Productos')
    df_part = pd.read_excel('datos_prueba.xlsx', sheet_name='Partes')
except Exception as e:
    print("Error leyendo el archivo. ¿Ejecutaste el script generador primero?")
    exit()

# --- PROCESO DE CARGA ---
print(f"4. Iniciando carga de {len(df_prod)} productos y sus partes...")

for index, row in df_prod.iterrows():
    # A. Preparar Unidades de Negocio (Many2many)
    # El Excel trae "Jumbo,Easy", necesitamos convertirlo a IDs [4, ID_JUMBO], [4, ID_EASY]
    unidad_names = str(row['unidades']).split(',')
    unidad_ids = []
    for nombre in unidad_names:
        nombre = nombre.strip()
        if nombre in unidades_map:
            # Sintaxis Odoo Many2many: (4, id) vincula un registro existente
            unidad_ids.append((4, unidades_map[nombre]))
    
    # B. Crear el Producto
    vals_producto = {
        'name': row['nombre'],
        'codigo': row['codigo'],
        'tipo': row['tipo'],
        'origen': row['origen'],
        'cantidad_vendida': row['cantidad_vendida'],
        'unidad_negocio_ids': unidad_ids
    }
    
    try:
        # Intentamos crear el producto
        prod_id = execute('gestion.productos', 'create', [vals_producto])
        print(f"   [OK] Producto creado: {row['nombre']} (ID: {prod_id})")
        
        # C. Crear las Partes Asociadas
        # Filtramos del dataframe de partes aquellas que coincidan con este código
        partes_del_producto = df_part[df_part['ref_producto'] == row['codigo']]
        
        for _, part_row in partes_del_producto.iterrows():
            vals_parte = {
                'name': part_row['nombre_parte'],
                'producto_id': prod_id # Aquí hacemos la magia del enlace
            }
            execute('gestion.partes', 'create', [vals_parte])
            # print(f"       -> Parte creada: {part_row['nombre_parte']}")
            
    except Exception as e:
        print(f"   [ERROR] Falló al crear {row['nombre']}: {e}")

print("\n--- PROCESO TERMINADO ---")
