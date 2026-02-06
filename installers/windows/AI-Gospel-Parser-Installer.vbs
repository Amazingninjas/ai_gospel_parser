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

' Create PowerShell command that will keep window open even on error
' Using -Command instead of -File to have better control
strCommand = "-ExecutionPolicy Bypass -NoProfile -Command """ & _
             "Set-Location '" & strScriptPath & "'; " & _
             "try { " & _
             "  & '" & strPSScript & "' " & _
             "} catch { " & _
             "  Write-Host 'Error occurred:' -ForegroundColor Red; " & _
             "  Write-Host $_.Exception.Message -ForegroundColor Red; " & _
             "  Write-Host ''; " & _
             "  Write-Host 'Press any key to exit...' -ForegroundColor Yellow; " & _
             "  $null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown') " & _
             "}"""

' Execute with Administrator privileges (UAC prompt will appear)
Set objShell = CreateObject("Shell.Application")
objShell.ShellExecute "powershell.exe", _
                       strCommand, _
                       strScriptPath, _
                       "runas", _
                       1  ' Show window (1 = normal, not hidden)

' Clean up
Set objShell = Nothing
Set objFSO = Nothing

' VBScript exits, PowerShell continues running
WScript.Quit 0
