$CD = Get-Location
$CD = $CD.Path
$WScriptShell = New-Object -ComObject Wscript.Shell
$Shortcut = $WScriptShell.CreateShortcut(“$Env:USERPROFILE\Desktop\junting.lnk”)
$Shortcut.IconLocation = “$CD\app.ico”
$Shortcut.TargetPath = “$CD\junting.cmd”
$Shortcut.WorkingDirectory = “$CD”
$Shortcut.save()