#!/usr/bin/env python3

"""
Project: Port Scanner
Description: Installs and runs nmap with colored scan results.
Author: batubyte
Date: 2025-15-06
"""

import subprocess
import platform
import shutil
import sys
import re

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


def print_output(output):
    ports_section = False
    for line in output.splitlines():
        line = line.strip()

        state_colored = None
        if ports_section and re.match(r"^\d+\/\w+\s", line):
            port, state, *rest = line.split()
            state_lower = state.lower()
            if state_lower == "open":
                state_colored = f"{GREEN}{state}{RESET}"
            elif state_lower == "closed":
                state_colored = f"{RED}{state}{RESET}"
            elif state_lower == "filtered":
                state_colored = f"{YELLOW}{state}{RESET}"
            else:
                state_colored = state

            service = rest[0] if rest else ""
            print(f"{port:10} {state_colored:10} {service}")
        elif line.startswith("Nmap scan report for"):
            print(f"\n{CYAN}{line}{RESET}")
            ports_section = False
        elif line.startswith("PORT"):
            print(f"{BOLD}{line}{RESET}")
            ports_section = True
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


if __name__ == "__main__":
    main()
