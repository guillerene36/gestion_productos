import pandas as pd
import random

# --- CONFIGURACIÓN ---
CANTIDAD_PRODUCTOS = 50
TIPOS = ['bien', 'servicio']
ORIGENES = ['imp', 'nac']
UNIDADES = ['Jumbo', 'Easy', 'Santa Isabel', 'Paris'] # Deben existir en tu Odoo

data_productos = []
data_partes = []

print(f"Generando {CANTIDAD_PRODUCTOS} productos de prueba...")

for i in range(1, CANTIDAD_PRODUCTOS + 1):
    # 1. Datos del Producto
    codigo = f"PROD-{i:04d}" # Ej: PROD-0001
    nombre_prod = f"Producto de Prueba {i}"
    tipo = random.choice(TIPOS)
    origen = random.choice(ORIGENES)
    ventas = random.randint(0, 1000)
    
    # Seleccionamos unidades al azar (ej: Jumbo, Easy)
    num_unidades = random.randint(1, 3)
    unidades_seleccionadas = ",".join(random.sample(UNIDADES, num_unidades))

    data_productos.append({
        "nombre": nombre_prod,
        "codigo": codigo,
        "tipo": tipo,
        "origen": origen,
        "cantidad_vendida": ventas,
        "unidades": unidades_seleccionadas
    })

    # 2. Generamos Partes para este producto (Solo si es un 'bien')
    if tipo == 'bien':
        for j in range(random.randint(1, 4)): # Entre 1 y 4 partes por producto
            data_partes.append({
                "nombre_parte": f"Parte {j+1} de {codigo}",
                "ref_producto": codigo # Clave para vincular después
            })

# --- CREAR DATAFRAMES Y GUARDAR EXCEL ---
df_prod = pd.DataFrame(data_productos)
df_part = pd.DataFrame(data_partes)

with pd.ExcelWriter('datos_prueba.xlsx') as writer:
    df_prod.to_excel(writer, sheet_name='Productos', index=False)
    df_part.to_excel(writer, sheet_name='Partes', index=False)

print("¡Listo! Archivo 'datos_prueba.xlsx' generado con éxito.")
print(f"Productos: {len(df_prod)}")
print(f"Partes: {len(df_part)}")
