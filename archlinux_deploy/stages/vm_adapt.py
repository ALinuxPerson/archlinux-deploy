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
import subprocess

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

def vbox_manage_command() -> str:
    if utils.in_path_env("vboxmanage" if utils.is_posix() else "vboxmanage.exe"):
        return "vboxmanage" if utils.is_posix() else "vboxmanage.exe"
    elif utils.in_path_env("VboxManage" if utils.is_posix() else "VboxManage.exe"):
        return "VboxManage" if utils.is_posix() else "VboxManage.exe"
    else:
        raise BaseStageException(
            "It seems like the vboxmanage command isn't in PATH. Either check in /usr/lib/virtualbox or C:\\Program Files\\Virtualbox"
        )

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
            name=VM_NAME,
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
    vbox: virtualbox.VirtualBox = virtualbox.VirtualBox()
    vm: virtualbox.library.IMachine = vbox.find_machine(VM_NAME)
    print(f"[blue]Changing VRAM size to {VM_VRAM_SIZE} MB.")
    try:
        vm.vram_size = VM_VRAM_SIZE
    except AttributeError:
        print("[yellow]Couldn't change vram size using 'virtualbox' module, using subprocess instead")
        sp_call(f"{vbox_manage_command()} modifyvm {VM_NAME} --vram {VM_VRAM_SIZE}")
    print("[green]Operation successful.")
    print(f"[blue]Changing memory size to {VM_MEM_SIZE} MB.")
    try:
        vm.memory_size = VM_MEM_SIZE
    except Exception:  # virtualbox module raises a Exception exception
        print("[yellow]Couldn't change memory size using 'virtualbox' module, using subprocess instead")
        sp_call(f"{vbox_manage_command()} modifyvm {VM_NAME} --memory {VM_MEM_SIZE}")
    print("[green]Operation successful.")
    print("[blue]Changing graphics controller to vmsvga.")
    try:
        vm.graphics_controller_type = virtualbox.library.GraphicsControllerType.VMSVGA
    except AttributeError:
        print("[yellow]Couldn't change graphics controller type using 'virtualbox' module, using subprocess instead")
        sp_call(f"{vbox_manage_command()} modifyvm {VM_NAME} --graphicscontroller vmsvga")
    print("[green]Operation successful.")

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
