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
from archlinux_deploy.stages.exceptions import BaseStageException
from typing import List, Callable
from archlinux_deploy import utils
from bs4 import BeautifulSoup
from rich import print
import virtualbox
import requests
import time
import os

def check_for_vboxapi():
    try:
        print("[blue]Checking if module 'vboxapi' is installed...")
        import vboxapi
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

def download_latest_iso():
    arch_linux_website: str = "http://mirror.rackspace.com/archlinux/iso/latest/"
    page: str = requests.get(arch_linux_website).text
    soup: BeautifulSoup = BeautifulSoup(page, "html.parser")
    all_isos: List[str] = [arch_linux_website + "/" + node.get("href") for node in soup.find_all("a") if node.get("href").endswith("iso")]
    with open("./arch-linux.iso", "wb") as iso:
        if os.path.exists("./arch-linux.iso"):
            print("[blue]ISO seems to be already downloaded, continuing...")
            return
        response: requests.Response = requests.get(all_isos[0], stream=True)
        print("[blue]Writing Arch Linux ISO to disk...")
        for data in response.iter_content(chunk_size=1024):
            iso.write(data)

def run():
    stages: List[Callable] = [check_for_vboxapi, download_latest_iso]
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

run()