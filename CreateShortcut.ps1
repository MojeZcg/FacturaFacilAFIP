param (
    [string]$TargetPath = "C:\Program Files (x86)\Factura Facil\FacturaFacilAFIP.exe",
    [string]$ShortcutPath = "$env:USERPROFILE\Desktop\Factura Facil.lnk",
    [string]$Arguments = ""
)

# Crear el objeto de shell
$shell = New-Object -ComObject WScript.Shell

# Crear el acceso directo
$shortcut = $shell.CreateShortcut($ShortcutPath)
$shortcut.TargetPath = $TargetPath
$shortcut.Arguments = $Arguments
$shortcut.WorkingDirectory = [System.IO.Path]::GetDirectoryName($TargetPath)
$shortcut.IconLocation = $TargetPath
$shortcut.Save()
