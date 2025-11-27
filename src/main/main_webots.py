"""
 -------------------------------------------
|      Autonomous-car-webots-version        |
|                                           |
|      Programmed by Artin Faghanzade       |
|          a.faghanzadeh@gmail.com          |
 -------------------------------------------


Main File
"""

import cv2
from controller import Robot, Camera, Motor

from config import parameters as cfg
from perception.camera import CameraProcessor
from control.movement import MovementController

def main():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())

    # Cam
    camera = robot.getDevice("camera")
    camera.enable(timestep)
    width = camera.getWidth()
    height = camera.getHeight()

    # Motor
    left_steer = robot.getDevice("left_steer")
    right_steer = robot.getDevice("right_steer")
    left_front = robot.getDevice("left_front_wheel")
    right_front = robot.getDevice("right_front_wheel")

    # velocity
    left_front.setPosition(float("inf"))
    right_front.setPosition(float("inf"))
    left_front.setVelocity(0.0)
    right_front.setVelocity(0.0)


    cam_processor = CameraProcessor()
    movement = MovementController(
        left_steer=left_steer,
        right_steer=right_steer,
        left_front=left_front,
        right_front=right_front,
    )

    while robot.step(timestep) != -1:
        img = camera.getImage()
        if img is None:
            continue

        debug_frame, follow_x = cam_processor.process(raw_image=img, width=width, height=height)

        movement.drive(follow_x)

        cv2.imshow("Lane Debug", debug_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()