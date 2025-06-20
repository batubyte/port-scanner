#!/usr/bin/env python3

from rich.console import Console
from rich.panel import Panel
import subprocess
import platform
import argparse
import requests
import shutil
import sys
import os
import re

PROGRAM = "port_scanner"
DESCRIPTION = "An Nmap wrapper"
VERSION = "0.1.2"

console = Console()
error_console = Console(stderr=True, style="bold red")


def update():
    install_nmap(force=True)
    subprocess.run(["pipx", "install", "--force", "git+https://github.com/batubyte/port-scanner"], check=True)


def get_latest_nmap_url():
    url = "https://nmap.org/dist/"
    resp = requests.get(url)
    links = re.findall(r'href="(nmap-(\d+\.\d+)-setup\.exe)"', resp.text)
    if not links:
        return None
    latest = max(links, key=lambda x: tuple(map(int, x[1].split('.'))))
    return url + latest[0]


def install_nmap(force=False):
    if not force and shutil.which("nmap"):
        return
    
    if not force:
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
            error_console.print("No supported package manager found. Please install nmap manually.")
            sys.exit(1)

    elif system == "Windows":
        url = get_latest_nmap_url()
        if not url:
            error_console.print("Failed to find the latest Nmap installer URL.")
            sys.exit(1)

        tmp_dir = os.environ.get("TEMP", "/tmp")
        installer_path = os.path.join(tmp_dir, "nmap-setup.exe")

        console.print(f"Downloading Nmap from {url}")
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(installer_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

        subprocess.Popen(["start", "", installer_path], shell=True)
        console.print("Please complete the Nmap installation manually.")


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
        error_console.log(f"Error: {e}")
        sys.exit(1)
