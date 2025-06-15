#!/usr/bin/env python3

"""
Project: Port Scanner
Description: Nmap wrapper for port scanning
Author: batubyte
Date: 2025-15-06
"""

import subprocess
import platform
import shutil
import sys
import re

VERSION = "0.1.0"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BOLD = "\033[1m"
RESET = "\033[0m"


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


def color_state(state):
    state = state.lower()
    if state == "open":
        return f"{GREEN}{state}{RESET}"
    elif state == "closed":
        return f"{RED}{state}{RESET}"
    elif state == "filtered":
        return f"{YELLOW}{state}{RESET}"
    else:
        return state


def print_output(output):
    ports_section = False
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("Nmap scan report for"):
            print(f"\n{CYAN}{line}{RESET}")
            ports_section = False
        elif line.startswith("PORT"):
            print(f"{BOLD}{line}{RESET}")
            ports_section = True
        elif ports_section and re.match(r"^\d+\/\w+\s", line):
            port, state, *rest = line.split()
            state_colored = color_state(state)
            service = rest[0] if rest else ""
            print(f"{port:10} {state_colored:10} {service}")
        else:
            print(line)


def nmap(args):
    cmd = ["nmap"] + args
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    print_output(result.stdout)


def main():
    try:
        install_nmap()
        if len(sys.argv) < 2:
            subprocess.run(["nmap", "-h"])
            sys.exit(0)
            
        nmap(sys.argv[1:])
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
