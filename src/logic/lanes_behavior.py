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
from dataclasses import dataclass

from config.ui_config import UIConfig
from src.common.control_command import ControlCommand
from src.common.perception_state import PerceptionState
from src.common.vehicle_state import VehicleState


@dataclass
class LaneBehaviorOutput:
    target_lateral_error: float
    target_speed: float


class LaneBehaviorPlanner:
    def __init__(self, ui: UIConfig):
        self.ui = ui

    def plan(
        self, perception: PerceptionState, vehicle: VehicleState
    ) -> LaneBehaviorOutput:
        if not perception.valid_lane or perception.follow_point is None:
            speed = self.ui.speed.base_speed * self.ui.speed.lost_factor
            return LaneBehaviorOutput(target_lateral_error=0.0, target_speed=speed)

        follow_x, _ = perception.follow_point
        error_x = float(follow_x - perception.car_center_x)
        speed = self.ui.speed.base_speed
        return LaneBehaviorOutput(
            target_lateral_error=error_x,
            target_speed=speed,
        )
