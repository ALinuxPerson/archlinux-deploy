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
from archlinux_deploy.stages.exceptions import BaseStageException  # type: ignore
from archlinux_deploy import utils
from typing import List, Callable
from bs4 import BeautifulSoup  # type: ignore
from rich import print
import subprocess
import requests
import os

def check_for_virtualbox():
    print("[blue]Checking if virtualbox is installed...")
    if not utils.in_path_env("virtualbox"):
        raise BaseStageException(
            "It seems like virtualbox isn't installed.\n"
            "Either install it from the website if you're using Windows, install it from the app store if you're running Mac,\n"
            "or install it using your distribution's package manager if you're using FreeBSD or Linux."
        )
    print("[blue]It is.")

def check_for_vboxapi():
    try:
        print("[blue]Checking if module 'vboxapi' is installed...")
        import vboxapi  # type: ignore
        print("[blue]It is.")
    except ModuleNotFoundError:
        raise BaseStageException("It seems like vboxapi isn't installed as a python module.\n"
                                 "Here is the following fix:\n\n"
                                 "1. Go to this link: https://www.virtualbox.org/wiki/Downloads\n"
                                 "2. Go to the header: VirtualBox x.x.xx Software Developer Kit (SDK)\n"
                                 "3. Click on the link that says 'All platforms'\n"
                                 "4. Download the zip file.\n"
                                 "5. Extract the zip file.\n"
                                 "6. Go to the extracted location, then go to the 'installer' folder.\n"
                                 "7. Open up a terminal in the directory (if on Windows, open cmd as admin).\n"
                                 "8.1. If on a POSIX-based distribution (e.g. Linux, Darwin, FreeBSD) type this:\n"
                                 "'$ sudo python vboxapisetup.py install'\n"
                                 "8.2. If on a Windows system, type this:\n"
                                 "'python vboxapisetup.py install'", "error") from None

def check_for_xpcom():
    try:
        print("[blue]Checking if module 'xpcom' is installed...")
        import xpcom  # type: ignore
        print("[blue]It is.")
    except ModuleNotFoundError:
        raise BaseStageException(
            "It seems like xpcom isn't in the PYTHONPATH.\n"
            "Assuming that vboxapi is installed, this means that you need to add <SDK_INSTALL_LOCATION>/bindings/xpcom/python to PYTHONPATH.\n"
            "Here's what you need to do:\n\n"
            "1.1. If on a POSIX based distribution (e.g. Linux, Darwin, FreeBSD) add this to your .<SHELL>rc:\n"
            "'''<SHELL>\n"
            "export VBOX_INSTALL_PATH=/usr/lib/virtualbox\n"
            "export VBOX_SDK_PATH=<SDK_INSTALL_LOCATION>\n"
            "export PYTHONPATH=<SDK_INSTALL_LOCATION>/bindings/xpcom/python\n"
            "'''\n"
        )

def download_latest_iso():
    arch_linux_website: str = "http://mirror.rackspace.com/archlinux/iso/latest/"
    page: str = requests.get(arch_linux_website).text
    soup: BeautifulSoup = BeautifulSoup(page, "html.parser")
    all_isos: List[str] = [arch_linux_website + "/" + node.get("href") for node in soup.find_all("a") if node.get("href").endswith("iso")]
    if os.path.exists("./arch-linux.iso"):
        print("[blue]ISO seems to be already downloaded, continuing...")
        return
    with open("./arch-linux.iso", "wb") as iso:
        response: requests.Response = requests.get(all_isos[0], stream=True)
        print("[blue]Writing Arch Linux ISO to disk...")
        for data in response.iter_content(chunk_size=1024):
            iso.write(data)

def vbox_manage_command() -> str:
    if utils.in_path_env("vboxmanage" if utils.is_posix() else "vboxmanage.exe"):
        return "vboxmanage" if utils.is_posix() else "vboxmanage.exe"
    elif utils.in_path_env("VboxManage" if utils.is_posix() else "VboxManage.exe"):
        return "VboxManage" if utils.is_posix() else "VboxManage.exe"
    else:
        raise BaseStageException(
            "It seems like the vboxmanage command isn't in PATH. Either check in /usr/lib/virtualbox or C:\\Program Files\\Virtualbox"
        )

def sp_call(command: str, accepted_return_codes: List[int] = None, ignore_return_code: bool = False):
    if accepted_return_codes is None:
        accepted_return_codes = [0]
    called = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    called.wait()  # needed so that the we'll get the return code
    stdout, stderr = called.communicate()
    return_code: int = called.returncode
    if return_code not in accepted_return_codes and not ignore_return_code:
        raise BaseStageException(
            f"Return code of command is {return_code} (not successful).\n"
            f"Command passed: '{command}'\n"
            f"Standard Output (stdout):\n"
            f"{utils.bytes_to_string(stdout) or '(empty)'}\n"
            f"Standard Error (stderr):\n"
            f"{utils.bytes_to_string(stderr) or '(empty)'}"
        )
    return return_code

def run():
    stages: List[Callable] = [check_for_virtualbox, check_for_vboxapi, check_for_xpcom, download_latest_iso]
    for stage in stages:
        stage_name: str = stage.__name__
        utils.colored_output(f"Stage 1 Substage {stage_name} started!", "info")
        try:
            stage()
        except BaseStageException as error:
            message = error.args[0]
            utils.colored_output(f"Stage 1 Substage {stage_name} FAILED:", "error")
            utils.colored_output(message, "error")
            return
        utils.colored_output(f"Stage 1 Substage {stage_name} completed!", "success")
    utils.colored_output(f"Stage 1 completed!", "success")
