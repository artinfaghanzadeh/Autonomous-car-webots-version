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
import sys
from pathlib import Path
from controller import Robot

# add project root
project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

from src.core.core import main_loop


def run():
    robot = Robot()
    main_loop(robot)


if __name__ == "__main__":
    run()
