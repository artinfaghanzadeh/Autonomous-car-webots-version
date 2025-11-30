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
class DebugConfig:
    enable_camera_overlay: bool
    enable_lane_overlay: bool
    enable_logs: bool
    enable_cv_window: bool
    show_sensor_data: bool
    record_data: bool



def load_debug(path: str | Path | None = None) -> DebugConfig:
    if path is None:
        path = Path(__file__).with_name("debug.yaml")
    else:
        path = Path(path)

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    dbg = data["debug"]

    return DebugConfig(
        enable_camera_overlay=dbg["enable_camera_overlay"],
        enable_lane_overlay=dbg["enable_lane_overlay"],
        enable_logs=dbg["enable_logs"],
        enable_cv_window=dbg["enable_cv_window"],
        show_sensor_data=dbg["show_sensor_data"],
        record_data=dbg["record_data"],
    )
