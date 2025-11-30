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
from controller import Motor, Robot

from src.common.control_command import ControlCommand


class WheelInterface:
    def __init__(self, robot: Robot):
        self.left_steer: Motor = robot.getDevice("left_steer")
        self.right_steer: Motor = robot.getDevice("right_steer")

        self.left_front: Motor = robot.getDevice("left_front_wheel")
        self.right_front: Motor = robot.getDevice("right_front_wheel")

        self.left_front.setPosition(float("inf"))
        self.right_front.setPosition(float("inf"))
        self.left_front.setVelocity(0.0)
        self.right_front.setVelocity(0.0)

    def apply_command(self, command: ControlCommand) -> None:
        self.left_steer.setPosition(command.steering)
        self.right_steer.setPosition(command.steering)
        self.left_front.setVelocity(command.speed)
        self.right_front.setVelocity(command.speed)
