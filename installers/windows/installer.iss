; ============================================================================
; AI Gospel Parser - Inno Setup Installer Script
; ============================================================================
; Compile this script with Inno Setup (https://jrsoftware.org/isinfo.php)
; to create a professional Windows installer (.exe)
; ============================================================================

#define MyAppName "AI Gospel Parser"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Amazing Ninjas"
#define MyAppURL "https://github.com/Amazingninjas/ai_gospel_parser"
#define MyAppExeName "launch.bat"

[Setup]
; Basic app info
AppId={{8F3B5C2D-4E7A-4B9C-8D6E-1A2B3C4D5E6F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}/issues
AppUpdatesURL={#MyAppURL}/releases

; Installation directories
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

; Require Administrator privileges
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Output settings
OutputDir=output
OutputBaseFilename=AI-Gospel-Parser-Setup-{#MyAppVersion}
SetupIconFile=icon.ico
Compression=lzma2/max
SolidCompression=yes

; Modern UI
WizardStyle=modern
WizardImageFile=wizard-image.bmp
WizardSmallImageFile=wizard-small-image.bmp

; License and info files
LicenseFile=..\..\LICENSE
InfoBeforeFile=..\..\README.md
InfoAfterFile=post-install-info.txt

; Uninstall settings
UninstallDisplayIcon={app}\icon.ico

; Architecture
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Main installer scripts
Source: "..\..\portable-installation\install-windows.ps1"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\portable-installation\docker-compose.yml"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\portable-installation\.env.example"; DestDir: "{app}"; DestName: ".env"; Flags: ignoreversion
Source: "..\..\portable-installation\README-SMART-INSTALLER.txt"; DestDir: "{app}"; Flags: ignoreversion isreadme

; Launcher scripts
Source: "launch.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "stop.bat"; DestDir: "{app}"; Flags: ignoreversion

; Documentation
Source: "..\..\README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\..\CHANGELOG.md"; DestDir: "{app}"; Flags: ignoreversion

; Icon
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Start Menu shortcuts
Name: "{group}\{#MyAppName}"; Filename: "{app}\launch.bat"; IconFilename: "{app}\icon.ico"; Comment: "Start AI Gospel Parser"
Name: "{group}\Stop {#MyAppName}"; Filename: "{app}\stop.bat"; IconFilename: "{app}\icon.ico"; Comment: "Stop AI Gospel Parser"
Name: "{group}\Open in Browser"; Filename: "http://localhost:3000"; Comment: "Open AI Gospel Parser in browser"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"

; Desktop shortcut (optional)
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\launch.bat"; IconFilename: "{app}\icon.ico"; Tasks: desktopicon

[Run]
; Run the installer after setup
Filename: "{app}\install-windows.ps1"; Description: "Install and start AI Gospel Parser now"; Flags: postinstall shellexec skipifsilent runascurrentuser

[UninstallRun]
; Stop Docker containers before uninstall
Filename: "{app}\stop.bat"; Flags: runhidden

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  Result := True;

  // Check if Docker is installed
  if not Exec('docker', '--version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) or (ResultCode <> 0) then
  begin
    if MsgBox('Docker Desktop is not installed or not running.' + #13#10 + #13#10 +
              'AI Gospel Parser requires Docker Desktop to run.' + #13#10 + #13#10 +
              'Would you like to open the Docker Desktop download page?',
              mbConfirmation, MB_YESNO) = IDYES then
    begin
      ShellExec('open', 'https://www.docker.com/products/docker-desktop', '', '', SW_SHOW, ewNoWait, ResultCode);
    end;
    Result := False;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ResultCode: Integer;
begin
  if CurStep = ssPostInstall then
  begin
    // Create .env file from .env.example if it doesn't exist
    if not FileExists(ExpandConstant('{app}\.env')) then
    begin
      FileCopy(ExpandConstant('{app}\.env.example'), ExpandConstant('{app}\.env'), False);
    end;
  end;
end;
