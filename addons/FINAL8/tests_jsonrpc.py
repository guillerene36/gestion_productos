import json
import urllib.request
import random

# --- 1. CONFIGURACIÓN ---
HOST = 'localhost'
PORT = 8070
DB = 'mi_practica'
USER = 'admin'
PASS = 'admin'
URL = f"http://{HOST}:{PORT}/jsonrpc"

def json_rpc(service, method, args):
    """Función de conexión base"""
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": service,
            "method": method,
            "args": args,
        },
        "id": random.randint(0, 1000000000),
    }
    req = urllib.request.Request(URL, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        if 'error' in result: 
            print(f"\n!!! ERROR ODOO: {result['error']['data']['message']}")
            raise Exception("Fallo en la llamada RPC")
        return result['result']
    except Exception as e:
        print(f"Error de conexión o datos: {e}")
        return None

# --- LOGIN ---
print("--- INICIANDO SIMULACIÓN EXTERNA (V3 - Anti Duplicados) ---")
uid = json_rpc("common", "login", [DB, USER, PASS])
print(f"Login exitoso. Usuario ID: {uid}\n")

def execute(model, method, args_list):
    return json_rpc("object", "execute_kw", [DB, uid, PASS, model, method, args_list])

# ==========================================
# 1. CREATE (Crear)
# ==========================================
# Generamos un código aleatorio para que NO falle si ejecutas el script 2 veces
codigo_random = f"GAMER-{random.randint(100, 9999)}"

print(f"1. [C]REATE: Creando 'Silla Gamer RGB' con código {codigo_random}...")

vals = {
    'name': 'Silla Gamer RGB',
    'codigo': codigo_random,  # <--- AQUÍ ESTÁ EL TRUCO
    'tipo': 'bien',
    'cantidad_vendida': 0
}

product_id = execute('gestion.productos', 'create', [vals]) 

if product_id:
    print(f"   -> Éxito. Producto creado con ID: {product_id}")

    # ==========================================
    # 2. READ (Leer)
    # ==========================================
    print(f"\n2. [R]EAD: Leyendo datos del ID {product_id}...")
    domain = [('id', '=', product_id)]
    fields = ['name', 'codigo', 'cantidad_vendida']
    datos = execute('gestion.productos', 'search_read', [domain, fields])
    if datos:
        print(f"   -> Odoo devolvió: {datos}")

    # ==========================================
    # 3. UPDATE (Actualizar)
    # ==========================================
    print(f"\n3. [U]PDATE: Actualizando precio y nombre...")
    nuevos_valores = {
        'name': 'Silla Gamer RGB (V2 Pro)',
        'cantidad_vendida': 500
    }
    execute('gestion.productos', 'write', [[product_id], nuevos_valores])
    
    # Verificamos
    check = execute('gestion.productos', 'search_read', [domain, ['name', 'cantidad_vendida']])
    if check:
        print(f"   -> Dato actualizado: {check[0]['name']} - Ventas: {check[0]['cantidad_vendida']}")

    # ==========================================
    # 4. DELETE (Borrar)
    # ==========================================
    print(f"\n4. [D]ELETE: Eliminando el producto...")
    execute('gestion.productos', 'unlink', [[product_id]])
    
    # Verificamos
    check_deleted = execute('gestion.productos', 'search', [domain])
    if not check_deleted:
        print("   -> Éxito. El producto ya no existe en la base de datos.")
    else:
        print("   -> Error. El producto sigue ahí.")

else:
    print("!!! El proceso se detuvo porque falló la creación.")

print("\n--- CICLO CRUD FINALIZADO ---")
