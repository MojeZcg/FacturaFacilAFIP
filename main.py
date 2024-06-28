import os
import threading
import time
from datetime import datetime
from tkinter.messagebox import showinfo

import ttkbootstrap as ttk
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from sqlalchemy.orm import sessionmaker

from database import Facturas, engine

ICON_PATH = './static/afip.ico'

load_dotenv()

Session = sessionmaker(bind=engine)
session = Session()

fecha_actual = datetime.now()
nombre_carpeta = fecha_actual.strftime('%d de %B %Y')

download_path = os.path.join(r'C:\Users\w10\Desktop\Facturas', nombre_carpeta)

if not os.path.exists(download_path):
    os.makedirs(download_path)


def start_chrome():
    """
    Inicia una instancia del navegador Chrome con opciones predefinidas.

    Returns:
        WebDriver: Una instancia del controlador de Chrome.
    """
    driver_path = os.getenv('DRIVER_PATH')
    service = Service(driver_path)
    prefs = {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True
    }
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def siguiente(driver):
    """
    Hace clic en el botón "Continuar" en la página actual del navegador.

    Args:
        driver (WebDriver): La instancia del controlador de Chrome.
    """
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, '//input[@value="Continuar >"]')
        )
    ).click()

def login(driver):
    """
    Realiza el inicio de sesión en la página de AFIP y navega a la sección
    correspondiente.

    Args:
        driver (WebDriver): La instancia del controlador de Chrome.
    """
    driver.get("https://auth.afip.gob.ar/contribuyente_/login.xhtml")
    username = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "F1:username"))
    )
    # Ingresar el Cuil Correspondiente
    username.clear()
    username.send_keys(os.getenv('AFIP_CUIL'))
    username.send_keys(Keys.RETURN)
    # Selecciona el campo Clave
    password = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "F1:password"))
    )
    # Ingresar la Clave Correspondiente
    password.clear()
    password.send_keys(os.getenv('AFIP_KEY'))
    password.send_keys(Keys.RETURN)
    # Ingresa a responsable inscripto
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.full-width"))
    ).click()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[-1])
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input.btn_empresa"))
    ).click()


def delete_files_with_parentheses(directory):
    """
    Elimina archivos con paréntesis en sus nombres dentro de un directorio
    especificado.

    Args:
        directory (str): La ruta del directorio donde se buscarán los archivos.
    """
    for filename in os.listdir(directory):
        if '(' in filename or ')' in filename:
            file_path = os.path.join(directory, filename)
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")


def download_day(driver):
    """
    Descarga las facturas del día desde la página de AFIP y las guarda en el
    directorio predefinido.

    Args:
        driver (WebDriver): La instancia del controlador de Chrome.
    """
    no_invoices = True
    progress('Descarga del Dia')
    try:
        login(driver)
        set_progress(20)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "btn_consultas"))
        ).click()
        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "idTipoComprobante"))
        )
        set_progress(40)
        select = Select(dropdown)
        select.select_by_index(9)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[contains(@value, "Buscar")]')
            )
        ).click()
        set_progress(55)
        ver_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, '//input[contains(@value, "Ver")]')
            )
        )
        set_progress(70)
        no_invoices = False
        for button in ver_buttons:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(button)
            ).click()
            time.sleep(4)
        time.sleep(3)
        delete_files_with_parentheses(download_path)
        set_progress(100)

    except Exception as e:
        if no_invoices:
            stop_progress()
            showinfo(
                title='Descargar Facturas',
                message='Hoy no hay facturas para descargar.',
            )
        else:
            print(f"Ocurrió un error: {e}")


def download_in_thread():
    """
    Inicia una nueva instancia del navegador Chrome y descarga las facturas del
    día en un hilo separado.
    """
    driver = start_chrome()
    thread = threading.Thread(target=download_day, args=(driver,))
    thread.start()


def center_window(window):
    """
    Centra una ventana de tkinter en la pantalla.

    Args:
        window (ttk.Window): La instancia de la ventana de tkinter.
    """
    window.update_idletasks()

    width = window.winfo_width()
    height = window.winfo_height()

    x_offset = (window.winfo_screenwidth() - width) // 2
    y_offset = (window.winfo_screenheight() - height) // 2

    window.geometry(f'+{x_offset}+{y_offset}')


