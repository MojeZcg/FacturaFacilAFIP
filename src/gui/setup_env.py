import tkinter as tk
import os
from tkinter import filedialog, messagebox
from pathlib import Path
from gui.app import ICON_PATH


def initialize_env_gui(root):
    app_dir = Path(__file__).resolve().parent.parent
    env_path = app_dir / ".env"

    if env_path.exists():
        print("Archivo .env ya existente. Saltando configuración inicial.")
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
        x=50, y=10
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

    frame_folder = tk.Frame(root)
    frame_folder.place(x=15, y=105)
    tk.Label(frame_folder, text="Carpeta de descarga:").pack(anchor="w")
    tk.Entry(frame_folder, textvariable=download_path, width=32).pack(
        side="left", padx=(3, 5)
    )
    tk.Button(frame_folder, text="Seleccionar", command=select_folder, width=10).pack(
        pady=5
    )

    def save_env():
        cuil = entry_cuil.get().strip()
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

    tk.Button(
        root,
        text="Guardar configuración",
        command=save_env,
        bg="#0078D7",
        fg="white",
        width=30,
        height=2,
    ).place(x=50, y=167)
    root.mainloop()
