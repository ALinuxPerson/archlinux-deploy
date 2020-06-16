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
import pathlib
import os

VM_NAME: str = os.getenv("ALD_VM_NAME", "arch-linux")
VM_VRAM_SIZE: int = int(os.getenv("ALD_VM_VRAM_SIZE", 16))
VM_MEM_SIZE: int = int(os.getenv("ALD_VM_MEM_SIZE", 1024))
VM_IGNORE_DUPLICATES: bool = bool(int(os.getenv("ALD_VM_IGNORE_DUPLICATES", 0)))
# shouldn't matter if the whitespace is escaped or not
VBOX_VMS_LOCATION: str = os.getenv("ALD_VBOX_VMS_LOCATION", os.path.join(str(pathlib.Path.home()), "VirtualBox VMs"))
VM_HDD_SIZE: int = int(os.getenv("ALD_VM_HDD_SIZE", 20480))
