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

print("--- INICIANDO LIMPIEZA TOTAL ---")
uid = json_rpc("common", "login", [DB, USER, PASS])

def execute(model, method, args_list):
    return json_rpc("object", "execute_kw", [DB, uid, PASS, model, method, args_list])

# 1. Borrar PARTES primero (para evitar errores de integridad)
print("1. Buscando todas las Partes...")
ids_partes = execute('gestion.partes', 'search', [[]]) # [] vacío trae todo
if ids_partes:
    print(f"   -> Borrando {len(ids_partes)} partes...")
    execute('gestion.partes', 'unlink', [ids_partes])
else:
    print("   -> No hay partes para borrar.")

# 2. Borrar PRODUCTOS
print("2. Buscando todos los Productos...")
ids_productos = execute('gestion.productos', 'search', [[]])
if ids_productos:
    print(f"   -> Borrando {len(ids_productos)} productos...")
    execute('gestion.productos', 'unlink', [ids_productos])
else:
    print("   -> No hay productos para borrar.")

print("--- ¡SISTEMA LIMPIO! ---")
