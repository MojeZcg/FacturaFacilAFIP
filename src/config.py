"""Configuración inicial de la aplicación usando tkinter."""

import sys
from pathlib import Path
import os
import tkinter as tk
import ttkbootstrap as ttk
from tkinter import filedialog, messagebox


def resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso, ya sea en desarrollo o en PyInstaller"""
    try:
        base_path = Path(sys._MEIPASS)  # pylint: disable=protected-access
    except AttributeError:
        base_path = Path(__file__).parent
    return base_path / relative_path


DEBUG = os.getenv("DEBUG", "0") == "1"
ICON_PATH = resource_path("static/arca.ico")


def initialize_env_gui(root):
    """Inicializa la ventana de configuración inicial si no existe el archivo .env"""
    app_dir = Path(__file__).resolve().parent.parent
    env_path = app_dir / ".env"

    if env_path.exists():
        return

    # --- Ventana principal ---
    root.title("Configuración inicial - ARCA")
    width, height = 320, 220

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    root.geometry(f"{width}x{height}+{x}+{y}")

    root.iconbitmap(ICON_PATH)
    root.resizable(False, False)

    tk.Label(root, text="Configuración de ARCA", font=("Segoe UI", 14, "bold")).place(
        x=50, y=8
    )
    tk.Label(root, text="CUIL/CUIT:").place(x=15, y=50)
    entry_cuil = tk.Entry(root, width=30)
    entry_cuil.place(x=100, y=50, width=200)

    tk.Label(root, text="Clave:").place(x=15, y=75)
    entry_key = tk.Entry(root, width=40, show="*")
    entry_key.place(x=100, y=75, width=200)

    download_path = tk.StringVar(value="C:\\Facturas")

    def select_folder():
        base_path = filedialog.askdirectory(title="Seleccione carpeta base de descarga")
        if base_path:
            full_path = os.path.join(base_path, "MisFacturas")
            os.makedirs(full_path, exist_ok=True)
            download_path.set(full_path)

    tk.Label(root, text="Carpeta de descarga:").place(x=10, y=115)
    tk.Entry(root, textvariable=download_path, width=30, font=("Segoe UI", 9)).place(
        x=15, height=28, y=135
    )
    ttk.Button(
        root,
        text="Seleccionar",
        command=select_folder,
        bootstyle="dark",
        width=10,
    ).place(x=220, y=135, height=28)

    def save_env():
        cuil = "".join(ch for ch in entry_cuil.get().strip() if ch.isdigit())
        key = entry_key.get().strip()
        path = download_path.get().replace("\\", "/")

        if not cuil or not key:
            messagebox.showerror("Error", "Debe ingresar sus credenciales.")
            return

        with open(env_path, "w", encoding="utf-8") as f:
            f.write(f"DOWNLOAD_PATH={path}\n")
            f.write(f"ARCA_CUIL={cuil}\n")
            f.write(f"ARCA_KEY={key}\n")

        messagebox.showinfo("Configuración", "Archivo .env creado correctamente.")
        root.destroy()

    ttk.Button(
        root,
        text="Guardar configuración",
        command=save_env,
        bootstyle="dark",
        width=30,
    ).place(x=50, y=175, height=35)
    root.mainloop()
