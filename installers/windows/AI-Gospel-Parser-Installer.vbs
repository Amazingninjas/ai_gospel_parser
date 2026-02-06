' ============================================================================
' AI Gospel Parser - Windows One-Click Installer Launcher
' ============================================================================
' This VBScript automatically elevates to Administrator and runs the installer
' User just needs to double-click this file
' ============================================================================

Option Explicit

Dim objShell, objFSO, strScriptPath, strPSScript, strCommand

' Get the directory where this VBS file is located
Set objFSO = CreateObject("Scripting.FileSystemObject")
strScriptPath = objFSO.GetParentFolderName(WScript.ScriptFullName)

' Path to the PowerShell installer script
strPSScript = strScriptPath & "\install-windows.ps1"

' Check if PowerShell script exists
If Not objFSO.FileExists(strPSScript) Then
    MsgBox "Error: Could not find install-windows.ps1" & vbCrLf & vbCrLf & _
           "Please make sure this file is in the same folder as:" & vbCrLf & _
           "install-windows.ps1", vbCritical, "AI Gospel Parser Installer"
    WScript.Quit 1
End If

' Create command to run PowerShell with elevation
strCommand = "powershell.exe -ExecutionPolicy Bypass -NoProfile -File """ & strPSScript & """"

' Execute with Administrator privileges (UAC prompt will appear)
Set objShell = CreateObject("Shell.Application")
objShell.ShellExecute "powershell.exe", _
                       "-ExecutionPolicy Bypass -NoProfile -File """ & strPSScript & """", _
                       strScriptPath, _
                       "runas", _
                       1  ' Show window

' Clean up
Set objShell = Nothing
Set objFSO = Nothing

WScript.Quit 0
