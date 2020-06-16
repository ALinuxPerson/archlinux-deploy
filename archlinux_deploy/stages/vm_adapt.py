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
from archlinux_deploy import VM_NAME, VM_MEM_SIZE, VM_VRAM_SIZE, VM_IGNORE_DUPLICATES, VBOX_VMS_LOCATION, VM_HDD_SIZE
from archlinux_deploy.stages.exceptions import BaseStageException  # type: ignore
from archlinux_deploy import utils
from typing import List, Callable
import virtualbox  # type: ignore
from rich import print

def create_vm():
    vbox: virtualbox.VirtualBox = virtualbox.VirtualBox()
    vm_names: List[str] = [machine.name for machine in vbox.machines]
    if VM_NAME in vm_names:
        if VM_IGNORE_DUPLICATES is False:
            raise BaseStageException(
                F"It seems like there's a vm that has the same name that was going to be created ({VM_NAME}).\n"
                F"Either rename the VM, set the vm_name in config.ini to something else or set ignore_duplicates to 1 in the environment variables."
            )
        print(f"[yellow]There's a VM with the same name ({VM_NAME}). Continuing anyway...")

    try:
        vm: virtualbox.library.IMachine = vbox.create_machine(
            name="arch-linux",
            os_type_id="ArchLinux_64",
            groups=["/"],
            flags="",
            settings_file=""
        )
        vbox.register_machine(vm)
    except virtualbox.library_ext.library.VBoxErrorFileError:
        pass
    print("[blue]Created and registered Arch Linux VM." if "arch-linux" not in vm_names else "[blue]Got Arch Linux VM.")

def set_vm_config():
    pass

def create_vm_controllers():
    pass

def attach_vm_controllers():
    pass

def run():
    stages: List[Callable] = [create_vm, set_vm_config, create_vm_controllers, attach_vm_controllers]
    for stage in stages:
        stage_name = stage.__name__
        utils.colored_output(f"Stage 2 Substage {stage_name} started!", "info")
        try:
            stage()
        except BaseStageException as error:
            message: str = error.args[0]
            utils.colored_output(
                f"Stage 2 Substage {stage_name} FAILED:\n"
                f"{message}",
                "error"
            )
            return
        utils.colored_output(f"Stage 2 Substage {stage_name} completed!", "success")
    utils.colored_output("Stage 2 completed!", "success")

run()
