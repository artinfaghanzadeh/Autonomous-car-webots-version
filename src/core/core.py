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
from controller import Robot

from config.statics import load_statics
from config.ui_config import load_ui
from src.adjust_data.camera_filter import CameraPreprocessor
from src.common.vehicle_state import VehicleState
from src.executive.commands import CommandBuilder
from src.executive.pid_speed import SpeedController
from src.executive.pid_steering import SteeringPID
from src.fw_debug.camera_overlay import CameraOverlay
from src.get_data.camera import CameraInterface
from src.get_data.wheel import WheelInterface
from src.logic.lanes_behavior import LaneBehaviorPlanner
from src.process.lanes_detection import LaneDetector
from src.safety.exception_guard import ExceptionGuard
from config.debug_config import load_debug
from src.get_data.raw_sensor import SensorInterface
from src.adjust_data.sensor_filter import SensorFilter



def main_loop(robot: Robot) -> None:

    timestep = int(robot.getBasicTimeStep())

    statics = load_statics()
    ui = load_ui()
    debug_cfg = load_debug()

    cam_if = CameraInterface(robot, statics.camera.name, timestep)
    wheel_if = WheelInterface(robot)
    sensor_if = SensorInterface(robot, timestep)

    dt_seconds = timestep / 1000.0
    sensor_filter = SensorFilter(dt_seconds)

    camera_pre = CameraPreprocessor(statics, ui)
    lane_detector = LaneDetector(ui, statics.vehicle.car_center_x)
    lane_behavior = LaneBehaviorPlanner(ui)
    steering_pid = SteeringPID(ui, statics.vehicle.max_steer_rad)
    speed_ctrl = SpeedController(max_speed_kmh=statics.vehicle.max_speed, wheel_radius_m=statics.vehicle.wheel_radius_m,)
    cmd_builder = CommandBuilder(steering_pid, speed_ctrl)
    cam_overlay = CameraOverlay()
    guard = ExceptionGuard(fallback_speed=0.0)

    vehicle_state = VehicleState()

    def step_once():
        sensor_readings = sensor_if.read()
        filtered = sensor_filter.filter(sensor_readings)
        vehicle_state.speed = filtered.speed
        
        if debug_cfg.show_sensor_data:
            print(
                "Sensors:",
                f"GPS={sensor_readings.gps}",
                f"GYRO={sensor_readings.gyro}",
                f"speed={filtered.speed:.2f} m/s",
            )
        
        
        raw_frame = cam_if.get_frame()
        if raw_frame is None:
            return cmd_builder.build(
                lane_behavior.plan(
                    perception=lane_detector.detect(camera_pre.preprocess(raw_frame).gray).perception,vehicle=vehicle_state), vehicle=vehicle_state)

        pre = camera_pre.preprocess(raw_frame)
        lane_res = lane_detector.detect(pre.gray, pre.mode_text)
        behavior = lane_behavior.plan(lane_res.perception, vehicle_state)
        command = cmd_builder.build(behavior, vehicle_state)
        
        if debug_cfg.enable_logs:
            print(f"debug : steer={command.steering:.4f}    target_kmh={behavior.target_speed:.2f}   wheel_rad_s={command.speed:.2f}")


        if debug_cfg.enable_camera_overlay:
            debug_img = cam_overlay.render(
                pre.gray,
                lane_res.perception,
                lane_res.center_lines,
                lane_res.right_lines,
                enable_lane_overlay=debug_cfg.enable_lane_overlay,
            )
        else:
            debug_img = pre.gray

        import cv2


        if debug_cfg.enable_cv_window:
            cv2.imshow("Lane Debug", debug_img)
            cv2.waitKey(1)

        wheel_if.apply_command(command)
        return command

    while robot.step(timestep) != -1:
        guard.run_safe(step_once)
