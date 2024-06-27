import os
import time
from tkinter import StringVar, simpledialog

import ttkbootstrap as ttk
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

load_dotenv()


download_path = r'C:\Users\w10\Desktop\Facturas'

def start_chrome():
    driver_path = os.getenv('DRIVER_PATH')
    service = Service(driver_path)
    prefs = {
        "download.default_directory": download_path, 
        "download.prompt_for_download": False, 
        "directory_upgrade": True,
        "safebrowsing.enabled": True 
    }
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Ejecutar en modo headless
    options.add_argument("--disable-gpu") 
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=service, options=options)
    return driver
    
def siguiente(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@value="Continuar >"]'))
    ).click()

def login(driver): 
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
        
        #Ingresa a responsable inscripto
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.full-width"))
    ).click()
        
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[-1])
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input.btn_empresa"))
    ).click()

def download_day(driver):
    try:
        login(driver)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "btn_consultas"))
        ).click()
        
        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "idTipoComprobante"))
        )
            
        select = Select(dropdown)
        select.select_by_index(9)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[contains(@value, "Buscar")]'))
        ).click()
        
        ver_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//input[contains(@value, "Ver")]'))
        )
        
        for button in ver_buttons:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable(button)).click()
            time.sleep(5)

    except Exception as e:
        print(f"Ocurrió un error: {e}")

