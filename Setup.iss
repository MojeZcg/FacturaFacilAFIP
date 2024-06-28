
[Setup]
AppName=Factura Facil
AppVersion=1.0.1
DefaultDirName={autopf}\Factura Facil
DefaultGroupName=Factura Facil

OutputBaseFilename=FacturaFacilSetup
; Archivo icono para el instalador
SetupIconFile=static\afip.ico
; Licencia (opcional)
LicenseFile=LICENSE
; No crear un grupo de acceso directo en el menú de inicio
DisableProgramGroupPage=yes
; No permitir modificar la ruta de instalación
DisableDirPage=yes

[Files]
; Archivos a incluir en el instalador
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Crear un acceso directo en el escritorio
Name: "{commondesktop}\Factura Facil"; Filename: "{app}\FacturaFacil.exe"; IconFilename: "{app}\static\afip.ico"

[Run]
; Ejecutar el programa al finalizar la instalación
Filename: "{app}\FacturaFacil.exe"; Description: "{cm:LaunchProgram,Factura Facil}"; Flags: nowait postinstall skipifsilent
