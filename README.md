# Port Scanner
![image](https://github.com/user-attachments/assets/d84cc929-ec5d-416b-aab8-5622eadbe513)

## Installation
### Linux (Ubuntu/Debian)
```bash
sudo apt update && sudo apt install -y git
curl -LsSf https://astral.sh/uv/install.sh | sh
cd ~/Documents
git clone https://github.com/batubyte/port-scanner.git
```
### Windows
```batch
Win + R -> cmd
winget install --id=Git.Git -e
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
set Path=%USERPROFILE%\.local\bin;%Path%
cd %USERPROFILE%\Documents
git clone https://github.com/batubyte/port-scanner.git
```

## Run
### Linux
```bash
cd ~/Documents/port-scanner
uv sync
uv run port_scanner.py
```
### Windows
```batch
Win + R -> cmd
cd %USERPROFILE%\Documents\port-scanner
uv sync
uv run port_scanner.py
```

## Nmap docs
https://nmap.org/book/man.html
