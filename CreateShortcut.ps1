param (
<<<<<<< HEAD
    [string]$TargetPath = "C:\Program Files (x86)\Factura Facil\FacturaFacilAFIP.exe",
    [string]$ShortcutPath = "$env:USERPROFILE\Desktop\Factura Facil.lnk",
=======
    [string]$TargetPath = "C:\Program Files (x86)\MiFactura\MiFactura.exe",
    [string]$ShortcutPath = "$env:USERPROFILE\Desktop\MiFactura.lnk",
>>>>>>> 13ec7a9 (rework: Mejor distribucion del codigo)
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
