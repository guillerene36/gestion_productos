import pandas as pd
import random

# --- CONFIGURACIÓN ---
CANTIDAD = 20  # Hacemos 20 para que sea rápido de revisar
UNIDADES = ['Jumbo', 'Easy', 'Santa Isabel', 'Paris'] 

data_productos = []
data_partes = []

print(f"Generando {CANTIDAD} productos con sus partes...")

for i in range(1, CANTIDAD + 1):
    codigo = f"PROD-TEST-{i:03d}"  # Ej: PROD-TEST-001
    nombre_prod = f"Producto Test {i}"
    
    # 1. Crear Producto
    data_productos.append({
        "nombre": nombre_prod,
        "codigo": codigo,
        "tipo": "bien", # Forzamos 'bien' para que tenga sentido tener partes
        "origen": "nac",
        "cantidad_vendida": random.randint(10, 500),
        "unidades": ",".join(random.sample(UNIDADES, random.randint(1, 2)))
    })

    # 2. Crear Partes (Entre 2 y 5 partes por producto OBLIGATORIO)
    for j in range(random.randint(2, 5)): 
        data_partes.append({
            "nombre_parte": f"Componente {j+1} del {codigo}",
            "ref_producto": codigo, # Esta es la clave de enlace
            "descripcion": "Parte generada automáticamente"
        })

# --- GUARDAR EXCEL ---
df_prod = pd.DataFrame(data_productos)
df_part = pd.DataFrame(data_partes)

# Forzamos que las columnas clave sean texto (string) para evitar errores de tipo
df_prod['codigo'] = df_prod['codigo'].astype(str)
df_part['ref_producto'] = df_part['ref_producto'].astype(str)

with pd.ExcelWriter('datos_prueba.xlsx') as writer:
    df_prod.to_excel(writer, sheet_name='Productos', index=False)
    df_part.to_excel(writer, sheet_name='Partes', index=False)

print(f"¡Listo! Excel creado.")
print(f"-> {len(df_prod)} Productos")
print(f"-> {len(df_part)} Partes (Deberían cargarse todas)")
