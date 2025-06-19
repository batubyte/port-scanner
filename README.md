# 🛜 Port Scanner
![image](https://github.com/user-attachments/assets/32276a99-882b-473a-b707-bd03625a8e03)

## 📦 Install
### Linux (Ubuntu/Debian)
```bash
sudo apt update && sudo apt install -y git
curl -LsSf https://astral.sh/uv/install.sh | sh && export PATH="$HOME/.local/bin:$PATH"
rm -rf ~/Documents/port-scanner && git clone https://github.com/batubyte/port-scanner.git ~/Documents/port-scanner && chmod +x ~/Documents/port-scanner/port_scanner.py
```
### Windows
```batch
:: WinGet
:: do Win + X -> A
Start-BitsTransfer -Source https://aka.ms/getwinget -Destination AppInstaller.msixbundle; Add-AppxPackage .\AppInstaller.msixbundle; Remove-Item .\AppInstaller.msixbundle

:: Git
winget install --id=Git.Git -e --accept-package-agreements --accept-source-agreements

:: uv
:: do Win + R -> cmd
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex" && setx Path=%USERPROFILE%\.local\bin;%Path%

:: Repository
rmdir /s /q "%USERPROFILE%\Documents\port-scanner" & git clone https://github.com/batubyte/port-scanner.git "%USERPROFILE%\Documents\port-scanner"
```

## ⚡ Run
### Linux
```bash
cd ~/Documents/port-scanner
 uv sync && uv run port_scanner.py -h
```
### Windows
```batch
:: do Win + R -> cmd
cd %USERPROFILE%\Documents\port-scanner
uv sync & uv run port_scanner.py -h
```

## 📚 Nmap manual
https://nmap.org/book/man.html
