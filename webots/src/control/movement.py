from typing import Optional

from config_loader import parameters as cfg


class MovementController:
    def __init__(self, left_steer, right_steer, left_front, right_front):
        self.left_steer = left_steer
        self.right_steer = right_steer
        self.left_front = left_front
        self.right_front = right_front

        self.prev_steer = 0.0

    def drive(self, follow_x: Optional[int]):
        
        if follow_x is not None:
            error_x = follow_x - cfg.CAR_CENTER_X

            steer_cmd = cfg.STEER_GAIN * error_x
            steer_cmd = max(-cfg.STEER_LIMIT, min(cfg.STEER_LIMIT, steer_cmd))

            steer_cmd = (cfg.STEER_SMOOTH * steer_cmd + (1 - cfg.STEER_SMOOTH) * self.prev_steer)
            self.prev_steer = steer_cmd

            self.left_steer.setPosition(steer_cmd)
            self.right_steer.setPosition(steer_cmd)

            self.left_front.setVelocity(cfg.TARGET_SPEED)
            self.right_front.setVelocity(cfg.TARGET_SPEED)

        else:
            self.left_steer.setPosition(0.0)
            self.right_steer.setPosition(0.0)

            self.left_front.setVelocity(cfg.TARGET_SPEED * 0.6)
            self.right_front.setVelocity(cfg.TARGET_SPEED * 0.6)
