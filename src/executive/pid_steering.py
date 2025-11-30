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


class SteeringPID:
    def __init__(self, ui: UIConfig, max_steer: float):
        self.ui = ui
        self.max_steer = max_steer
        self._prev_output = 0.0

    def compute(self, lateral_error: float) -> float:
        raw = self.ui.steering.gain * lateral_error
        raw = max(-self.max_steer, min(self.max_steer, raw))
        smooth = (
            self.ui.steering.smooth * raw
            + (1.0 - self.ui.steering.smooth) * self._prev_output
        )
        self._prev_output = smooth
        return smooth
