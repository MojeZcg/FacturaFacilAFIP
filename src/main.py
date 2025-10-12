"""
Main file for the App in tkinter. Process with selenium and ttkbootstrap for app style
"""

from pathlib import Path

from tkinter import filedialog, simpledialog, messagebox

import ttkbootstrap as ttk
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from gui.app import App  # Asegúrate de que la ruta de importación sea correcta

from models.database import inicializar_si_necesario, session

inicializar_si_necesario()

load_dotenv()


def initialize_env_gui(rr):
    app_dir = Path(__file__).parent
    env_path = app_dir / ".env"

    if not env_path.exists():
        rr.withdraw()

        download_path = (
            filedialog.askdirectory(title="Seleccione carpeta de descarga")
            or "C:\\Facturas"
        )
        cuil = simpledialog.askstring("AFIP", "Ingrese su CUIL/CUIT:")
        key = simpledialog.askstring("AFIP", "Ingrese su clave:", show="*")

        if not cuil or not key:
            messagebox.showerror("Error", "Debe ingresar sus credenciales.")
            return

        with open(env_path, "w", encoding="utf-8") as f:
            f.write(f"DOWNLOAD_PATH={download_path.replace('\\', '/')}\n")
            f.write(f"AFIP_CUIL={cuil}\n")
            f.write(f"AFIP_KEY={key}\n")

        messagebox.showinfo("Configuración", "Archivo .env creado correctamente.")
    else:
        print("Archivo .env ya existente. Saltando configuración inicial.")


engine = create_engine("sqlite:///History.db", pool_size=20, max_overflow=10)

Session = sessionmaker(bind=engine, future=True)
session = Session()

session.expire_all()

if __name__ == "__main__":
    root = ttk.Window()
    initialize_env_gui(root)
    APP = App(root)
    root.mainloop()
