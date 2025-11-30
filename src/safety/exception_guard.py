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
from typing import Callable

from src.common.control_command import ControlCommand


class ExceptionGuard:
    def __init__(self, fallback_speed: float = 0.0):
        self.fallback_speed = fallback_speed

    def run_safe(self, step_fn: Callable[[], ControlCommand]) -> ControlCommand:
        try:
            return step_fn()
        except Exception:
            return ControlCommand(steering=0.0, speed=self.fallback_speed)
