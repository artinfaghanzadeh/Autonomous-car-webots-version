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
from typing import Tuple

import cv2
import numpy as np

from config.statics import StaticsConfig
from config.ui_config import UIConfig


@dataclass
class CameraPreprocessResult:
    gray: np.ndarray
    crop_top: int
    mode_text: str
    width: int
    height: int


class CameraPreprocessor:
    def __init__(self, statics: StaticsConfig, ui: UIConfig):
        self.statics = statics
        self.ui = ui

    @staticmethod
    def _adjust_gamma(img: np.ndarray, gamma: float) -> np.ndarray:
        inv = 1.0 / (gamma + 1e-6)
        table = np.array([(i / 255.0) ** inv * 255 for i in range(256)]).astype(
            "uint8"
        )
        return cv2.LUT(img, table)

    def preprocess(self, rgba_frame: np.ndarray) -> CameraPreprocessResult:
        bgr = cv2.cvtColor(rgba_frame, cv2.COLOR_RGBA2BGR)
        h, w = bgr.shape[:2]
        crop_top = int(h * self.statics.camera.crop_ratio_bottom)
        crop = bgr[crop_top:h, :]
        ch, cw = crop.shape[:2]

        gray_raw = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        mean_raw = float(np.mean(gray_raw))

        if mean_raw < self.ui.lighting.dark_threshold:
            clahe = cv2.createCLAHE(
                clipLimit=self.ui.lighting.clahe_clip_limit,
                tileGridSize=(
                    self.ui.lighting.clahe_tile_grid,
                    self.ui.lighting.clahe_tile_grid,
                ),
            )
            gray = clahe.apply(gray_raw)
            gamma = 160.0 / (np.mean(gray) + 1e-6)
            gamma = float(np.clip(gamma, 0.5, 3.0))
            gray = self._adjust_gamma(gray, gamma)
            gray = cv2.normalize(
                gray, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX
            )
            mode_text = f"Mode=BOOST MeanRaw={mean_raw:.1f}"
        else:
            gray = gray_raw
            mode_text = f"Mode=NORMAL MeanRaw={mean_raw:.1f}"

        blur = cv2.GaussianBlur(
            gray,
            (self.ui.lane_filter.gaussian_ksize, self.ui.lane_filter.gaussian_ksize),
            self.ui.lane_filter.gaussian_sigma,
        )
        blur = cv2.medianBlur(blur, self.ui.lane_filter.median_ksize)

        return CameraPreprocessResult(
            gray=blur,
            crop_top=crop_top,
            mode_text=mode_text,
            width=cw,
            height=ch,
        )
