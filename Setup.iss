[Setup]
AppName=MiFactura
AppVersion=1.0.0
AppVerName=MiFactura 1.0.0
DefaultDirName={autopf}\MiFactura
DefaultGroupName=MiFactura
AppPublisher=Walter Jesus Montenegro
AppPublisherURL=https://github.com/MojeZcg
OutputBaseFilename=MiFactura
SetupIconFile=static\arca.ico
LicenseFile=LICENSE
DisableProgramGroupPage=yes
DisableDirPage=yes
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin


[Files]
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\CreateShortcut.ps1"; DestDir: "{tmp}"; Flags: deleteafterinstall

[Run]
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{tmp}\CreateShortcut.ps1"""; Flags: runhidden
Filename: "{app}\MiFactura.exe"; Description: "{cm:LaunchProgram,MiFactura}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: "{app}\.env"
Type: filesandordirs; Name: "{app}\logs"
Type: files; Name: "{app}\CreateShortcut.ps1"
