# Port Scanner
![image](https://github.com/user-attachments/assets/d987db90-aefd-4b9c-a828-7bfe7387e334)

## Installation
### Linux
```bash
cd ~/Documents
curl -o port_scanner.py https://raw.githubusercontent.com/batubyte/port-scanner/refs/heads/main/port_scanner.py
curl -LsSf https://astral.sh/uv/install.sh | sh
uv run port_scanner.py
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
