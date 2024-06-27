# Factura Fácil AFIP
## Descripción
#### FacturaFacilAFIP es una aplicación para emitir facturas electrónicas a través de los servicios web de la AFIP (Administración Federal de Ingresos Públicos de Argentina). Este proyecto tiene como objetivo simplificar la integración con los servicios de facturación electrónica de AFIP, permitiendo a los usuarios gestionar sus facturas de manera eficiente.

## Características
- Integración con Web Services de AFIP: Utiliza los servicios de WSFEv1 para emitir facturas electrónicas.
- Autenticación y autorización: Maneja el proceso de autenticación y autorización requerido por AFIP.
  

> [!IMPORTANT]
> ## Requisitos
> - Python 3.11 o superior
> - Las dependencias necesarias están detalladas en el archivo requirements.txt.
> 
> ## Instalación
> ### Clonar el repositorio:
> ```bash
> git clone https://github.com/MojeZcg/FacturaFacilAFIP.git
> ```
> 
> ### Navegar al directorio del proyecto:
> ```bash
> cd FacturaFacilAFIP
> ```
> ### Instalar las dependencias:
> ```bash
> pip install -r requirements.txt
> ```
> ### Uso:
> Configurar las credenciales de acceso de AFIP en el archivo de configuración .env.
> Ejecutar el script principal para emitir facturas:
> python emitir_factura.py


> [!NOTE]
> ## Contribuir
> 1. Hacer un fork del repositorio.
> 2. Crear una nueva rama con tu funcionalidad o corrección:
> ```bash
> git checkout -b nueva-funcionalidad
> ```
> 3. Hacer commit de los cambios:
> ```bash
> git commit -am 'Añadir nueva funcionalidad'
> ```
>
> 4. Push:
> ```bash
> git push origin nueva-funcionalidad
> ```
> 
> 5. Crear un Pull Request en GitHub.
> 
> ## Licencia
> #### Este proyecto está bajo la Licencia MIT. Para más detalles, ver el archivo LICENSE.

## Contacto
Para cualquier duda o sugerencia, puedes contactar al desarrollador principal a través del [correo electrónico](mailto:jesusmontenegro941@gmail.com).
