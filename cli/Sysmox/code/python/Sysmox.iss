[Setup]
AppId={{A7B8C9D0-E1F2-4A3B-8C9D-0E1F2A3B4C5D}
AppName=Sysmox
AppVersion=0.2.0

AppPublisher=Sysmox
AppPublisherURL=https://github.com/ProgramerXYZ/Sysmox-releses
AppSupportURL=https://github.com/ProgramerXYZ/Sysmox-releses
AppUpdatesURL=https://github.com/ProgramerXYZ/Sysmox-releses

DefaultDirName={autopf}\Sysmox
DefaultGroupName=Sysmox

OutputBaseFilename=Sysmox-Installer
Compression=lzma
SolidCompression=yes
PrivilegesRequired=admin

; 🎨 ICON / BRANDING
SetupIconFile=logo.ico
UninstallDisplayIcon={app}\sysmox.exe

; 📄 PRIVACY POLICY (FORCES ACCEPTANCE)
LicenseFile=PRIVACY_POLICY.txt


[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"


[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "noreconfig"; Description: "Skip initial configuration"; GroupDescription: "Configuration:"; Flags: unchecked


[Files]
Source: "dist\sysmox\sysmox.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\sysmox\_internal\*"; DestDir: "{app}\_internal"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "PRIVACY_POLICY.txt"; DestDir: "{app}"; Flags: ignoreversion


[Icons]
Name: "{group}\Sysmox"; Filename: "{app}\sysmox.exe"
Name: "{group}\{cm:UninstallProgram,Sysmox}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Sysmox"; Filename: "{app}\sysmox.exe"; Tasks: desktopicon


[Registry]
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; \
    ValueType: expandsz; ValueName: "Path"; \
    ValueData: "{olddata};{app}"; \
    Check: NeedsAddPath


[Run]
Filename: "{app}\sysmox.exe"; Parameters: "reconfig"; \
    Flags: nowait runhidden; Check: not WizardIsTaskSelected('noreconfig')


[Code]
const
  WM_SETTINGCHANGE = $001A;
  SMTO_ABORTIFHUNG = $0002;

function SendMessageTimeout(
  hWnd: HWND;
  Msg: Integer;
  wParam: Integer;
  lParam: string;
  flags: Integer;
  timeout: Integer;
  var lpdwResult: DWORD
): Integer;
  external 'SendMessageTimeoutW@user32.dll stdcall';

function NeedsAddPath(): Boolean;
var
  Paths: string;
begin
  if RegQueryStringValue(
    HKLM,
    'SYSTEM\CurrentControlSet\Control\Session Manager\Environment',
    'Path',
    Paths
  ) then
    Result := Pos(ExpandConstant('{app}'), Paths) = 0
  else
    Result := True;
end;

procedure RefreshEnvironment;
var
  MsgResult: DWORD;
begin
  SendMessageTimeout(
    HWND_BROADCAST,
    WM_SETTINGCHANGE,
    0,
    'Environment',
    SMTO_ABORTIFHUNG,
    5000,
    MsgResult
  );
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  PolicyText: AnsiString;
  AcceptanceText: AnsiString;
  OutputFile: string;
begin
  if CurStep = ssInstall then
  begin
    if FileExists(ExpandConstant('{src}\PRIVACY_POLICY.txt')) then
    begin
      LoadStringFromFile(
        ExpandConstant('{src}\PRIVACY_POLICY.txt'),
        PolicyText
      );

      AcceptanceText :=
        PolicyText + #13#10 + #13#10 +
        '------------------------------------------------------------' + #13#10 +
        'PRIVACY POLICY ACCEPTANCE' + #13#10 + #13#10 +
        'The user confirms that they have read and accepted the above ' +
        'Privacy Policy in its entirety, without modification.' + #13#10 +
        'Acceptance Date: ' +
        GetDateTimeString('yyyy-mm-dd hh:nn:ss', '-', ':') + #13#10;

      OutputFile := ExpandConstant('{app}\privacy_policy_acceptance.txt');
      SaveStringToFile(OutputFile, AcceptanceText, False);
    end;
  end;

  if CurStep = ssPostInstall then
  begin
    RefreshEnvironment;
  end;
end;
