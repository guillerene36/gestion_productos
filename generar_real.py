import pandas as pd
import random

# --- DATOS MAESTROS REALES ---
# Definimos listas para combinar y crear variaciones realistas

CATALOGO = {
    'Jumbo': {
        'marcas': ['Colun', 'Nestlé', 'Coca-Cola', 'Tucapel', 'Luchetti', 'Hellmanns', 'Soprole', 'Elite', 'Omo'],
        'productos': ['Leche Entera', 'Yoghurt Batido', 'Arroz G2', 'Fideos Spaghetti', 'Mayonesa', 'Papel Higiénico', 'Detergente Líquido', 'Bebida 3L', 'Café Instantáneo'],
        'origen': 'nac',
        'tipo': 'bien'
    },
    'Easy': {
        'marcas': ['Bosch', 'Makita', 'Black+Decker', 'Stanley', 'Tricolor', 'Ceresita', 'Bauker', '3M'],
        'productos': ['Taladro Percutor', 'Sierra Circular', 'Set de Brocas', 'Pintura Esmalte', 'Lija para Madera', 'Cinta Adhesiva Industrial', 'Esmeril Angular', 'Juego de Llaves'],
        'origen': 'imp', # Mayoría importado
        'tipo': 'bien'
    },
    'Paris': {
        'marcas': ['Samsung', 'Apple', 'Sony', 'LG', 'Nike', 'Adidas', 'Levi\'s', 'HP', 'Lenovo'],
        'productos': ['Smart TV 55"', 'iPhone 14', 'Galaxy S23', 'Notebook Gamer', 'Zapatillas Running', 'Polera Algodón', 'Jeans 501', 'Audífonos Bluetooth'],
        'origen': 'imp',
        'tipo': 'bien'
    }
}

# Unidades posibles para mezclar (Ej: Jumbo y Santa Isabel comparten cosas)
UNIDADES_MIX = {
    'Jumbo': ['Jumbo', 'Jumbo, Santa Isabel'],
    'Easy': ['Easy', 'Easy, Paris'], # Herramientas a veces en Paris
    'Paris': ['Paris', 'Paris, Easy']  # Tecno a veces en Easy
}

data_productos = []
data_partes = []

print("Generando catálogo extendido de 50 productos reales...")

for i in range(1, 51):
    # 1. Elegir una tienda base al azar
    tienda = random.choice(['Jumbo', 'Easy', 'Paris'])
    info = CATALOGO[tienda]
    
    # 2. Armar nombre realista (Marca + Producto)
    marca = random.choice(info['marcas'])
    prod = random.choice(info['productos'])
    nombre_completo = f"{prod} {marca} (Modelo {random.randint(2023, 2025)})"
    
    # 3. Código único
    prefijo = tienda[:3].upper() # JUM, EAS, PAR
    codigo = f"{prefijo}-{marca[:3].upper()}-{i:03d}"
    
    # 4. Unidades de negocio lógicas
    unidades = random.choice(UNIDADES_MIX[tienda])
    
    data_productos.append({
        "nombre": nombre_completo,
        "codigo": codigo,
        "tipo": info['tipo'],
        "origen": info['origen'],
        "cantidad_vendida": random.randint(10, 5000),
        "unidades": unidades
    })
    
    # 5. Generar Partes Lógicas
    # (Ej: Caja, Manual, Accesorio)
    partes_base = ['Caja Original', 'Manual de Usuario', 'Garantía']
    if tienda == 'Easy': partes_base += ['Batería', 'Cable de Poder', 'Repuesto']
    elif tienda == 'Paris': partes_base += ['Cargador', 'Control Remoto', 'Cable HDMI']
    elif tienda == 'Jumbo': partes_base = ['Envase Reciclable', 'Etiqueta', 'Tapa']

    # Elegimos 2 o 3 partes al azar para este producto
    mis_partes = random.sample(partes_base, random.randint(2, 3))
    
    for parte in mis_partes:
        data_partes.append({
            "nombre_parte": f"{parte} para {codigo}",
            "ref_producto": codigo,
            "descripcion": "Componente estándar"
        })

# --- GUARDAR EXCEL ---
df_prod = pd.DataFrame(data_productos)
df_part = pd.DataFrame(data_partes)

# Forzar texto en códigos
df_prod['codigo'] = df_prod['codigo'].astype(str)
df_part['ref_producto'] = df_part['ref_producto'].astype(str)

with pd.ExcelWriter('productos_reales.xlsx') as writer:
    df_prod.to_excel(writer, sheet_name='Productos', index=False)
    df_part.to_excel(writer, sheet_name='Partes', index=False)

print(f"¡Listo! Creados {len(df_prod)} productos y {len(df_part)} partes.")
print("Ejemplo:", data_productos[0]['nombre'], "-", data_productos[0]['unidades'])
