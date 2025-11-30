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
from typing import Optional, Tuple

from src.get_data.raw_sensor import SensorReadings


@dataclass
class FilteredSensors:
    speed: float = 0.0
    

class SensorFilter:
    def __init__(self, dt: float):
        self.dt = dt
        self._prev_gps: Optional[Tuple[float, float, float]] = None

    def filter(self, readings: SensorReadings) -> FilteredSensors:
        speed = 0.0

        if self._prev_gps is not None and readings.gps is not None and self.dt > 0.0:
            x0, y0, z0 = self._prev_gps
            x1, y1, z1 = readings.gps

            dx = x1 - x0
            dy = y1 - y0
            dz = z1 - z0

            dist = (dx * dx + dy * dy ) ** 0.5

            speed = dist / self.dt

        if readings.gps is not None:
            self._prev_gps = readings.gps

        return FilteredSensors(speed=speed)
    