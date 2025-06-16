# Port Scanner

## Installation
### Linux
1. cd ~/Documents
2. curl -o port_scanner.py https://raw.githubusercontent.com/batubyte/port-scanner/refs/heads/main/port_scanner.py
3. curl -LsSf https://astral.sh/uv/install.sh | sh
4. uv run port_scanner.py
### Windows
1. Win + R -> cmd
2. cd %USERPROFILE%\Documents
3. curl -o port_scanner.py https://raw.githubusercontent.com/batubyte/port-scanner/refs/heads/main/port_scanner.py
4. powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
5. uv python install
6. uv run port_scanner.py

## Docs
https://nmap.org/book/man.html
