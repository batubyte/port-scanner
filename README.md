# Port Scanner

![image](https://github.com/user-attachments/assets/d987db90-aefd-4b9c-a828-7bfe7387e334)

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
5. set Path=%USERPROFILE%\.local\bin;%Path%
6. uv python install
7. uv run port_scanner.py

## Docs
https://nmap.org/book/man.html
