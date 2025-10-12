from tkinter.messagebox import showwarning, showinfo
import ttkbootstrap as ttk
from utils.env import update_afip_key, refresh_env, getenv

from utils.helpers import center_window

from gui.history import History
from models.database import session
from models.downloads import download
from models.database import (
    Facturas,
)

ICON_PATH = "./static/arca.ico"

CONDITION_OPTIONS = [
    "Consumidor Final",
    "Iva Responsable Inscripto",
    "Iva Sujeto Excento",
]


class App:
    # pylint: disable=too-many-instance-attributes
    """
    Crea la clase de la aplicación.
    """

    def __init__(self, r):
        # pylint: disable=too-many-statements
        """
        Inicializa la interfaz de la aplicación.

        Args:
            root (ttk.Window): La instancia de la ventana raíz de tkinter.
        """
        self.root = r

        # Configuracion de la pestaña root
        self.root.title("Factura Fácil AFIP")
        self.root.resizable(False, False)
        self.root.iconbitmap(ICON_PATH)
        self.root.geometry("612x420")

        menu_bar = ttk.Menu(self.root)
        self.root.config(menu=menu_bar)

        config_menu = ttk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Descargar", menu=config_menu)
        config_menu.add_command(label="Descargar historial", command=download)

        config_menu1 = ttk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Configuración", menu=config_menu1)
        config_menu1.add_command(
            label="Actualizar Contraseña", command=self.show_update_window
        )

        self.client_options = ("CUIT", "CUIL", "DNI")
        self.client_var = ttk.StringVar(value=self.client_options[0])

        # Crear campos de entrada del id del cliente
        ttk.Label(r, text="Identificador del cliente:").place(x=10, y=10)
        self.client_type = ttk.OptionMenu(
            r,
            self.client_var,
            self.client_options[0],
            *self.client_options,
            bootstyle="dark",
        )
        self.client_type.place(x=10, y=32, width=75)

        self.client = ttk.StringVar()
        self.client.trace_add("write", self.format_client_id)

        self.client_entry = ttk.Entry(r, textvariable=self.client)
        self.client_entry.place(x=90, y=32, width=120)

        # Crear campo y opciones para el OptionMenu
        self.option_var = ttk.StringVar(value=CONDITION_OPTIONS[0])
        self.options = (
            CONDITION_OPTIONS[0],
            CONDITION_OPTIONS[1],
            CONDITION_OPTIONS[2],
        )

        ttk.Label(r, text="Condición frente al IVA:").place(x=220, y=10)
        self.option = ttk.OptionMenu(
            r,
            self.option_var,
            self.options[0],
            *self.options,
            command=self.update_client_options,
            bootstyle="dark",
        )
        self.option.place(x=220, y=32, width=200, height=30)
        # Llamar a update_client_options al inicio
        # para inicializar correctamente
        self.update_client_options(self.options[0])

        # Crear tabla
        self.tree = ttk.Treeview(
            r,
            bootstyle="dark",
            columns=("name", "quantity", "unique_price", "total_price"),
            show="headings",
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
            "Fotos Carnet",
            "Revelado de Fotos",
            "Servicio Laser",
            "Estampados",
        )

        ttk.Label(r, text="Nombre de producto:").place(x=10, y=265)
        self.name = ttk.Combobox(r, bootstyle="secondary", values=self.common_products)

        self.name.place(x=10, y=285, height=25, width=150)

        ttk.Label(r, text="Cantidad:").place(x=10, y=315)
        self.quantity = ttk.Entry(r, bootstyle="secondary")
        self.quantity.place(x=10, y=335, height=25, width=150)

        ttk.Label(r, text="Precio Unitario:").place(x=10, y=365)
        self.priceu = ttk.Entry(r, bootstyle="secondary")
        self.priceu.place(x=10, y=385, height=25, width=150)

        self.add_row_button = ttk.Button(
            r,
            bootstyle="default-outline",
            text="Agregar Producto",
            command=self.add_row,
        )

        self.add_row_button.place(x=180, y=313, width=140, height=28)

        self.remove_row_button = ttk.Button(
            r,
            bootstyle="danger-outline",
            text="Eliminar Seleccionados",
            command=self.delete_rows,
        )
        self.remove_row_button.place(x=180, y=348, width=140, height=28)

        self.remove_all_button = ttk.Button(
            r, bootstyle="dark", text="Eliminar Todos", command=self.delete_all_rows
        )
        self.remove_all_button.place(x=180, y=383, width=140, height=28)

        self.text_total = ttk.Label(r, bootstyle="dark", text="Total: 0$")
        self.text_total.place(x=395, y=272)

        # Botón para ejecutar las funciones de Selenium
        self.send_button = ttk.Button(
            r, bootstyle="success-outline", text="Facturar", command=self.send
        )
        self.send_button.place(x=485, y=270, width=120)

        self.history_button = ttk.Button(
            r, bootstyle="dark-outline", text="Ver Historial", command=self.history
        )
        self.history_button.place(x=485, y=310, width=120)

        self.error_label = ttk.Label(r, text="", bootstyle="danger")
        self.error_label.place(x=330, y=390)

        self.raw_client_id = ""

        center_window(self.root)

    def show_update_window(self):
        """
        Muestra una ventana para actualizar la clave AFIP_KEY.
        """

        def submit():
            """
            Obtiene el nuevo valor de la entrada y actualiza la clave AFIP_KEY.
            Muestra una advertencia si el campo está vacío y una notificación
            si la actualización es exitosa.
            """
            new_value = entry.get()
            if not new_value:
                showwarning("Advertencia", "El campo no puede estar vacío")
                return
            update_afip_key(new_value)
            showinfo("Éxito", "Cambiaste la contraseña de afip.")
            update_window.destroy()

        refresh_env()

        update_window = ttk.Toplevel(self.root)
        update_window.geometry("280x115")
        update_window.resizable(False, False)
        update_window.iconbitmap(ICON_PATH)
        update_window.title("Actualizar AFIP_KEY")

        ttk.Label(update_window, text="Contraseña actual: ").place(x=15, y=10)
        current_key = getenv("AFIP_KEY")
        ttk.Label(update_window, text=current_key, bootstyle="primary").place(
            x=130, y=10
        )

        ttk.Label(update_window, text="Nueva Contraseña:").place(x=15, y=40)
        entry = ttk.Entry(update_window, bootstyle="dark")
        entry.place(x=130, y=35)

        ttk.Button(update_window, text="Actualizar", command=submit).place(
            x=163, y=75, width=100
        )

    def obtener_valores_columna(self):
        """
        Obtiene los valores de una columna específica del widget 'tree'.

        Recorre todos los elementos del widget 'tree' y extrae los valores de la
        cuarta columna ('values')[3]. Luego, agrega estos valores a una lista y
        la devuelve.

        Returns:
            list: Una lista de valores de la cuarta columna de cada elemento del 'tree'.
        """
        valores = []
        for item_id in self.tree.get_children():
            valor_columna = self.tree.item(item_id, "values")[3]
            valores.append(valor_columna)
        return valores

    def actualizar_label(self):
        """
        Actualiza el texto de un label con la suma de los valores de una columna específica.

        Obtiene los valores de la cuarta columna de cada elemento del widget 'tree'
        usando la función 'obtener_valores_columna', los suma y actualiza el texto del
        widget 'text_total' para mostrar el total en dólares.
        """
        valores = self.obtener_valores_columna()
        resultado = 0
        for valor in valores:
            resultado += float(valor)
        self.text_total.config(text=f"Total: {resultado}$")

    def format_client_id(self, *args):
        """
        Formatea el ID del cliente en el formato 'XX-XXXXXXXX-X' para CUIT o CUIL.

        Dependiendo del tipo de cliente seleccionado (CUIT o CUIL), limpia y formatea
        el valor del ID del cliente ingresado en el campo de entrada. Mantiene la
        posición actual del cursor adecuada al nuevo formato.

        Args:
            *args: Argumentos adicionales que pueden ser pasados a la función, pero no
                se utilizan directamente.
        """
        client_var = self.client_var.get()
        cursor = self.client_entry.index(ttk.INSERT)
        if client_var in ("CUIT", "CUIL"):
            # Guardar la posición actual del cursor

            new_value = self.client.get()
            clean = "".join(filter(str.isdigit, new_value))

            # Formatear el valor limpio
            formatted_value = f"{clean[0:2]}-{clean[2:10]}-{clean[10:11]}"

            # Ajustar el valor del campo de entrada
            self.client.set(formatted_value)
            self.raw_client_id = clean

            # Calcular la nueva posición del cursor
            clean_cursor_position = sum(1 for c in new_value[:cursor] if c.isdigit())
            if clean_cursor_position <= 2:
                new_cursor = clean_cursor_position
            elif clean_cursor_position <= 10:
                new_cursor = clean_cursor_position + 1  # Compensar el primer guion
            else:
                new_cursor = clean_cursor_position + 2  # Compensar ambos guiones

            # Establecer la nueva posición del cursor
            self.client_entry.icursor(new_cursor)
            if not args:
                print("noargs")

    def update_client_options(self, selected_option):
        """
        Actualiza las opciones del identificador del cliente en función de la
        condición frente al IVA seleccionada.

        Args:
            selected_option (str): La condición frente al IVA seleccionada.
        """
        if selected_option in {CONDITION_OPTIONS[1], CONDITION_OPTIONS[2]}:
            new_client_options = ("CUIT",)
        else:  # Consumidor Final
            new_client_options = ("CUIT", "CUIL", "DNI")

        # Actualizar las opciones del primer OptionMenu
        menu = self.client_type["menu"]
        menu.delete(0, "end")  # pylint: disable=no-member

        for option in new_client_options:
            menu.add_command(  # pylint: disable=no-member
                label=option, command=lambda value=option: self.client_var.set(value)
            )

        # Establecer la opción predeterminada
        self.client_var.set(new_client_options[0])

    def add_row(self):
        """
        Agrega un producto a la tabla de productos.
        """
        if (
            self.name.get() == ""
            or self.quantity.get() == ""
            or self.priceu.get() == ""
        ):
            self.error_label.config(text="Error: Falta informacion en el producto")
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
                        total_price,
                    ),
                )

                self.name.delete(0, "end")
                self.quantity.delete(0, "end")
                self.priceu.delete(0, "end")
                self.error_label.config(text="")
                self.actualizar_label()
            except ValueError:
                self.error_label.config(
                    text="La Cantidad o el Precio Unitario no es un numero"
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

        if client_var == "CUIT":
            return 0

        if client_var == "CUIL":
            return 1

        if client_var == "DNI":
            return 6

        return -1

    def get_selected_option(self):
        """
        Obtiene el índice de la condición frente al IVA seleccionada.

        Returns:
            int: El índice de la condición frente al IVA seleccionada.
        """
        option_var = self.option_var.get()
        if option_var == CONDITION_OPTIONS[0]:
            return 3

        if option_var == CONDITION_OPTIONS[1]:
            return 1

        if option_var == CONDITION_OPTIONS[2]:
            return 2

        return -1

    def get_products(self):
        """
        Obtiene la lista de productos de la tabla de productos.

        Returns:
            list: La lista de productos.
        """

        if self.tree.get_children() != ():
            products = []
            for item in self.tree.get_children():
                item_data = self.tree.item(item, "values")

                filtered_products = [
                    [
                        value
                        for index, value in enumerate(item_data)
                        if self.tree["columns"][index] not in "total_price"
                    ]
                ]

                for item in filtered_products:
                    products.append(
                        {"Product": item[0], "Quantity": item[1], "Price": item[2]}
                    )
            return products

        self.error_label.config(text="Error: No hay productos")
        return None

    def validate_client_id(self) -> int | str:
        """
        Valida el identificador del cliente.

        Returns:
            str: El identificador del cliente si es válido.
            int: -1 si el identificador del cliente no es válido.
        """
        format_error = "El id del cliente (CUIT, CUIL o DNI) no es valido."

        client_id = self.raw_client_id
        client_type_var = self.client_var.get()

        if client_id == "":
            return client_id

        valid_lengths = {"CUIT": [10, 11], "CUIL": [10, 11], "DNI": [7, 8]}

        if client_type_var not in valid_lengths:
            return -1

        if len(client_id) not in valid_lengths[client_type_var]:
            self.error_label.config(text=format_error)
            return -1

        try:
            int(client_id)
            return client_id
        except ValueError:
            self.error_label.config(text=format_error)
            return -1

    def clear_all(self):
        """
        Limpia todos los campos de entrada y la tabla de productos.
        """
        self.delete_all_rows()
        self.raw_client_id = ""
        self.client_entry.delete(0, "end")
        self.name.delete(0, "end")
        self.quantity.delete(0, "end")
        self.priceu.delete(0, "end")
        self.error_label.config(text="")
        self.text_total.config(text="Total: 0$")

    def history(self):
        """_summary_"""
        History(self.root)

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

        if products:
            for product in products:
                price = float(product["Price"])
                quantity = float(product["Quantity"])
                totalvalue += price * quantity

        factura = Facturas(
            id_cliente=client_id,
            tipo_de_documento_id=client_option + 1,
            condicion_iva=option,
            productos=products,
            valor_total=totalvalue,
        )

        if client_option != -1 and option != -1 and client_id != -1 and products:
            session.add(factura)
            session.commit()

            in_thread(  # pylint: disable=undefined-variable
                client_option=client_option,
                client_id=client_id,
                option=option,
                products=products,
            )

            self.clear_all()
            session.close()
