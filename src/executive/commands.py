# ===============================================================
#
# Copyright (c) 2025, Artin Faghanzadeh
# This file is part of the Autonomous-car-webots-version project.
# All rights reserved.
#
# Author: Artin Faghanzadeh
# GitHub: https://github.com/artinfaghanzadeh
# LinkedIn: https://www.linkedin.com/in/artin-faghanzadeh
#
# ===============================================================
from src.common.control_command import ControlCommand
from src.logic.lanes_behavior import LaneBehaviorOutput
from src.common.vehicle_state import VehicleState

from src.executive.pid_steering import SteeringPID
from src.executive.pid_speed import SpeedController


class CommandBuilder:
    def __init__(self, steering_pid: SteeringPID, speed_ctrl: SpeedController):
        self.steering_pid = steering_pid
        self.speed_ctrl = speed_ctrl

    def build(
        self, behavior: LaneBehaviorOutput, vehicle: VehicleState
    ) -> ControlCommand:
        steer = self.steering_pid.compute(behavior.target_lateral_error)
        speed = self.speed_ctrl.compute(behavior.target_speed)
        return ControlCommand(steering=steer, speed=speed)
