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
from archlinux_deploy.stages import exceptions
from archlinux_deploy import utils
from typing import List, Callable

def create_vm():
    pass

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
        except exceptions.BaseStageException as error:
            message: str = error.args[0]
            utils.colored_output(
                f"Stage 2 Substage {stage_name} FAILED:\n"
                f"{message}",
                "error"
            )
            return
        utils.colored_output(f"Stage 2 Substage {stage_name} completed!", "success")
    utils.colored_output("Stage 2 completed!", "success")
