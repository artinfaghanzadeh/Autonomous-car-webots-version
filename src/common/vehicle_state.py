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


@dataclass
class VehicleState:
    speed: float = 0.0
    yaw: float = 0.0
    x: float = 0.0
    y: float = 0.0