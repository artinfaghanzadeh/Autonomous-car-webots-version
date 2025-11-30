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
from dataclasses import dataclass, field
from typing import List, Tuple, Optional


Point = Tuple[int, int]


@dataclass
class PerceptionState:
    midpoints: List[Point] = field(default_factory=list)
    follow_point: Optional[Point] = None
    mode_text: str | None = None
    car_center_x: int = 0
    valid_lane: bool = False