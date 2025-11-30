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
class CameraStatics:
    name: str
    width: int
    height: int
    crop_ratio_bottom: float


@dataclass
class VehicleStatics:
    car_center_x: int
    max_steer_rad: float
    max_speed: float
    wheel_radius_m: float


@dataclass
class StaticsConfig:
    camera: CameraStatics
    vehicle: VehicleStatics


def load_statics(path: str | Path | None = None) -> StaticsConfig:
    if path is None:

        path = Path(__file__).with_name("statics.yaml")
    else:
        path = Path(path)

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    cam = data["camera"]
    veh = data["vehicle"]

    return StaticsConfig(
        camera=CameraStatics(
            name=cam["name"],
            width=cam["width"],
            height=cam["height"],
            crop_ratio_bottom=cam["crop_ratio_bottom"],
        ),
        vehicle=VehicleStatics(
            car_center_x=veh["car_center_x"],
            max_steer_rad=veh["max_steer_rad"],
            max_speed=veh["max_speed"],
            wheel_radius_m=veh["wheel_radius_m"]
        ),
    )
