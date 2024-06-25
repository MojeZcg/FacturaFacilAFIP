import os
import time
from tkinter import StringVar, simpledialog

import ttkbootstrap as ttk
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

load_dotenv()


def iniciar_navegador():
    driver_path = os.getenv('DRIVER_PATH')
    service = Service(driver_path)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def abrir_pagina(driver, url):
    driver.get(url)
    
def siguiente():
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@value="Continuar >"]'))
    ).click()

def realizar_operacion(driver, clientcuil, option, products):
    abrir_pagina(driver, "https://auth.afip.gob.ar/contribuyente_/login.xhtml")
    
    try:
        # Selecciona el campo CUIL
        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "F1:username"))
        )
        
        # Ingresar el Cuil Correspondiente
        username.send_keys(os.getenv('AFIP_CUIL'))
        username.send_keys(Keys.RETURN)
        
        # Selecciona el campo Clave
        password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "F1:password"))
        )
        
        # Ingresar la Clave Correspondiente
        password.send_keys(os.getenv('AFIP_KEY'))
        password.send_keys(Keys.RETURN)
        
        #Ingresa a responsable inscripto
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.full-width"))
        ).click()
        
        time.sleep(1)
        driver.switch_to.window(driver.window_handles[-1])
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input.btn_empresa"))
        ).click()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "btn_gen_cmp"))
        ).click()
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "novolveramostrar"))
        ).click()
        
        
        puntodeventa = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "puntoDeVenta"))
        )
        select = Select(puntodeventa)
        select.select_by_index(1)
        
        siguiente()
        
        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "idconcepto"))
        )
        select = Select(dropdown)
        select.select_by_index(1)
        
        
        siguiente()
        
        
        condicion = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "idivareceptor"))
        )
        
        select = Select(condicion)
        select.select_by_index(option)
        
        
        cuil = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nrodocreceptor"))
        )
        
        cuil.send_keys(clientcuil)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "formadepago1"))
        ).click()
        
        
        time.sleep(10)
        
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        # Cerrar Chrome
        driver.quit()
        
class App:
    def __init__(self, root):
        self.root = root
        
        # Configuracion de la pestaña
        self.root.title("Factura Fácil AFIP")
        self.root.iconbitmap('afip.ico') 
        self.root.geometry("615x420")

        # Crear campos de entrada de Cuil
        ttk.Label(root, text="Cuil del cliente:").place(x=10, y=10)
        self.cuil = ttk.Entry(root, bootstyle="secondary")
        self.cuil.place(x=10, y=32, width=130, height=30)

        # Crear campo y opciones para el OptionMenu
        self.options = ('Consumidor Final', 'Iva Responsable Inscripto', 'Iva Sujeto Excento')
        self.option_var = ttk.StringVar(value=self.options[0])
        
        ttk.Label(root, text="Condición frente al IVA:").place(x=170, y=10)
        self.option = ttk.OptionMenu(root, self.option_var, self.options[0], *self.options, bootstyle="dark")
        self.option.place(x=170, y=32, width=200, height=30)

        # Crear tabla
        self.tree = ttk.Treeview(root, bootstyle="dark", columns=("name", "quantity", "unique_price", "total_price"), show='headings')
        self.tree.heading("name", text="Nombre")
        self.tree.heading("quantity", text="Cantidad (Unidades)")
        self.tree.heading("unique_price", text="Precio por Unidad (ARS)")
        self.tree.heading("total_price", text="Precio Total (ARS)")
        
        self.tree.column("name", anchor=ttk.E, width=150)
        self.tree.column("quantity",anchor=ttk.E,  width=150)
        self.tree.column("unique_price",anchor=ttk.E,  width=150)
        self.tree.column("total_price",anchor=ttk.E, width=149)
        self.tree.place(x=5, y=75, width=600)
        
        # Crear campo y opciones para el OptionMenu
        self.common_products = ('Revelado de Fotografias', 'Laser', 'Sublimación')
        
        ttk.Label(root, text="Nombre de producto:").place(x=10, y=265)
        self.name = ttk.Combobox(root,bootstyle="secondary", values=self.common_products)
        self.name.place(x=10, y=285, height=25, width=150)
        
        ttk.Label(root, text="Cantidad:").place(x=10, y=315)
        self.quantity = ttk.Entry(root,bootstyle="secondary")
        self.quantity.place(x=10, y=335, height=25, width=150)
        
        ttk.Label(root, text="Precio Unitario:").place(x=10, y=365)
        self.priceu = ttk.Entry(root,bootstyle="secondary")
        self.priceu.place(x=10, y=385, height=25, width=150)
        
        
        
        self.add_row_button = ttk.Button(root, bootstyle="default-outline", text="Agregar Producto", command=self.add_row)
        self.add_row_button.place(x=180, y=313, width=140, height=28)
        
        self.remove_row_button = ttk.Button(root, bootstyle="danger-outline", text="Eliminar Seleccionados", command=self.add_row)
        self.remove_row_button.place(x=180, y=348, width=140, height=28)
        
        self.remove_all_button = ttk.Button(root, bootstyle="dark", text="Eliminar Todos", command=self.add_row)
        self.remove_all_button.place(x=180, y=383, width=140, height=28)

        # Botón para ejecutar las funciones de Selenium
        self.selenium_button = ttk.Button(root, bootstyle="success-outline", text="Enviar", command=self.ejecutar_selenium)
        self.selenium_button.place(x=485, y=270, width=120)
        
        self.error_label = ttk.Label(root, text='', bootstyle="danger")
        self.error_label.place(x=330, y=390)

        # Variables para almacenar los valores
        self.var_cuil = ""
        self.var_option = ""

    def add_row(self):
        if self.name.get() == '' or self.quantity.get() == '' or self.priceu.get() == '':
            self.error_label.config(text="Error: Falta informacion en el producto")
        else:
            try:
                q = float(self.quantity.get())
                p = float(self.priceu.get())
                total_price = f'${q * p}'
                self.tree.insert("", "end", values=(self.name.get(),  self.quantity.get() , self.priceu.get(), total_price))
            except ValueError:
                self.error_label.config(text='La Cantidad o el Precio Unitario no es un numero')
                
    def ejecutar_selenium(self):
        cuil = self.cuil.get()
        option = self.option_var.get()
        products = []
        
        driver = iniciar_navegador()
        realizar_operacion(driver, clientcuil=cuil, option=option, products=products)

if __name__ == "__main__":
    root = ttk.Window()
    app = App(root)
    root.mainloop()       


