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
cd %USERPROFILE%\Documents
curl -o port_scanner.py https://raw.githubusercontent.com/batubyte/port-scanner/refs/heads/main/port_scanner.py
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
set Path=%USERPROFILE%\.local\bin;%Path%
uv python install
uv run port_scanner.py
```

## Nmap docs
https://nmap.org/book/man.html
