
import numpy as np

import time

from threading import Thread, Event

import random

from mission_controller.custom_error import CustomError


class SimulatedRobot:

    def __init__(self, initial_position, update_position_callback=None):
        print("Creating SimulatedRobot!")
        if isinstance(initial_position,np.ndarray):
            if initial_position.ndim == 1:
                if initial_position.shape[0]==2:
                    self.position = initial_position
                else:
                    raise CustomError("Invalid SimulatedRobot class initialisation on shape")
            else:
                raise CustomError("Invalid SimulatedRobot class initialisation on dimension")
        else:
            raise CustomError("Invalid SimulatedRobot class initialisation on type")
        self.update_position_callback = update_position_callback
        self.stop_flag = Event()

    def get_position(self):
        return self.position

    # sets the navigation command and wait for it to reach
    def set_navigation_command(self, waypoint):

        wait = random.uniform(1.0, 2.0)
        start = time.time()
        while ((time.time()-start) < wait):
            if self.stop_flag.is_set():
                return
            time.sleep(0.1)
        print(f"Robot is now at {waypoint}")
        self.position = waypoint
        self.update_position_callback(waypoint)

class SimulatedRobotWithCommunicationDelay:

    def __init__(self, initial_position):
        if isinstance(initial_position,np.ndarray):
            if initial_position.ndim == 1 :
                if initial_position.shape[0]==2:
                    self.position = initial_position
                else:
                    raise CustomError("Invalid SimulatedRobotWithCommunicationDelay class initialisation on shape")
            else:
                raise CustomError("Invalid SimulatedRobotWithCommunicationDelay class initialisation on dimensions")
        else:
            raise CustomError("Invalid SimulatedRobotWithCommunicationDelay class initialisation on type")
        
        self._robot = SimulatedRobot(initial_position, self.set_position)

        self.position = initial_position

        self.stop_flag = Event()

    # updates the position 
    def set_position(self, position):

        wait = random.uniform(0.0, 2.0)
        start = time.time()
        while ((time.time()-start) < wait):
            if self.stop_flag.is_set():
                return
            time.sleep(0.1)

        self.position = position

    def get_position(self):
        return self.position

    def set_navigation_command(self, waypoint):

        print(f"Commanding robot to move to {waypoint}")

        wait = random.uniform(0.0, 2.0)
        start = time.time()
        while ((time.time()-start) < wait):
            if self.stop_flag.is_set():
                return
            time.sleep(0.1)

        self._robot.set_navigation_command(waypoint)
