import json
import urllib.request
import random

# --- CONFIGURACIÓN ---
HOST = 'localhost'
PORT = 8070          # El puerto que usas en tu Docker (vi que era 8070 en tus logs)
DB = 'mi_practica'   # Tu base de datos
USER = 'admin'       # Usamos admin para no tener problemas de permisos
PASS = 'admin'       # La contraseña de tu admin (cámbiala si es distinta)
URL = f"http://{HOST}:{PORT}/jsonrpc"

def json_rpc(service, method, args):
    """Función para enviar paquetes JSON a Odoo"""
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
    
    req = urllib.request.Request(
        URL, 
        data=json.dumps(payload).encode(), 
        headers={"Content-Type": "application/json"}
    )
    
    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        if 'error' in result:
            raise Exception(result['error'])
        return result['result']
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

# --- PASO 1: AUTENTICACIÓN (LOGIN) ---
print("1. Conectando a Odoo...")
uid = json_rpc("common", "login", [DB, USER, PASS])

if not uid:
    print("ERROR: No se pudo iniciar sesión. Revisa usuario/contraseña/puerto.")
    exit()
else:
    print(f"   -> Login exitoso! Tu User ID es: {uid}")

# --- PASO 2: CREAR UNA UNIDAD DE NEGOCIO ---
print("\n2. Creando Unidad de Negocio 'Tottus'...")
nueva_unidad_id = json_rpc("object", "execute_kw", [
    DB, uid, PASS,
    'gestion.unidad.negocio',  # Modelo
    'create',                  # Método
    [{                         # Valores
        'name': 'Tottus',
        'descripcion': 'Hipermercado Externo (Cargado por Script)'
    }]
])
print(f"   -> Unidad creada con ID: {nueva_unidad_id}")

# --- PASO 3: CREAR UN PRODUCTO ASOCIADO ---
print("\n3. Creando Producto 'Tablet Samsung'...")
nuevo_producto_id = json_rpc("object", "execute_kw", [
    DB, uid, PASS,
    'gestion.productos',       # Modelo
    'create',                  # Método
    [{                         # Valores
        'name': 'Tablet Samsung S9',
        'codigo': 'TAB-SAM-001',
        'tipo': 'bien',
        'origen': 'imp',
        'cantidad_vendida': 10,
        # Aquí la magia: Asignamos la unidad que acabamos de crear (Many2many usa código 4)
        'unidad_negocio_ids': [[4, nueva_unidad_id]], 
    }]
])
print(f"   -> Producto creado con ID: {nuevo_producto_id}")

print("\n--- ¡CARGA COMPLETADA CON ÉXITO! ---")
