#!/usr/bin/env python3

# Installation
## curl -o port_scanner.py https://example.com/path/to/file.py
## curl -LsSf https://astral.sh/uv/install.sh | sh
## uv run port_scanner.py

"""
Project: PortScanner
Description: Nmap wrapper for port scanning
Author: batubyte
Date: 2025-15-06
"""

import subprocess
import argparse
import textwrap
import platform
import shutil
import sys


VERSION = "0.1.0"


def install_nmap():
    if shutil.which("nmap") is not None:
        return

    answer = input("Nmap not found. Install now? [Y/n]: ").strip().lower()
    if answer not in ("", "y", "yes"):
        sys.exit(1)

    system = platform.system()
    if system == "Linux":
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "install", "-y", "nmap"], check=True)
    elif system == "Windows":
        print("Install nmap from https://nmap.org/download.html")
        print("Then restart your system.")
        sys.exit(1)

    if shutil.which("nmap") is None:
        print("Installation failed. Install nmap manually.")
        sys.exit(1)


def nmap(target: str, ports: str, timing: str = "4", aggressive: bool = False):
    cmd = ["nmap", target, "-T" + timing, "-v"]

    if aggressive:
        cmd.append("-A")
    if ports:
        cmd.extend(["-p", ports])

    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    print(result.stdout)


def parse_args():
    parser = argparse.ArgumentParser(epilog=textwrap.dedent("""
    examples:
        python3 port_scanner.py scanme.nmap.org
        python3 port_scanner.py 192.168.1.1 -p 22,80,443
        python3 port_scanner.py example.com -a -t 5
    """), formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("target", help="IP address or domain")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument("-p", "--ports", help="(e.g. 22,80,443 or 1-65535)")
    parser.add_argument("-t", "--timing", default="4", choices=["0", "1", "2", "3", "4", "5"],
                        help="(0=slow and stealthy, 5=fast and risky). Default: 4")
    parser.add_argument("-a", "--aggressive", action="store_true",
                        help="OS and service detection")
    return parser.parse_args()


def main():
    try:
        install_nmap()
        args = parse_args()
        nmap(args.target, ports=args.ports, timing=args.timing, aggressive=args.aggressive)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
