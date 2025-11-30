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
import yaml
from dataclasses import dataclass
from pathlib import Path


@dataclass
class LightingConfig:
    dark_threshold: float
    clahe_clip_limit: float
    clahe_tile_grid: int


@dataclass
class LaneFilterConfig:
    gaussian_ksize: int
    gaussian_sigma: float
    median_ksize: int


@dataclass
class CannyConfig:
    low: int
    high: int
    morph_kernel: int


@dataclass
class LaneSmoothingConfig:
    alpha_midpoints: float


@dataclass
class SteeringConfig:
    gain: float
    smooth: float


@dataclass
class SpeedConfig:
    base_speed: float
    lost_factor: float


@dataclass
class UIConfig:
    lighting: LightingConfig
    lane_filter: LaneFilterConfig
    canny: CannyConfig
    lane_smoothing: LaneSmoothingConfig
    steering: SteeringConfig
    speed: SpeedConfig


def load_ui(path: str | Path | None = None) -> UIConfig:
    if path is None:
        path = Path(__file__).with_name("ui.yaml")
    else:
        path = Path(path)

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    return UIConfig(
        lighting=LightingConfig(**data["lighting"]),
        lane_filter=LaneFilterConfig(**data["lane_filter"]),
        canny=CannyConfig(**data["canny"]),
        lane_smoothing=LaneSmoothingConfig(**data["lane_smoothing"]),
        steering=SteeringConfig(**data["steering"]),
        speed=SpeedConfig(**data["speed"]),
    )
