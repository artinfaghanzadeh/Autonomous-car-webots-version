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
from typing import Optional

import numpy as np
from controller import Camera, Robot


class CameraInterface:
    def __init__(self, robot: Robot, name: str, timestep: int):
        self._camera: Camera = robot.getDevice(name)
        self._camera.enable(timestep)
        self.width = self._camera.getWidth()
        self.height = self._camera.getHeight()

    def get_frame(self) -> Optional[np.ndarray]:
        img = self._camera.getImage()
        if img is None:
            return None
        buf = np.frombuffer(img, dtype=np.uint8).reshape((self.height, self.width, 4))
        return buf