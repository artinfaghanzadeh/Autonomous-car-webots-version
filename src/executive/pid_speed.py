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
from config.ui_config import UIConfig


class SpeedController:
    def __init__(self, max_speed_kmh: float, wheel_radius_m: float):
        self._max_speed_kmh = max_speed_kmh
        self._wheel_radius_m = wheel_radius_m

    def _kmh_to_motor(self, kmh: float) -> float:

        v_ms = kmh / 3.6

        if self._wheel_radius_m <= 0.0:
            return 0.0
        return v_ms / self._wheel_radius_m

    def compute(self, target_speed_kmh: float) -> float:

        if target_speed_kmh > self._max_speed_kmh:
            target_speed_kmh = self._max_speed_kmh
        elif target_speed_kmh < -self._max_speed_kmh:
            target_speed_kmh = -self._max_speed_kmh


        return self._kmh_to_motor(target_speed_kmh)
