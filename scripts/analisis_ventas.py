import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Se utilizan rutas relativas para asegurar reproducibilidad
# en Google Colab y otros entornos.

base_dir = Path.cwd()

datos_path = base_dir / "datos" / "ventas.csv"
resultados_dir = base_dir / "resultados"

# Creación automática de carpeta de resultados
resultados_dir.mkdir(exist_ok=True)

# Lectura del dataset
ventas = pd.read_csv(datos_path)

# Conversión de fecha
ventas["fecha"] = pd.to_datetime(ventas["fecha"])

# Cálculo de ventas totales
ventas["total_venta"] = ventas["cantidad"] * ventas["precio_unitario"]

ventas_totales = ventas["total_venta"].sum()

# Producto más vendido
producto_mas_vendido = ventas.groupby("producto")["cantidad"].sum().idxmax()

cantidad_producto = ventas.groupby("producto")["cantidad"].sum().max()

# Ventas por mes
ventas["mes"] = ventas["fecha"].dt.to_period("M").astype(str)

ventas_por_mes = ventas.groupby("mes")["total_venta"].sum().reset_index()

# Exportación de resultados
resumen = pd.DataFrame({
    "Indicador": [
        "Ventas Totales",
        "Producto Más Vendido",
        "Cantidad Vendida"
    ],
    "Resultado": [
        ventas_totales,
        producto_mas_vendido,
        cantidad_producto
    ]
})

resumen.to_csv(resultados_dir / "resumen_ventas.csv", index=False)

# Generación de gráfico
plt.figure(figsize=(8,5))

plt.plot(
    ventas_por_mes["mes"],
    ventas_por_mes["total_venta"],
    marker="o"
)

plt.title("Evolución mensual de ventas")
plt.xlabel("Mes")
plt.ylabel("Ventas Totales")

plt.grid(True)

plt.savefig(resultados_dir / "grafico_ventas.png")

plt.close()

print("Análisis completado correctamente.")
print(f"Ventas totales: ${ventas_totales}")
print(f"Producto más vendido: {producto_mas_vendido}")
print(f"Cantidad vendida: {cantidad_producto}")
