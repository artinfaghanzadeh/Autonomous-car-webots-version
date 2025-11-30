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

from controller import GPS, Gyro, Robot


@dataclass
class SensorReadings:
    gps: Optional[Tuple[float, float, float]] = None
    gyro: Optional[Tuple[float, float, float]] = None


class SensorInterface:
    def __init__(self, robot: Robot, timestep: int):
        self._gps: Optional[GPS] = None
        self._gyro: Optional[Gyro] = None

        try:
            gps_dev = robot.getDevice("gps")
            if isinstance(gps_dev, GPS):
                self._gps = gps_dev
                self._gps.enable(timestep)
        except Exception:
            self._gps = None


        try:
            gyro_dev = robot.getDevice("gyro")
            if isinstance(gyro_dev, Gyro):
                self._gyro = gyro_dev
                self._gyro.enable(timestep)
        except Exception:
            self._gyro = None

    def read(self) -> SensorReadings:
        gps_val: Optional[Tuple[float, float, float]] = None
        gyro_val: Optional[Tuple[float, float, float]] = None

        if self._gps is not None:
            v = self._gps.getValues()
            gps_val = (round(float(v[0]), 3), round(float(v[1]), 3), round(float(v[2]), 3))

        if self._gyro is not None:
            g = self._gyro.getValues()
            gyro_val = (round(float(g[0]), 3), round(float(g[1]), 3), round(float(g[2]), 3))

        return SensorReadings(gps=gps_val, gyro=gyro_val)