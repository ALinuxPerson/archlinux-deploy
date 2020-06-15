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
from archlinux_deploy import utils
from typing import List, Callable
import virtualbox

def check_for_vboxapi():
    utils.colored_output("Stage 1: check_for_vboxapi", "info")
    try:
        import vboxapi
    except ModuleNotFoundError:
        raise BaseStageException("Stage 1 Error: Substage check_for_vboxapi FAILED:\n"
                                 "It seems like vboxapi isn't installed as a python module.\n"
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

def run():
    stages: List[Callable] = [check_for_vboxapi]