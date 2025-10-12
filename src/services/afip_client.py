import os
import time
from datetime import datetime

from tkinter.messagebox import showerror
from pathlib import Path
from dotenv import load_dotenv


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from selenium.common.exceptions import TimeoutException

from webdriver_manager.chrome import ChromeDriverManager

from gui.progress import ProgressWindow


# Configuración de la carpeta de descargas
fecha_actual = datetime.now()
nombre_carpeta = fecha_actual.strftime("%d de %B %Y")

default_path = Path(str(os.getenv("DOWNLOAD_PATH")))

download_path = os.path.join(default_path, nombre_carpeta)


# Crear la carpeta de descargas si no existe
if not os.path.exists(download_path):
    os.makedirs(download_path)


def start_chrome():
    """
    Inicia una instancia del navegador Chrome con opciones predefinidas,
    descargando automáticamente el driver compatible si es necesario.
    """
    load_dotenv()  # Cargar variables del .env

    prefs = {
        "download.default_directory": download_path,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True,
    }

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    options.add_argument("--log-level=3")
    options.add_argument("--disable-gpu")
    options.add_experimental_option("prefs", prefs)

    # Aquí se usa webdriver-manager para gestionar automáticamente el driver
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)
    return driver


def login(driver):
    """
    Realiza el inicio de sesión en la página de ARCA y navega a la sección
    correspondiente.

    Args:
        driver (WebDriver): La instancia del controlador de Chrome.
    """
    load_dotenv()

    try:
        driver.get("https://auth.afip.gob.ar/contribuyente_/login.xhtml")

        username = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "F1:username"))
        )

        # Ingresar el Cuil Correspondiente
        username.clear()
        arca_cuil = os.getenv("ARCA_CUIL")

        if arca_cuil is None:
            raise ValueError("La variable de entorno 'ARCA_CUIL' no está definida.")

        username.send_keys(arca_cuil)
        username.send_keys(Keys.RETURN)

        # Selecciona el campo Clave
        password = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "F1:password"))
        )

        # Ingresar la Clave Correspondiente
        password.clear()
        arca_key = os.getenv("ARCA_KEY")

        if arca_key is None:
            raise ValueError("La variable de entorno 'ARCA_KEY' no está definida.")

        password.send_keys(arca_key)
        password.send_keys(Keys.RETURN)

        # Ingresa a responsable inscripto
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a.full-width"))
        ).click()

        time.sleep(1)

        driver.switch_to.window(driver.window_handles[-1])

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="button"]'))
        ).click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "btn_gen_cmp"))
        ).click()

        print("\n Inicio de sesión exitoso y navegación completada. \n")

    except (TimeoutError, RuntimeError, ValueError) as e:
        showerror(title="Error", message="Fallo al iniciar sesión.")
        print(f"error: {e}")


def put_all_items(driver, products):
    """
    Ingresa una lista de productos en un formulario web usando Selenium.

    Args:
        driver (selenium.webdriver): El controlador de Selenium WebDriver.
        products (list): Lista de diccionarios con claves 'Product', 'Quantity', y 'Price'.
    """
    for index, product in enumerate(products, start=1):
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, f"detalle_descripcion{index}"))
        ).send_keys(product["Product"])

        quantity = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, f"detalle_cantidad{index}"))
        )
        quantity.clear()
        quantity.send_keys(product["Quantity"])
        detalleselect = Select(
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, f"detalle_medida{index}"))
            )
        )
        detalleselect.select_by_index(7)

        preciou = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, f"detalle_precio{index}"))
        )
        preciou.send_keys(product["Price"])
        if len(products) >= index + 1:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '//input[@type="button" and @value="Agregar línea descripción"]',
                    )
                )
            ).click()


def siguiente(driver):
    """
    Hace clic en el botón "Continuar" en la página actual del navegador.

    Args:
        driver (WebDriver): La instancia del controlador de Chrome.
    """
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@value="Continuar >"]'))
    ).click()


def esperar_descarga_completa(folder, timeout=20):
    """
    Espera hasta que no haya archivos .tmp o .crdownload en la carpeta de descargas.
    """
    start = time.time()
    while time.time() - start < timeout:
        if not any(f.endswith((".tmp", ".crdownload")) for f in os.listdir(folder)):
            print("[INFO] Descarga finalizada.")
            return True
        time.sleep(1)
    print("[ERROR] La descarga no se completó a tiempo.")
    return False


def realizar_operacion(driver, client_option, client_id, option, products, debug=False):
    """
    Realiza una operación de facturación en la página de ARCA.

    Args:
        driver (WebDriver): Controlador del navegador.
        client_option (int): Tipo de documento del cliente.
        client_id (str): Número de documento del cliente.
        option (int): Condición frente al IVA.
        products (list): Lista de productos.
        debug (bool): Si es True, no confirma ni descarga la factura.
    """
    progress = ProgressWindow(None, "Facturación")

    try:
        login(driver)

        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "novolveramostrar"))
            ).click()
            print("[INFO] Se clickeó novolveramostrar")
        except TimeoutException:
            print(
                "[INFO] El botón 'novolveramostrar' no apareció. Continuando sin hacer clic."
            )

        punto_venta = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "puntoDeVenta"))
        )
        Select(punto_venta).select_by_index(1)

        time.sleep(2)

        siguiente(driver)
        progress.set_progress(18)

        concepto = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "idconcepto"))
        )
        Select(concepto).select_by_index(1)

        siguiente(driver)
        progress.set_progress(25)

        condicion_iva = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "idivareceptor"))
        )
        Select(condicion_iva).select_by_index(option)
        progress.set_progress(30)

        tipo_doc = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "idtipodocreceptor"))
        )
        Select(tipo_doc).select_by_index(client_option)
        progress.set_progress(45)

        nro_doc = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "nrodocreceptor"))
        )
        nro_doc.send_keys(client_id)
        progress.set_progress(52)

        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "formadepago1"))
        ).click()
        progress.set_progress(60)

        siguiente(driver)

        put_all_items(driver, products)
        progress.set_progress(75)

        siguiente(driver)
        progress.set_progress(80)

        print("[INFO] Datos ingresados correctamente.")

        if not debug:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (
                        By.XPATH,
                        '//input[@type="button" and @value="Confirmar Datos..."]',
                    )
                )
            ).click()
            progress.set_progress(85)

            try:
                WebDriverWait(driver, 5).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                print(f"[ALERTA] {alert.text}")
                alert.accept()
            except TimeoutException:
                print("[INFO] No apareció ninguna alerta de confirmación.")

            # Clic en "Imprimir..."
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//input[@type="button" and @value="Imprimir..."]')
                )
            ).click()

            # Esperar la descarga
            esperar_descarga_completa(download_path)

            progress.set_progress(97)
        else:
            print("[DEBUG] Simulación activa: no se confirmó ni descargó la factura.")

    except (TimeoutError, RuntimeError, ValueError) as e:
        print(f"[ERROR] {type(e).__name__}: {e}")

    finally:
        progress.set_progress(100)
        driver.quit()
        progress.stop_progress()
        print("Operación completada. El navegador se ha cerrado.")
