<<<<<<< HEAD

=======
>>>>>>> 13ec7a9 (rework: Mejor distribucion del codigo)
# MiFactura

MiFactura es una aplicación para emitir facturas electrónicas a través de los servicios web de la AFIP (Administración Federal de Ingresos Públicos).

[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)

## Screenshots

<p align="center">
  <img src="screenshots/Screenshot_1.png" alt="Main App Screenshot" width="450">
  <img src="screenshots/Screenshot_2.png" alt="History window Screenshot" width="300">
</p>

## Como ejecutar localmente

Clone the project

```bash
  git clone git@github.com:MojeZcg/FacturaFacilAFIP.git
  cd FacturaFacilAFIP
```

Create an enviroment and activate it

```bash
  python -m venv venv
  .\venv\Scripts\activate
```
<<<<<<< HEAD
=======

>>>>>>> 13ec7a9 (rework: Mejor distribucion del codigo)
Or Linux or Mac.

```bash
  python -m venv venv
  source venv/bin/activate
```

Install dependencies

```bash
  pip install -r .\requirements.txt
```

Start the app (the database is created by running main.py)

```bash
  python main.py
```

<<<<<<< HEAD

=======
>>>>>>> 13ec7a9 (rework: Mejor distribucion del codigo)
## Como Desplegar

Para desplegar, debe generar un archivo .spec con pyinstaller

```bash
<<<<<<< HEAD
  pyinstaller --onefile --name FacturaFacilAfip --icon=static/afip.ico --add-data ".env:." --add-data "static:static" --add-data "LICENSE:." main.py
```


=======
  pyinstaller --onefile --name FacturaFacilAfip --icon=static/arca.ico --add-data ".env:." --add-data "static:static" --add-data "LICENSE:." main.py
```

>>>>>>> 13ec7a9 (rework: Mejor distribucion del codigo)
## Variables de entorno

Para ejecutar este proyecto, deberá agregar las siguientes variables de entorno a su archivo .env. O use el .iss para crear la configuración.

`AFIP_CUIL`

`AFIP_KEY`

`DOWNLOAD_PATH`

<<<<<<< HEAD
`DRIVER_PATH`


=======
>>>>>>> 13ec7a9 (rework: Mejor distribucion del codigo)
## Ejecutar Lint

Para ejecutar el lint, instale las dependencias y pylint.

```bash
  pip -r requirements.txt
  pip install pylint
```

luego ejecuta pylint.

```bash
  pylint **/*.py
```

<<<<<<< HEAD

=======
>>>>>>> 13ec7a9 (rework: Mejor distribucion del codigo)
## Contribuciones

¡Las contribuciones siempre son bienvenidas!

Consulte `contributing.md` para conocer las formas de contribuir.

Siga el `code of conduct` de este proyecto.

#### Para empezar:
<<<<<<< HEAD
1. Hacer un fork del repositorio.
2. Crear una nueva rama con tu funcionalidad o corrección:
```bash
git checkout -b nueva-funcionalidad
```
3. Hacer commit de los cambios:
=======

1. Hacer un fork del repositorio.
2. Crear una nueva rama con tu funcionalidad o corrección:

```bash
git checkout -b nueva-funcionalidad
```

3. Hacer commit de los cambios:

>>>>>>> 13ec7a9 (rework: Mejor distribucion del codigo)
```bash
git commit -am 'Añadir nueva funcionalidad'
```

4. Push:
<<<<<<< HEAD
=======

>>>>>>> 13ec7a9 (rework: Mejor distribucion del codigo)
```bash
git push origin nueva-funcionalidad
```

5. Crear un Pull Request en GitHub.

<<<<<<< HEAD

## Licencia
=======
## Licencia

>>>>>>> 13ec7a9 (rework: Mejor distribucion del codigo)
#### Este proyecto está bajo la Licencia [GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text). Para más detalles, ver el archivo [LICENSE](LICENSE).
