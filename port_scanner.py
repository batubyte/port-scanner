#!/usr/bin/env python3

from rich.console import Console
from rich.panel import Panel
import subprocess
import platform
import argparse
import shutil
import sys
import re

PROGRAM = "port_scanner"
DESCRIPTION = "An Nmap wrapper"
VERSION = "0.1.2"

console = Console()
error_console = Console(stderr=True, style="bold red")


def update():
    install_nmap()
    subprocess.run(["pipx", "install", "--force", "git+https://github.com/batubyte/port-scanner"], check=True)


def install_nmap():
    if shutil.which("nmap"):
        return

    answer = input("Nmap not found. Install? [Y/n]: ").strip().lower()
    if answer not in ("", "y", "yes"):
        sys.exit(1)

    system = platform.system()
    if system == "Linux":
        if shutil.which("apt-get"):
            subprocess.run(["sudo", "apt-get", "update"], check=True)
            subprocess.run(["sudo", "apt-get", "install", "-y", "nmap"], check=True)
        elif shutil.which("dnf"):
            subprocess.run(["sudo", "dnf", "install", "-y", "nmap"], check=True)
        elif shutil.which("yum"):
            subprocess.run(["sudo", "yum", "install", "-y", "nmap"], check=True)
        else:
            console.print("No supported package manager found. Install nmap manually.", style="bold red")
            sys.exit(1)

    elif system == "Windows":
        # install nmap sliently
        sys.exit(1)

    if shutil.which("nmap") is None:
        console.print("Installation failed. Install nmap manually.", style="bold red")
        sys.exit(1)


def run_nmap(args):
    cmd = ["nmap"] + args
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    output = result.stdout.strip()

    colored_output = []
    for line in output.splitlines():
        line = re.sub(r"\bopen\b", "[green]open[/]", line)
        line = re.sub(r"\bclosed\b", "[red]closed[/]", line)
        line = re.sub(r"\bfiltered\b", "[yellow]filtered[/]", line)
        colored_output.append(line)

    styled_output = "\n".join(colored_output)

    console.print(
        Panel(
            styled_output,
            title="nmap " + " ".join(args),
            border_style="cyan"
        )
    )


def parse_args(parser):
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s version {VERSION}"
    )
    parser.add_argument("-h", "--help", action="store_true", help="show this help message")
    parser.add_argument("-u", "--update", action="store_true", help="update nmap and this program")
    parser.add_argument("-n", "--nmap", nargs=argparse.REMAINDER, help="run nmap with custom arguments")
    return parser.parse_args()


def main():
    parser = argparse.ArgumentParser(prog=PROGRAM, description=DESCRIPTION, add_help=False)
    args = parse_args(parser)
    
    if len(sys.argv) == 1 or args.help:
        console.print(
            Panel(
                parser.format_help(),
                title=' '.join(sys.argv),
                border_style="cyan",
            )
        )
        return
    
    if args.update:
        update()

    if args.nmap is not None:
        install_nmap()
        if len(args.nmap) == 0:
            run_nmap(["--help"])
        else:
            run_nmap(args.nmap)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        error_console.print(f"Error: {e}")
        sys.exit(1)
