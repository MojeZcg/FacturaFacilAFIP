[Setup]
AppName=Factura Facil
AppVersion=2.1.0
DefaultDirName={pf}\Factura Facil
DefaultGroupName=Factura Facil
OutputBaseFilename=FacturaFacilSetup
SetupIconFile=static\afip.ico
LicenseFile=LICENSE
DisableProgramGroupPage=yes
DisableDirPage=yes

[Files]
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\CreateShortcut.ps1"; DestDir: "{tmp}"; Flags: deleteafterinstall

[Run]
Filename: "powershell.exe"; Parameters: "-ExecutionPolicy Bypass -File ""{tmp}\CreateShortcut.ps1"""; Flags: runhidden
Filename: "{app}\FacturaFacilAFIP.exe"; Description: "{cm:LaunchProgram,Factura Facil}"; Flags: nowait postinstall skipifsilent

[Code]
var
  DownloadPathPage: TInputDirWizardPage;
  CredentialsPage: TInputQueryWizardPage;

procedure InitializeWizard();
begin
  DownloadPathPage := CreateInputDirPage(wpSelectDir, 'Carpeta de Descarga', 
    'Seleccione la carpeta donde desea descargas de las facturas:', 
    'Por favor seleccione la carpeta donde se guardarán las facturas descargadas:', False, 'Facturas');
  DownloadPathPage.Add('');

  CredentialsPage := CreateInputQueryPage(wpSelectComponents, 
    'Credenciales AFIP', 'Introduzca sus credenciales de AFIP:', 
    'Por favor introduzca su Cuil y clave para continuar:');
  CredentialsPage.Add('&Cuil o Cuit:', False);
  CredentialsPage.Add('&Clave:', True);
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  EnvFile: TStringList;
  EnvFilePath: string;
begin
  if CurStep = ssPostInstall then
  begin
    EnvFilePath := ExpandConstant('{app}\.env');
    EnvFile := TStringList.Create;
    try
      if FileExists(EnvFilePath) then
        // Update or add new environment variables
        if DownloadPathPage.Values[0] <> '' then
          EnvFile.Add('DOWNLOAD_PATH=' + DownloadPathPage.Values[0]);
        if CredentialsPage.Edits[0].Text <> '' then
          EnvFile.Add('AFIP_CUIL=' + CredentialsPage.Edits[0].Text);
        if CredentialsPage.Edits[1].Text <> '' then
          EnvFile.Add('AFIP_KEY=' + CredentialsPage.Edits[1].Text);
        EnvFile.Add('DRIVER_PATH=' + './static/chromedriver.exe');
          
        EnvFile.SaveToFile(EnvFilePath);
      
    finally
      EnvFile.Free;
    end;
  end;
end;
