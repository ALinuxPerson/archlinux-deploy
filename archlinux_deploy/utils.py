#  archlinux-deploy - Deploys a VirtualBox Arch Linux VM automatically.
#  Copyright (C) 2020  ALinuxPerson
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
from typing import Any, Dict, List
from rich import print
import platform
import os

def colored_output(message: Any, level: str):
    levels: Dict[str, str] = {
        "info": "[bold blue]🛈 ",
        "warn": "[bold yellow]⚠ ",
        "success": "[bold green]✔ ",
        "error": "[bold red]✗ "
    }

    to_print: List[str] = str(message).splitlines()

    for line in to_print:
        print(f"{levels[level]}{line}")

def in_path_env(file: str) -> bool:
    PATH: List[str] = os.environ["PATH"].split(";" if platform.system() == "Windows" else ":")

    for path in PATH:
        file_path: str = os.path.join(os.path.sep, path, file)
        if os.path.exists(file_path) and os.path.isfile(file_path) and os.access(file_path, os.X_OK):
            return True
        continue
    else:
        return False

def bytes_to_string(byte_object: bytes) -> str:
    return byte_object.decode("utf-8")

def is_posix() -> bool:
    try:
        import posix
        return True
    except ModuleNotFoundError:
        return False
