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
from typing import List, Tuple, Optional

import cv2
import numpy as np

from config.ui_config import UIConfig
from src.common.perception_state import PerceptionState


Line = Tuple[int, int, int, int]


@dataclass
class LaneDetectionResult:
    perception: PerceptionState
    center_lines: List[Line]
    right_lines: List[Line]


class LaneDetector:
    def __init__(self, ui: UIConfig, car_center_x: int):
        self.ui = ui
        self.car_center_x = car_center_x
        self._prev_midpoints: Optional[List[Tuple[int, int]]] = None

    def _edges(self, gray: np.ndarray) -> np.ndarray:
        edges = cv2.Canny(
            gray, self.ui.canny.low, self.ui.canny.high
        )
        kernel = np.ones(
            (self.ui.canny.morph_kernel, self.ui.canny.morph_kernel), np.uint8
        )
        return cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    @staticmethod
    def _classify_lines(
        lines: Optional[np.ndarray],
    ) -> Tuple[List[Line], List[Line]]:
        center_lines: List[Line] = []
        right_lines: List[Line] = []
        if lines is None:
            return center_lines, right_lines

        for l in lines:
            x1, y1, x2, y2 = l[0]
            slope = (y2 - y1) / (x2 - x1 + 1e-6)
            if slope < 0:
                center_lines.append((x1, y1, x2, y2))
            else:
                right_lines.append((x1, y1, x2, y2))
        return center_lines, right_lines

    def _build_midpoints(
        self, center_lines: List[Line], right_lines: List[Line], ch: int
    ) -> List[Tuple[int, int]]:
        midpoints: List[Tuple[int, int]] = []
        if not center_lines and not right_lines:
            return midpoints

        num_samples = 15
        ys = np.linspace(ch - 1, 0, num_samples).astype(int)

        for y in ys:
            xs_center = []
            xs_right = []

            for x1, y1, x2, y2 in center_lines:
                if (y1 <= y <= y2) or (y2 <= y <= y1):
                    if y2 != y1:
                        t = (y - y1) / (y2 - y1)
                        xs_center.append(x1 + t * (x2 - x1))

            for x1, y1, x2, y2 in right_lines:
                if (y1 <= y <= y2) or (y2 <= y <= y1):
                    if y2 != y1:
                        t = (y - y1) / (y2 - y1)
                        xs_right.append(x1 + t * (x2 - x1))

            if xs_center and xs_right:
                xc = float(np.mean(xs_center))
                xr = float(np.mean(xs_right))
                xm = (xc + xr) / 2.0
                midpoints.append((int(xm), int(y)))

        return midpoints

    def _smooth_midpoints(
        self, midpoints: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        if not midpoints:
            return self._prev_midpoints or []

        if self._prev_midpoints is None or len(self._prev_midpoints) != len(
            midpoints
        ):
            self._prev_midpoints = midpoints
            return midpoints

        alpha = self.ui.lane_smoothing.alpha_midpoints
        smooth: List[Tuple[int, int]] = []
        for (x, y), (px, py) in zip(midpoints, self._prev_midpoints):
            x_s = int(alpha * x + (1 - alpha) * px)
            smooth.append((x_s, y))

        self._prev_midpoints = smooth
        return smooth

    def detect(
        self, blur_gray: np.ndarray, mode_text: str
    ) -> LaneDetectionResult:
        ch, cw = blur_gray.shape[:2]
        edge_img = self._edges(blur_gray)

        raw_lines = cv2.HoughLinesP(
            edge_img,
            rho=1,
            theta=np.pi / 180,
            threshold=40,
            minLineLength=40,
            maxLineGap=35,
        )

        center_lines, right_lines = self._classify_lines(raw_lines)
        midpoints = self._build_midpoints(center_lines, right_lines, ch)
        midpoints = self._smooth_midpoints(midpoints)

        follow_point = None
        if midpoints:
            follow_point = midpoints[0]

        perception = PerceptionState(
            midpoints=midpoints,
            follow_point=follow_point,
            mode_text=mode_text,
            car_center_x=self.car_center_x,
            valid_lane=follow_point is not None,
        )

        return LaneDetectionResult(
            perception=perception,
            center_lines=center_lines,
            right_lines=right_lines,
        )
