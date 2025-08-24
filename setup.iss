[Setup]
AppName=Passport Photo Extractor
AppVersion=1.0
AppPublisher=Kasim K
DefaultDirName={pf}\PassportPhotoExtractor
DefaultGroupName=Passport Photo Extractor
OutputBaseFilename=PassportPhotoExtractorSetup
Compression=lzma
SolidCompression=yes

[Files]
; PyInstaller produces dist\main.exe, include it
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\Passport Photo Extractor"; Filename: "{app}\main.exe"
Name: "{commondesktop}\Passport Photo Extractor"; Filename: "{app}\main.exe"

[Run]
Filename: "{app}\main.exe"; Description: "Launch Passport Photo Extractor"; Flags: nowait postinstall skipifsilent
