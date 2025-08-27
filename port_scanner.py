#!/usr/bin/env python3

import argparse
import os
import os.path
import platform
import re
import shutil
import signal
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from threading import Event
from typing import Iterable, Tuple
from urllib.request import urlopen

import requests
from rich.color import Color
from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

PROGRAM = "port-scanner"
DESCRIPTION = "An enhanced Nmap wrapper"
VERSION = "0.1.3"

console = Console()


def update():
    subprocess.run(
        ["pipx", "install", "--force", "git+https://github.com/batubyte/port-scanner"],
        check=True,
    )
    install_nmap(force=True)


def run_nmap(*nmap_args: str) -> None:
    cmd = ["nmap", *nmap_args]

    process = subprocess.run(cmd, capture_output=True, text=True)
    output = process.stdout + process.stderr

    section_headers = [
        r"TARGET SPECIFICATION:",
        r"HOST DISCOVERY:",
        r"SCAN TECHNIQUES:",
        r"PORT SPECIFICATION AND SCAN ORDER:",
        r"SERVICE/VERSION DETECTION:",
        r"SCRIPT SCAN:",
        r"OS DETECTION:",
        r"TIMING AND PERFORMANCE:",
        r"FIREWALL/IDS EVASION AND SPOOFING:",
        r"OUTPUT:",
        r"MISC:",
        r"EXAMPLES:",
        r"SEE THE MAN PAGE",
    ]

    for header in section_headers:
        output = re.sub(rf"(?m)^({header})", r"\n\1", output)

    text = Text(output)
    text.highlight_regex(r"\bopen\b", "green")
    text.highlight_regex(r"\bclosed\b", "red")
    text.highlight_regex(r"\bfiltered\b", "yellow")

    panel = Panel(
        text,
        border_style="dim",
        title=" ".join(cmd),
        title_align="left",
    )
    console.print(panel)


def get_nmap_url():
    url = "https://nmap.org/dist/"
    resp = requests.get(url)
    links = re.findall(r'href="(nmap-(\d+\.\d+)-setup\.exe)"', resp.text)
    if not links:
        return None
    latest = max(links, key=lambda x: tuple(map(int, x[1].split("."))))
    return url + latest[0]


def install_nmap(force=False):
    if not force and shutil.which("nmap"):
        return

    if not force:
        answer = input("Nmap not found. Install? [Y/n]: ").strip().lower()
        if answer not in ("", "y", "yes"):
            return

    system = platform.system()
    if system == "Linux":
        if shutil.which("apt-get"):
            subprocess.run(["apt-get", "update"], check=True)
            subprocess.run(["apt-get", "install", "-y", "nmap"], check=True)
        elif shutil.which("dnf"):
            subprocess.run(["dnf", "install", "-y", "nmap"], check=True)
        elif shutil.which("yum"):
            subprocess.run(["yum", "install", "-y", "nmap"], check=True)
        else:
            raise RuntimeError(
                "No supported package manager found. Please install Nmap manually."
            )

    elif system == "Windows":
        url = get_nmap_url()
        if not url:
            raise RuntimeError("Failed to find the latest Nmap installer URL.")

        tmp_dir = tempfile.gettempdir()
        filename = url.split("/")[-1]
        dest_path = os.path.join(tmp_dir, filename)

        downloader = Downloader()
        downloader.download([url], tmp_dir)

        console.print("Starting Nmap installer.")
        console.print("Please complete the installation manually.")
        subprocess.Popen(["start", "", dest_path], shell=True)

    elif system == "Darwin":  # macOS
        if shutil.which("brew"):
            subprocess.run(["brew", "install", "nmap"], check=True)
        else:
            raise RuntimeError("Homebrew not found. Please install Homebrew first.")


