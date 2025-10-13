import threading
import sqlite3
import json
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
import pandas as pd


def download():
    Tk().withdraw()
    save_path = asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Archivos Excel", "*.xlsx")],
        title="Guardar historial como...",
    )
    if not save_path:
        print("❌ No se seleccionó ningún archivo.")
        return

    db_path = "History.db"  # Ajusta según tu ruta
    conn = sqlite3.connect(db_path)

    # Leer datos
    cursor = conn.cursor()
    cursor.execute("SELECT fecha, valor_total, productos FROM facturas")
    rows = cursor.fetchall()

    # Preparar lista para construir el DataFrame
    data = []

    for fecha, valor_total, productos_json in rows:
        try:
            productos = json.loads(productos_json)
            if isinstance(productos, list):
                for p in productos:
                    cantidad = int(p.get("Quantity", 0))
                    data.append(
                        {
                            "Producto": p.get("Product", ""),
                            "Cantidad": cantidad,
                            "Total ($)": f"${valor_total:,.2f}",
                            "Fecha": pd.to_datetime(fecha).strftime(
                                "%d/%m/%Y %H:%M:%S"
                            ),
                        }
                    )
            else:
                data.append(
                    {
                        "Producto": str(productos),
                        "Cantidad": "",
                        "Total ($)": f"${valor_total:,.2f}",
                        "Fecha": pd.to_datetime(fecha).strftime("%d/%m/%Y %H:%M:%S"),
                    }
                )
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            data.append(
                {
                    "Producto": "(JSON inválido)",
                    "Cantidad": "",
                    "Total ($)": f"${valor_total:,.2f}",
                    "Fecha": pd.to_datetime(fecha).strftime("%d/%m/%Y %H:%M:%S"),
                }
            )

    # Crear DataFrame
    df = pd.DataFrame(data)

    # Reordenar columnas
    df = df[["Producto", "Cantidad", "Total ($)", "Fecha"]]

    # Exportar a Excel
    df.to_excel(save_path, index=False)
    print(f"✅ Historial exportado como '{save_path}'")
