from tkinter import ttk
from tkinter import HORIZONTAL, Toplevel

# Define the path to your icon file here
ICON_PATH = "static/arca.ico"


class ProgressWindow:
    """
    Clase que representa una ventana de progreso con una barra de progreso.

    Attributes:
        root (tk.Tk): La ventana principal de la aplicación.
        icon_path (str): La ruta del icono de la ventana de progreso.
        progress_window (tk.Toplevel): La ventana de progreso.
        progress_bar (ttk.Progressbar): La barra de progreso.
    """

    def __init__(self, r, text):
        """
        Inicializa una instancia de ProgressWindow.

        Args:
            root (tk.Tk): La ventana principal de la aplicación.
            text (str): El texto que se mostrará en la ventana de progreso.
        """
        self.root = r
        self.icon_path = ICON_PATH
        self.create_progress_window(text)

    def create_progress_window(self, text):
        """
        Crea y configura la ventana de progreso y la barra de progreso.

        Args:
            text (str): El texto que se mostrará en la ventana de progreso.
        """
        self.progress_window = Toplevel(self.root)
        self.progress_window.geometry("280x60")
        self.progress_window.title("Progreso de Factura")
        self.progress_window.iconbitmap(self.icon_path)

        progress_label = ttk.Label(
            self.progress_window, text=text, font=("TkDefaultFont", 11)
        )
        progress_label.place(x=20, y=0)
        self.progress_bar = ttk.Progressbar(
            self.progress_window,
            orient=HORIZONTAL,
            mode="determinate",
            value=0,
            maximum=100,
            length=230,
        )
        self.progress_bar.place(x=20, y=25, height=25)

    def set_progress(self, p):
        """
        Actualiza el valor de la barra de progreso.

        Args:
            p (int): El valor de progreso que se establecerá en la barra.
        """
        self.progress_bar["value"] = p
        self.progress_window.lift()
        self.progress_window.update_idletasks()

    def stop_progress(self):
        """
        Cierra la ventana de progreso.
        """
        if self.progress_window:
            self.progress_window.destroy()