def progress(text):
    """
    Muestra una ventana de progreso con una barra de progreso.

    Args:
        text (str): El texto que se mostrará en la ventana de progreso.
    """
    global progress_window, progress_bar

    progress_window = ttk.Toplevel(app)
    progress_window.geometry("280x60")
    progress_window.title("Progreso de Factura")
    progress_window.iconbitmap(ICON_PATH)

    progress_label = ttk.Label(
        progress_window,
        text=text,
        font=('TkDefaultFont', 11)
    )
    progress_label.place(x=20, y=0)

    progress_bar = ttk.Progressbar(
        progress_window, orient=ttk.HORIZONTAL, mode='determinate',
        value=0, maximum=100, length=230, bootstyle="success"
    )
    progress_bar.place(x=20, y=25, height=25)


def in_thread(client_option, client_id, option, products):
    """
    Realiza una operación en un hilo separado y muestra la ventana de progreso.

    Args:
        client_option (int): La opción del cliente.
        client_id (str): El identificador del cliente.
        option (int): La opción seleccionada.
        products (list): La lista de productos.
    """
    driver = start_chrome()

    thread = threading.Thread(
        target=realizar_operacion,
        args=(driver, client_option, client_id, option, products,)
        )
    threadprogress = threading.Thread(target=progress, args=('Facturacion',))

    thread.start()
    threadprogress.start()


def set_progress(progress):
    """
    Actualiza el valor de la barra de progreso.

    Args:
        progress (int): El valor de progreso que se establecerá en la barra.
    """
    global progress_bar
    progress_bar['value'] = progress
    progress_window.lift()
    progress_window.update_idletasks()


def stop_progress():
    """
    Cierra la ventana de progreso.
    """
    global progress_window
    if progress_window:
        progress_window.destroy()


def realizar_operacion(driver, client_option, client_id, option, products):
    """
    Realiza una operación de facturación en la página de AFIP utilizando los
    datos proporcionados.

    Args:
        driver (WebDriver): La instancia del controlador de Chrome.
        client_option (int): La opción del cliente.
        client_id (str): El identificador del cliente.
        option (int): La opción seleccionada.
        products (list): La lista de productos.
    """
    try:
        login(driver)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "btn_gen_cmp"))
        ).click()
        set_progress(5)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "novolveramostrar"))
        ).click()
        set_progress(10)
        puntodeventa = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "puntoDeVenta"))
        )
        select = Select(puntodeventa)
        select.select_by_index(1)
        siguiente(driver)
        set_progress(18)
        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "idconcepto"))
        )
        select = Select(dropdown)
        select.select_by_index(1)
        set_progress(25)
        siguiente(driver)
        condicion = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "idivareceptor"))
        )
        set_progress(30)
        select = Select(condicion)
        select.select_by_index(option)
        typeid = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "idtipodocreceptor"))
        )
        set_progress(45)
        selecttype = Select(typeid)
        selecttype.select_by_index(client_option)
        clientid = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nrodocreceptor"))
        )
        set_progress(52)
        clientid.send_keys(client_id)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "formadepago1"))
        ).click()
        set_progress(60)
        siguiente(driver)
        for index, product in enumerate(products, start=1):
            clientid = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, f"detalle_descripcion{index}")
                    )
            )
            clientid.send_keys(product['Product'])
            quantity = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, f"detalle_cantidad{index}")
                    )
            )
            quantity.clear()
            quantity.send_keys(product['Quantity'])
            condicion = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, f"detalle_medida{index}")
                    )
            )
            select = Select(condicion)
            select.select_by_index(7)
            preciou = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.ID, f"detalle_precio{index}")
                    )
            )
            preciou.send_keys(product['Price'])
            if len(products) >= index + 1:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            '//input[@type="button" and @value="Agregar línea descripción"]'
                        )
                    )
                ).click()
        set_progress(75)

        siguiente(driver)

        set_progress(80)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//input[@type="button" and @value="Confirmar Datos..."]'
                    )
                    )
            ).click()

            set_progress(85)

            WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()

            set_progress(90)

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH,
                     '//input[@type="button" and @value="Imprimir..."]')
                )
            ).click()

            set_progress(95)
            time.sleep(6)
            set_progress(100)

        except Exception as e:
            print(f"Ocurrió un error: {e}")

    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        # Cerrar Chrome y parar el progreso
        driver.quit()
        stop_progress()


