#!/usr/bin/env python3

"""
Project: Port Scanner
Description: Async port scanner with Nmap support
Author: batubyte
Date: 2025-06-17
"""

import subprocess
import platform
import argparse
import asyncio
import shutil
import socket
import sys
import re

DESCRIPTION = "Async port scanner with Nmap support"
VERSION = "0.1.1"

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BOLD = "\033[1m"
RESET = "\033[0m"


def install_nmap():
    if shutil.which("nmap"):
        return

    answer = input("Nmap not found. Install? [Y/n]: ").strip().lower()
    if answer not in ("", "y", "yes"):
        sys.exit(1)

    system = platform.system()
    if system == "Linux":
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "install", "-y", "nmap"], check=True)
    elif system == "Windows":
        print("Install nmap from https://nmap.org/download.html#windows")
        print("Restart system after installation")
        sys.exit(1)

    if shutil.which("nmap") is None:
        print("Installation failed. Install nmap manually.")
        sys.exit(1)


def run_nmap(args):
    cmd = ["nmap"] + args
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    output = result.stdout

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


async def scan_port(host, port, sem):
    async with sem:
        try:
            reader, writer = await asyncio.open_connection(host, port)
            print(f"{port}/tcp open")
            writer.close()
            await writer.wait_closed()
        except:
            pass


async def full_scan(host):
    sem = asyncio.Semaphore(500)
    tasks = [scan_port(host, port, sem) for port in range(1, 65536)]
    try:
        await asyncio.gather(*tasks)
    except asyncio.CancelledError:
        pass


def valid_host(host):
    try:
        socket.gethostbyname(host)
        return True
    except socket.error:
        return False
    

def parse_args(parser):
    parser.add_argument("-v", "--version", action="version", version=VERSION)
    parser.add_argument("-n", nargs=argparse.REMAINDER, help="Run nmap")
    parser.add_argument("target", nargs="?", help="IP address, hostname or domain")
    return parser.parse_args()


def main():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    args = parse_args(parser)
        
    if args.n is not None:
        install_nmap()
        if len(args.n) == 0:
            subprocess.run(["nmap", "-h"])
        else:
            run_nmap(args.n)
    elif args.target and valid_host(args.target):
        asyncio.run(full_scan(args.target))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