def realizar_operacion(driver, client_option , client_id, option, products):
    try:
        login(driver)
        
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
        
        siguiente(driver)
        
        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "idconcepto"))
        )
        
        select = Select(dropdown)
        select.select_by_index(1)
        
        
        siguiente(driver)
        
        condicion = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "idivareceptor"))
        )
        
        select = Select(condicion)
        select.select_by_index(option)
        
        
        typeid = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "idtipodocreceptor"))
        )
        
        selecttype = Select(typeid)
        selecttype.select_by_index(client_option)
        
        
        clientid = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nrodocreceptor"))
        )
        
        clientid.send_keys(client_id)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "formadepago1"))
        ).click()
        
        siguiente(driver)
        
        for index, product in enumerate(products, start=1):
            
            clientid = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, f"detalle_descripcion{index}"))
            )
            
            clientid.send_keys(product['Product'])
            
            quantity = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, f"detalle_cantidad{index}"))
            )
            
            quantity.clear()
            quantity.send_keys(product['Quantity'])
            
            condicion = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, f"detalle_medida{index}"))
            )
            
            select = Select(condicion)
            select.select_by_index(7)
            
            
            preciou = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, f"detalle_precio{index}"))
            )
            
            preciou.send_keys(product['Price'])
            
            
            if len(products) >= index + 1:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//input[@type="button" and @value="Agregar línea descripción"]'))
                ).click()
            
        siguiente(driver)
        
        try:
            # Espera explícita para que el botón "Confirmar Datos..." sea clickable
            #confirmar_datos_button = WebDriverWait(driver, 10).until(
                #EC.element_to_be_clickable((By.XPATH, '//input[@type="button" and @value="Confirmar Datos..."]'))
            #)
            #confirmar_datos_button.click()

            # Espera a que aparezca la alerta y acéptala
            # WebDriverWait(driver, 10).until(EC.alert_is_present())
            # alert = driver.switch_to.alert
            # alert.accept()

            # Espera explícita para que el botón "Imprimir..." sea clickable
            # imprimir_button = WebDriverWait(driver, 10).until(
                # EC.element_to_be_clickable((By.XPATH, '//input[@type="button" and @value="Imprimir..."]'))
            
            
            #) imprimir_button.click()
            
            time.sleep(20)

        except Exception as e:
            print(f"Ocurrió un error: {e}")
        
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
        self.root.iconbitmap('./static/afip.ico') 
        self.root.geometry("612x420")
        
        self.client_options = ('CUIT', 'CUIL', 'DNI')
        self.client_var = ttk.StringVar(value=self.client_options[0])
        
        # Crear campos de entrada de Cuil
        ttk.Label(root, text="Identificador del cliente:").place(x=10, y=10)
        self.client_type = ttk.OptionMenu(root, self.client_var, self.client_options[0], *self.client_options,  bootstyle="dark")
        self.client_type.place(x=10, y=32, width=75)
        
        self.client = ttk.StringVar()
        self.client.trace_add('write', self.format_client_id)
        
        self.client_entry = ttk.Entry(root, textvariable=self.client)
        self.client_entry.place(x=90, y=32, width=120)
        
        # Crear campo y opciones para el OptionMenu
        self.option_var = ttk.StringVar(value='Consumidor Final')
        self.options = ('Consumidor Final', 'Iva Responsable Inscripto', 'Iva Sujeto Excento')
        
        ttk.Label(root, text="Condición frente al IVA:").place(x=220, y=10)
        self.option = ttk.OptionMenu(root, self.option_var, self.options[0], *self.options, command=self.update_client_options, bootstyle="dark")
        self.option.place(x=220, y=32, width=200, height=30)
        
        # Llamar a update_client_options al inicio para inicializar correctamente
        self.update_client_options(self.options[0])

        # Crear tabla
        self.tree = ttk.Treeview(root, bootstyle="dark", columns=("name", "quantity", "unique_price", "total_price"), show='headings')
        self.tree.heading("name", text="Nombre")
        self.tree.heading("quantity", text="Cantidad (Unidades)")
        self.tree.heading("unique_price", text="Precio por Unidad (ARS)")
        self.tree.heading("total_price", text="Precio Total (ARS)")
        
        self.tree.column("name", anchor=ttk.E, width=150)
        self.tree.column("quantity",anchor=ttk.E,  width=150)
        self.tree.column("unique_price",anchor=ttk.E,  width=150)
        self.tree.column("total_price",anchor=ttk.E, width=140)
        self.tree.place(x=5, y=75, width=600)
        
        # Crear campo y opciones para el OptionMenu
        self.common_products = ('Revelado de Fotografias', 'Laser', 'Sublimación')
        
        ttk.Label(root, text="Nombre de producto:").place(x=10, y=265)
        self.name = ttk.Combobox(root,bootstyle="secondary", values=self.common_products)
        self.name.place(x=10, y=285, height=25, width=150)
        
        ttk.Label(root, text="Cantidad:").place(x=10, y=315)
        self.quantity = ttk.Entry(root, bootstyle="secondary")
        self.quantity.place(x=10, y=335, height=25, width=150)
        
        ttk.Label(root, text="Precio Unitario:").place(x=10, y=365)
        self.priceu = ttk.Entry(root,bootstyle="secondary")
        self.priceu.place(x=10, y=385, height=25, width=150)
        
        self.add_row_button = ttk.Button(root, bootstyle="default-outline", text="Agregar Producto", command=self.add_row)
        self.add_row_button.place(x=180, y=313, width=140, height=28)
        
        self.remove_row_button = ttk.Button(root, bootstyle="danger-outline", text="Eliminar Seleccionados", command=self.delete_rows)
        self.remove_row_button.place(x=180, y=348, width=140, height=28)
        
        self.remove_all_button = ttk.Button(root, bootstyle="dark", text="Eliminar Todos", command=self.delete_all_rows)
        self.remove_all_button.place(x=180, y=383, width=140, height=28)

        # Botón para ejecutar las funciones de Selenium
        self.send_button = ttk.Button(root, bootstyle="success-outline", text="Enviar", command=self.send)
        self.send_button.place(x=485, y=270, width=120)
        
        self.download_button = ttk.Button(root, bootstyle="secundary-outline", text="Descargar facturas", command=self.download)
        self.download_button.place(x=485, y=310, width=120)
        
        self.error_label = ttk.Label(root, text='', bootstyle="danger")
        self.error_label.place(x=330, y=390)
        
        self.raw_client_id = ""
    
    def format_client_id(self, *args):   
        client_var = self.client_var.get()
        if client_var in ('CUIT', 'CUIL'):
            # Guardar la posición actual del cursor
            cursor_position = self.client_entry.index(ttk.INSERT)
            
            new_value = self.client.get()
            cleaned_value = ''.join(filter(str.isdigit, new_value))
            
            # Formatear el valor limpio
            formatted_value = f"{cleaned_value[:2]}-{cleaned_value[2:10]}-{cleaned_value[10:11]}"
            
            # Ajustar el valor del campo de entrada
            self.client.set(formatted_value.strip('-'))
            self.raw_client_id = cleaned_value
            
            # Ajustar la posición del cursor
            formatted_parts = [cleaned_value[:2], cleaned_value[2:10], cleaned_value[10:11]]
            new_cursor_position = cursor_position + sum(len(part) + 1 for part in formatted_parts if part) - (cursor_position > 2) - (cursor_position > 10)
            
            # Asegurar que la posición del cursor no se salga del rango del texto
            new_cursor_position = min(new_cursor_position, len(formatted_value.strip('-')))
            
            # Establecer la nueva posición del cursor
            self.client_entry.icursor(new_cursor_position)
        
    def update_client_options(self, selected_option):
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
            menu.add_command(label=option, command=lambda value=option: self.client_var.set(value))
        
        # Establecer la opción predeterminada
        self.client_var.set(new_client_options[0])

    def add_row(self):
        if self.name.get() == '' or self.quantity.get() == '' or self.priceu.get() == '':
            self.error_label.config(text="Error: Falta informacion en el producto")
        else:
            try:
                q = float(self.quantity.get())
                p = float(self.priceu.get())
                total_price = f'${q * p}'
                self.tree.insert("", "end", values=(self.name.get(),  self.quantity.get() , self.priceu.get(), total_price))
                
                self.name.delete(0, "end")
                self.quantity.delete(0, "end")
                self.priceu.delete(0, "end")
            except ValueError:
                self.error_label.config(text='La Cantidad o el Precio Unitario no es un numero')
    
    def delete_rows(self):
        for selected_item in self.tree.selection():
            self.tree.delete(selected_item)
    
    def delete_all_rows(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def get_client_id_option(self):
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
        if self.tree.get_children() == ():
            self.error_label.config(text='Error: No hay productos')
            return []
        else:
            products = []
            for item in self.tree.get_children():
                item_data  = self.tree.item(item, 'values')
                    
                filtered_products = [[value for index, value in enumerate(item_data) if self.tree['columns'][index] not in 'total_price']]
                    
                for item in filtered_products:
                    products.append({
                        'Product': item[0],
                        'Quantity': item[1],
                        'Price': item[2]
                    })
            return products
    
    def validate_client_id(self):
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
        self.delete_all_rows()
        self.raw_client_id = ''
        self.client_entry.delete(0, "end")
        self.name.delete(0, "end")
        self.quantity.delete(0, "end")
        self.priceu.delete(0, "end")
    
    def download(self):
        driver = start_chrome()
        download_day(driver)
      
    def send(self):
        client_id = self.validate_client_id()
        client_option = self.get_client_id_option()
        option = self.get_selected_option()
        products =  self.get_products()
        
        if client_option != -1 and option != -1 and client_id != -1 and products != []:
            driver = start_chrome()
            realizar_operacion(driver, client_option=client_option , client_id=client_id, option=option, products=products)
            self.clear_all()         

if __name__ == "__main__":
    root = ttk.Window()
    app = App(root)
    root.mainloop()       