class App:
    """
    Crea la clase de la aplicación.
    """
    def __init__(self, root):
        """
        Inicializa la interfaz de la aplicación.

        Args:
            root (ttk.Window): La instancia de la ventana raíz de tkinter.
        """
        self.root = root

        # Configuracion de la pestaña root
        self.root.title("Factura Fácil AFIP")
        self.root.resizable(False, False)
        self.root.iconbitmap(ICON_PATH)
        self.root.geometry("612x420")

        self.client_options = ('CUIT', 'CUIL', 'DNI')
        self.client_var = ttk.StringVar(value=self.client_options[0])

        # Crear campos de entrada del id del cliente
        ttk.Label(root, text="Identificador del cliente:").place(x=10, y=10)
        self.client_type = ttk.OptionMenu(
            root, self.client_var,
            self.client_options[0],
            *self.client_options,
            bootstyle="dark"
        )
        self.client_type.place(x=10, y=32, width=75)

        self.client = ttk.StringVar()
        self.client.trace_add('write', self.format_client_id)

        self.client_entry = ttk.Entry(root, textvariable=self.client)
        self.client_entry.place(x=90, y=32, width=120)

        # Crear campo y opciones para el OptionMenu
        self.option_var = ttk.StringVar(value='Consumidor Final')
        self.options = (
            'Consumidor Final',
            'Iva Responsable Inscripto',
            'Iva Sujeto Excento'
        )

        ttk.Label(root, text="Condición frente al IVA:").place(x=220, y=10)
        self.option = ttk.OptionMenu(root,
                                     self.option_var,
                                     self.options[0],
                                     *self.options,
                                     command=self.update_client_options,
                                     bootstyle="dark"
                                     )
        self.option.place(x=220, y=32, width=200, height=30)
        # Llamar a update_client_options al inicio
        # para inicializar correctamente
        self.update_client_options(self.options[0])

        # Crear tabla
        self.tree = ttk.Treeview(root,
                                 bootstyle="dark",
                                 columns=(
                                     "name",
                                     "quantity",
                                     "unique_price",
                                     "total_price"
                                     ),
                                 show='headings'
                                 )
        self.tree.heading("name", text="Nombre")
        self.tree.heading("quantity", text="Cantidad (Unidades)")
        self.tree.heading("unique_price", text="Precio por Unidad (ARS)")
        self.tree.heading("total_price", text="Precio Parcial (ARS)")

        self.tree.column("name", width=150)
        self.tree.column("quantity", anchor=ttk.E, width=150)
        self.tree.column("unique_price", anchor=ttk.E, width=150)
        self.tree.column("total_price", anchor=ttk.E, width=140)
        self.tree.place(x=5, y=75, width=600)

        # Crear campo y opciones para el OptionMenu
        self.common_products = (
            'Fotos Carnet',
            'Revelado de Fotos',
            'Servicio Laser',
            'Estampados'
            )

        ttk.Label(root, text="Nombre de producto:").place(x=10, y=265)
        self.name = ttk.Combobox(
            root,
            bootstyle="secondary",
            values=self.common_products
        )

        self.name.place(x=10, y=285, height=25, width=150)

        ttk.Label(root, text="Cantidad:").place(x=10, y=315)
        self.quantity = ttk.Entry(root, bootstyle="secondary")
        self.quantity.place(x=10, y=335, height=25, width=150)

        ttk.Label(root, text="Precio Unitario:").place(x=10, y=365)
        self.priceu = ttk.Entry(root, bootstyle="secondary")
        self.priceu.place(x=10, y=385, height=25, width=150)

        self.add_row_button = ttk.Button(
            root,
            bootstyle="default-outline",
            text="Agregar Producto",
            command=self.add_row
        )

        self.add_row_button.place(x=180, y=313, width=140, height=28)

        self.remove_row_button = ttk.Button(
            root,
            bootstyle="danger-outline",
            text="Eliminar Seleccionados",
            command=self.delete_rows
        )
        self.remove_row_button.place(x=180, y=348, width=140, height=28)

        self.remove_all_button = ttk.Button(
            root,
            bootstyle="dark",
            text="Eliminar Todos",
            command=self.delete_all_rows
            )
        self.remove_all_button.place(x=180, y=383, width=140, height=28)

        self.text_total = ttk.Label(root, bootstyle="dark", text='Total: 0$')
        self.text_total.place(x=395, y=265)

        # Botón para ejecutar las funciones de Selenium
        self.send_button = ttk.Button(
            root,
            bootstyle="success-outline",
            text="Enviar",
            command=self.send
        )
        self.send_button.place(x=485, y=270, width=120)

        self.download_button = ttk.Button(
            root,
            bootstyle="secundary-outline",
            text="Descargar facturas",
            command=self.download
        )
        self.download_button.place(x=485, y=310, width=120)

        self.error_label = ttk.Label(root, text='', bootstyle="danger")
        self.error_label.place(x=330, y=390)

        self.raw_client_id = ""

        center_window(self.root)

    def obtener_valores_columna(self):
        valores = []
        for item_id in self.tree.get_children():
            valor_columna = self.tree.item(item_id, 'values')[3]
            valores.append(valor_columna)
        return valores

    def actualizar_label(self):
        valores = self.obtener_valores_columna()
        resultado = 0
        for valor in valores:
            resultado += float(valor)
        self.text_total.config(text=f"Total: {resultado}$")

    def format_client_id(self, *args):
        client_var = self.client_var.get()
        if client_var in ('CUIT', 'CUIL'):
            # Guardar la posición actual del cursor
            cursor = self.client_entry.index(ttk.INSERT)

            new_value = self.client.get()
            clean = ''.join(filter(str.isdigit, new_value))

            # Formatear el valor limpio
            formatted_value = f"{clean[:2]}-{clean[2:10]}-{clean[10:11]}"

            # Ajustar el valor del campo de entrada
            self.client.set(formatted_value.strip('-'))
            self.raw_client_id = clean

            # Ajustar la posición del cursor
            formatted_parts = [
                clean[:2],
                clean[2:10],
                clean[10:11]
                ]

            new = (
                cursor +
                sum(len(part) + 1 for part in formatted_parts if part) -
                (cursor > 2) -
                (cursor > 10)
            )

            # Asegurar que la posición del
            # cursor no se salga del rango del texto
            new = min(new, len(formatted_value.strip('-')))

            # Establecer la nueva posición del cursor
            self.client_entry.icursor(new)

    def update_client_options(self, selected_option):
        """
        Actualiza las opciones del identificador del cliente en función de la
        condición frente al IVA seleccionada.

        Args:
            selected_option (str): La condición frente al IVA seleccionada.
        """
        if selected_option == 'Iva Responsable Inscripto':
            new_client_options = ('CUIT',)
        elif selected_option == 'Iva Sujeto Excento':
            new_client_options = ('CUIT',)
        else:  # Consumidor Final
            new_client_options = ('CUIT', 'CUIL', 'DNI')

        # Actualizar las opciones del primer OptionMenu
        menu = self.client_type["menu"]
        menu.delete(0, "end")

        for option in new_client_options:
            menu.add_command(
                label=option,
                command=lambda
                value=option: self.client_var.set(value)
                )

        # Establecer la opción predeterminada
        self.client_var.set(new_client_options[0])

    def add_row(self):
        """
        Agrega un producto a la tabla de productos.
        """
        if self.name.get() == '' or self.quantity.get() == '' or self.priceu.get() == '':
            self.error_label.config(
                text="Error: Falta informacion en el producto"
            )
        else:
            try:
                q = float(self.quantity.get())
                p = float(self.priceu.get())
                total_price = q * p
                self.tree.insert(
                    "",
                    "end",
                    values=(
                        self.name.get(),
                        self.quantity.get(),
                        self.priceu.get(),
                        total_price)
                    )

                self.name.delete(0, "end")
                self.quantity.delete(0, "end")
                self.priceu.delete(0, "end")
                self.error_label.config(text="")
                self.actualizar_label()
            except ValueError:
                self.error_label.config(
                    text='La Cantidad o el Precio Unitario no es un numero'
                )

    def delete_rows(self):
        """
        Elimina los productos seleccionados de la tabla de productos.
        """
        for selected_item in self.tree.selection():
            self.tree.delete(selected_item)

    def delete_all_rows(self):
        """
        Elimina todos los productos de la tabla de productos.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)

    def get_client_id_option(self):
        """
        Obtiene el índice de la opción del identificador del cliente.

        Returns:
            int: El índice de la opción del identificador del cliente.
        """
        client_var = self.client_var.get()

        if client_var == 'CUIT':
            return 0
        elif client_var == 'CUIL':
            return 1
        elif client_var == 'DNI':
            return 6
        else:
            return -1

    def get_selected_option(self):
        """
        Obtiene el índice de la condición frente al IVA seleccionada.

        Returns:
            int: El índice de la condición frente al IVA seleccionada.
        """
        option_var = self.option_var.get()
        if option_var == 'Consumidor Final':
            return 3
        elif option_var == 'Iva Responsable Inscripto':
            return 1
        elif option_var == 'Iva Sujeto Excento':
            return 2
        else:
            return -1

    def get_products(self):
        """
        Obtiene la lista de productos de la tabla de productos.

        Returns:
            list: La lista de productos.
        """
        if self.tree.get_children() == ():
            self.error_label.config(text='Error: No hay productos')
            return []
        else:
            products = []
            for item in self.tree.get_children():
                item_data = self.tree.item(item, 'values')

                filtered_products = [
                    [
                        value for index, value in enumerate(item_data)
                        if self.tree['columns'][index]
                        not in 'total_price']
                    ]

                for item in filtered_products:
                    products.append({
                        'Product': item[0],
                        'Quantity': item[1],
                        'Price': item[2]
                    })
            return products

    def validate_client_id(self):
        """
        Valida el identificador del cliente.

        Returns:
            str: El identificador del cliente si es válido.
            int: -1 si el identificador del cliente no es válido.
        """
        FORMAT_ERROR = 'El id del cliente (CUIT, CUIL o DNI) no es valido.'

        client_id = self.raw_client_id
        client_type_var = self.client_var.get()

        if client_id == '':
            return client_id

        valid_lengths = {
            'CUIT': [10, 11],
            'CUIL': [10, 11],
            'DNI': [7, 8]
        }

        if client_type_var not in valid_lengths:
            return -1

        if len(client_id) not in valid_lengths[client_type_var]:
            self.error_label.config(text=FORMAT_ERROR)
            return -1

        try:
            int(client_id)
            return client_id
        except ValueError:
            self.error_label.config(text=FORMAT_ERROR)
            return -1

    def clear_all(self):
        """
        Limpia todos los campos de entrada y la tabla de productos.
        """
        self.delete_all_rows()
        self.raw_client_id = ''
        self.client_entry.delete(0, "end")
        self.name.delete(0, "end")
        self.quantity.delete(0, "end")
        self.priceu.delete(0, "end")
        self.error_label.config(text="")

    def download(self):
        """
        Descarga las facturas en un hilo separado.
        """
        download_in_thread()

    def send(self):
        """
        Envía los datos de facturación a la página de AFIP y guarda la factura en la
        base de datos.
        """
        client_id = self.validate_client_id()
        client_option = self.get_client_id_option()
        option = self.get_selected_option()
        products = self.get_products()
        totalvalue = 0

        for product in products:
            price = float(product['Price'])
            quantity = float(product['Quantity'])
            totalvalue += (price * quantity)

        factura = Facturas(
            id_cliente=client_id,
            tipo_de_documento_id=client_option,
            condicion_iva=option,
            productos=products,
            valor_total=totalvalue,
        )

        if client_option != -1 and option != -1 and client_id != -1 and products != []:
            session.add(factura)
            session.commit()

            in_thread(
                client_option=client_option,
                client_id=client_id,
                option=option,
                products=products
            )

            self.clear_all()
            session.close()


if __name__ == "__main__":
    root = ttk.Window()
    app = App(root)
    root.mainloop()
