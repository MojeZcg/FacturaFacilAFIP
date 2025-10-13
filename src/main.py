"""
Main file for the App in tkinter. Process with selenium and ttkbootstrap for app style
"""

import ttkbootstrap as ttk
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from gui.app import App
from config import initialize_env_gui

from models.database import inicializar_si_necesario, session


inicializar_si_necesario()

load_dotenv()


engine = create_engine("sqlite:///History.db", pool_size=20, max_overflow=10)

Session = sessionmaker(bind=engine, future=True)
session = Session()

session.expire_all()

if __name__ == "__main__":
    root = ttk.Window()
    initialize_env_gui(root)
    APP = App(root)
    root.mainloop()