class Downloader:
    def __init__(self):
        self.progress = Progress(
            TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
        )
        self.done_event = Event()
        signal.signal(signal.SIGINT, self.handle_sigint)

    def handle_sigint(self, signum, frame):
        self.done_event.set()

    def copy_url(self, task_id: TaskID, url: str, path: str) -> None:
        """Copy data from a URL to a local file."""
        self.progress.console.log(f"Requesting {url}")
        response = urlopen(url)

        # This will break if the response doesn't contain content length
        try:
            total = int(response.info()["Content-length"])
        except (KeyError, TypeError):
            total = None  # Unknown total size

        self.progress.update(task_id, total=total)

        with open(path, "wb") as dest_file:
            self.progress.start_task(task_id)
            for data in iter(partial(response.read, 32768), b""):
                dest_file.write(data)
                self.progress.update(task_id, advance=len(data))
                if self.done_event.is_set():
                    return
        self.progress.console.log(f"Downloaded {path}")

    def download(self, urls: Iterable[str], dest_dir: str):
        """Download multiple files to the given directory."""
        with self.progress:
            with ThreadPoolExecutor(max_workers=4) as pool:
                for url in urls:
                    filename = url.split("/")[-1]
                    dest_path = os.path.join(dest_dir, filename)
                    task_id = self.progress.add_task(
                        "download", filename=filename, start=False
                    )
                    pool.submit(self.copy_url, task_id, url, dest_path)


class RichCLI:
    @staticmethod
    def blend_text(
        message: str, color1: Tuple[int, int, int], color2: Tuple[int, int, int]
    ) -> Text:
        """Blend text from one color to another."""
        text = Text(message)
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        dr = r2 - r1
        dg = g2 - g1
        db = b2 - b1
        size = len(text)
        for index in range(size):
            blend = index / size
            color = f"#{int(r1 + dr * blend):02X}{int(g1 + dg * blend):02X}{int(b1 + db * blend):02X}"
            text.stylize(color, index, index + 1)
        return text

    @staticmethod
    def print_help(parser: argparse.ArgumentParser) -> None:
        class OptionHighlighter(RegexHighlighter):
            highlights = [
                r"(?P<switch>\-\w)",
                r"(?P<option>\-\-[\w\-]+)",
            ]

        highlighter = OptionHighlighter()
        rich_console = Console(
            theme=Theme({"option": "bold cyan", "switch": "bold green"}),
            highlighter=highlighter,
        )

        console.print(
            f"\n[b]{PROGRAM}[/b] [magenta]v{VERSION}[/] 🔍\n[dim]{DESCRIPTION}\n",
            justify="center",
        )
        console.print(f"Usage: [b]{PROGRAM}[/b] [b][Options][/] [b cyan]<...>\n")

        table = Table(highlight=True, box=None, show_header=False)
        for action in parser._actions:
            if not action.option_strings:
                continue
            opts = [highlighter(opt) for opt in action.option_strings]
            help_text = Text(action.help or "")
            if action.metavar:
                opts[-1] += Text(f" {action.metavar}", style="bold yellow")
            table.add_row(*opts, help_text)

        rich_console.print(
            Panel(table, border_style="dim", title="Options", title_align="left")
        )

        footer_console = Console()
        footer_console.print(
            RichCLI.blend_text(
                "batubyte.github.io",
                Color.parse("#b169dd").triplet,
                Color.parse("#542c91").triplet,
            ),
            justify="right",
            style="bold",
        )


def main():
    parser = argparse.ArgumentParser(
        prog=PROGRAM, description=DESCRIPTION, add_help=False
    )
    parser.add_argument("-h", "--help", action="store_true", help="Show help message")
    parser.add_argument("-v", "--version", action="store_true", help="Show version")
    parser.add_argument(
        "-u", "--update", action="store_true", help="Update port-scanner and Nmap"
    )
    parser.add_argument("-n", "--nmap", nargs=argparse.REMAINDER, help="Run Nmap")

    if len(sys.argv) == 1 or sys.argv[1] in ("?", "-h", "--help"):
        RichCLI.print_help(parser)
        return

    args = parser.parse_args()

    if args.version:
        console.print(f"{PROGRAM} {VERSION}")
        return

    if args.update:
        update()

    if args.nmap is not None:
        install_nmap()
        run_nmap(*args.nmap)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console.print_exception(show_locals=False)
        sys.exit(1)
