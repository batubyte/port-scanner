# Port Scanner
![image](https://github.com/user-attachments/assets/32276a99-882b-473a-b707-bd03625a8e03)

## 🪟 Windows
#### 📦 Installation
```batch
::Install WinGet
::Do Win + X -> A
Start-BitsTransfer -Source https://aka.ms/getwinget -Destination AppInstaller.msixbundle; Add-AppxPackage .\AppInstaller.msixbundle; Remove-Item .\AppInstaller.msixbundle

::Install Git
winget install --id=Git.Git -e --accept-package-agreements --accept-source-agreements

::Install uv
::Do Win + R -> cmd
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" && setx Path=%USERPROFILE%\.local\bin;%Path%

:: Install project
rmdir /s /q "%USERPROFILE%\Documents\port-scanner" & git clone https://github.com/batubyte/port-scanner.git "%USERPROFILE%\Documents\port-scanner"
```
#### ▶️ Run
```batch
::Win + R -> cmd
cd %USERPROFILE%\Documents\port-scanner
uv sync & uv run port_scanner.py
```

## 🐧 Linux (Ubuntu/Debian)
#### 📦 Installation
```bash
sudo apt update && sudo apt install -y git
curl -LsSf https://astral.sh/uv/install.sh | sh
rm -rf ~/Documents/port-scanner && git clone https://github.com/batubyte/port-scanner.git ~/Documents/port-scanner
```
#### ▶️ Run
```bash
cd ~/Documents/port-scanner
uv sync && uv run port_scanner.py
```


## Nmap docs
https://nmap.org/book/man.html
