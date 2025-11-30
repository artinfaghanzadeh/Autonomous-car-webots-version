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
from typing import List, Tuple

import cv2
import numpy as np

from src.common.perception_state import PerceptionState
from src.process.lanes_detection import Line


class CameraOverlay:
    def render(
        self,
        gray_crop: np.ndarray,
        perception: PerceptionState,
        center_lines: List[Line],
        right_lines: List[Line],
        enable_lane_overlay: bool = True,
    ) -> np.ndarray:
        debug = cv2.cvtColor(gray_crop, cv2.COLOR_GRAY2BGR)

        if perception.mode_text:
            cv2.putText(
                debug,
                perception.mode_text,
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 255),
                2,
            )

        h, w = debug.shape[:2]
        if 0 <= perception.car_center_x < w:
            cv2.line(
                debug,
                (perception.car_center_x, 0),
                (perception.car_center_x, h - 1),
                (255, 255, 0),
                2,
            )
            
        if enable_lane_overlay:
            for x1, y1, x2, y2 in center_lines:
                cv2.line(debug, (x1, y1), (x2, y2), (255, 0, 0), 3)
            for x1, y1, x2, y2 in right_lines:
                cv2.line(debug, (x1, y1), (x2, y2), (0, 255, 0), 3)

            if perception.midpoints and len(perception.midpoints) > 1:
                for i in range(len(perception.midpoints) - 1):
                    cv2.line(
                        debug,
                        perception.midpoints[i],
                        perception.midpoints[i + 1],
                        (0, 0, 255),
                        3,
                    )

            if perception.follow_point:
                cv2.circle(debug, perception.follow_point, 5, (0, 255, 255), -1)

        return debug
