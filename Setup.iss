
[Setup]
AppName=Factura Facil
AppVersion=1.0.1

DefaultDirName={autopf}\Factura Facil
DefaultGroupName=Factura Facil

OutputBaseFilename=FacturaFacilSetup

SetupIconFile=static\afip.ico
LicenseFile=LICENSE

DisableProgramGroupPage=yes
DisableDirPage=yes

[Files]
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{commondesktop}\Factura Facil"; Filename: "{app}\FacturaFacil.exe"; IconFilename: "{app}\static\afip.ico"

[Run]
Filename: "{app}\FacturaFacil.exe"; Description: "{cm:LaunchProgram,Factura Facil}"; Flags: nowait postinstall skipifsilent
