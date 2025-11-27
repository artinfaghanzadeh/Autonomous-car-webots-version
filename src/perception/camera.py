"""
 -------------------------------------------
|      Autonomous-car-webots-version        |
|                                           |
|      Programmed by Artin Faghanzade       |
|          a.faghanzadeh@gmail.com          |
 -------------------------------------------


Camera processing
"""

from typing import Optional, Tuple, List
import numpy as np
import cv2

from config import parameters as cfg
from framework import filters


class CameraProcessor:
    def __init__(self):
        self.prev_midpoints: Optional[List[Tuple[int, int]]] = None

    def _compute_midline(
        self,
        ch: int,
        center_lines: List[Tuple[int, int, int, int]],
        right_lines: List[Tuple[int, int, int, int]],
    ) -> Optional[List[Tuple[int, int]]]:
        midpoints: List[Tuple[int, int]] = []

        if not center_lines and not right_lines:
            return None

        ys = np.linspace(ch - 1, 0, cfg.NUM_MIDLINE_SAMPLES).astype(int)

        for y in ys:
            xs_center = []
            xs_right = []

            for (x1, y1, x2, y2) in center_lines:
                if (y1 <= y <= y2) or (y2 <= y <= y1):
                    if y2 != y1:
                        t = (y - y1) / (y2 - y1)
                        xs_center.append(x1 + t * (x2 - x1))

            for (x1, y1, x2, y2) in right_lines:
                if (y1 <= y <= y2) or (y2 <= y <= y1):
                    if y2 != y1:
                        t = (y - y1) / (y2 - y1)
                        xs_right.append(x1 + t * (x2 - x1))

            if xs_center and xs_right:
                xc = np.mean(xs_center)
                xr = np.mean(xs_right)
                xm = (xc + xr) / 2.0
                midpoints.append((int(xm), int(y)))

        if not midpoints:
            return None
        return midpoints

    def _smooth_midline(
        self, midpoints: Optional[List[Tuple[int, int]]]
    ) -> Optional[List[Tuple[int, int]]]:
        if midpoints:
            if (self.prev_midpoints is not None and len(self.prev_midpoints) == len(midpoints)):
                smooth = []
                for (x, y), (px, py) in zip(midpoints, self.prev_midpoints):
                    x_s = int(cfg.ALPHA_SMOOTH_MIDLINE * x + (1 - cfg.ALPHA_SMOOTH_MIDLINE) * px)
                    smooth.append((x_s, y))
                midpoints = smooth

            self.prev_midpoints = midpoints
            return midpoints
        else:
            return self.prev_midpoints

    def process(
        self, raw_image: bytes, width: int, height: int
    ) -> Tuple[np.ndarray, Optional[int]]:
        frame = np.frombuffer(raw_image, dtype=np.uint8).reshape((height, width, 4))
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

        h, w = frame.shape[:2]
        crop_top = int(h * cfg.CROP_RATIO)
        crop = frame[crop_top:h, :]
        ch, cw = crop.shape[:2]

        gray_raw = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        gray, mode_text, _ = filters.apply_brightness_mode(gray_raw)

        debug = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        cv2.putText(debug, mode_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        if 0 <= cfg.CAR_CENTER_X < cw:
            cv2.line(debug, (cfg.CAR_CENTER_X, 0), (cfg.CAR_CENTER_X, ch - 1), (255, 255, 0), 2)

        blur = filters.denoise(gray)

        edges = filters.detect_edges(blur)

        lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 180, threshold=cfg.HOUGH_THRESHOLD, minLineLength=cfg.HOUGH_MIN_LINE_LENGTH, maxLineGap=cfg.HOUGH_MAX_LINE_GAP)

        center_lines = []
        right_lines = []

        if lines is not None:
            for l in lines:
                x1, y1, x2, y2 = l[0]
                slope = (y2 - y1) / (x2 - x1 + 1e-6)

                if slope < 0:
                    center_lines.append((x1, y1, x2, y2))
                    cv2.line(debug, (x1, y1), (x2, y2), (255, 0, 0), 3)
                else:
                    right_lines.append((x1, y1, x2, y2))
                    cv2.line(debug, (x1, y1), (x2, y2), (0, 255, 0), 3)

        midpoints = self._compute_midline(ch, center_lines, right_lines)

        midpoints = self._smooth_midline(midpoints)

        follow_x: Optional[int] = None
        if midpoints and len(midpoints) > 1:
            for i in range(len(midpoints) - 1):
                cv2.line(debug, midpoints[i], midpoints[i + 1], (0, 0, 255), 3)

            follow_x = midpoints[0][0]
            cv2.circle(debug, (follow_x, midpoints[0][1]), 5, (0, 255, 255), -1)

        return debug, follow_x