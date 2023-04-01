
import numpy as np
import time
from threading import Thread, Lock, Event
from mission_controller.simulated_robot import SimulatedRobot, SimulatedRobotWithCommunicationDelay
from mission_controller.custom_error import CustomError

class MissionController:

    def __init__(self, robot):
        print("Creating MissionController!")
        self.thread_poll_position = Thread()
        if (isinstance(robot,SimulatedRobotWithCommunicationDelay) or isinstance(robot,SimulatedRobot)):
            self.robot = robot
        else:
            raise CustomError("Invalid MissionController class initialisation")
        self.current_waypoint_idx = 0
        self.trajectory = None
        self.stop_flag = Event()
        self.finish_flag = Event()
        self.finish_flag.clear()

    # similar to thread.join function to wait for thread completion
    def join(self):
        if (self.thread_poll_position.is_alive()):
            self.thread_poll_position.join()

    def set_stop(self):
        self.stop_flag.set()
        self.robot.stop_flag.set()
        self.robot._robot.stop_flag.set()
        self.finish_flag.clear()

    def reset_stop(self):
        self.stop_flag.clear()
        self.robot.stop_flag.clear()
        self.robot._robot.stop_flag.clear()

    # check input validation
    def is_valid(self, trajectory):
        if not isinstance(trajectory, np.ndarray):
            print("- The trajectory type is invalid - ")
            return False
        elif trajectory.ndim == 1 and trajectory.shape[0] == 0:
            print("Got Empty trajectory. STOPPING")
            self.finish_flag.set()
            return False
        elif trajectory.ndim != 2 :
            print("- Provide numpy of 2 dimensions - ")
            return False
        elif trajectory.shape[1] != 2:
            print("- Provide numpy of shape - N x 2 -")
            return False
        return True
        
    # checks for active thread if any and starts a new thread for
    # trajectory implementation
    def set_trajectory(self, trajectory):
        
        if (self.thread_poll_position.is_alive()):
            print("- ABORTED: moving towards position ", 
                    self.trajectory[self.current_waypoint_idx], " -")
            print("- ABORTED: previous Trajectory at position ", self.robot.get_position(), " -")
        
        # setting stop flag for stopping the thread
        self.set_stop()
        if (self.thread_poll_position.is_alive()):
            self.thread_poll_position.join()
        self.reset_stop()
        self.trajectory = None

        # input validation
        if not self.is_valid(trajectory):
            return
        
        # setting up of thread
        print("Setting up new trajectory")
        self.trajectory = trajectory
        self.current_waypoint_idx = 0
        self.thread_poll_position = Thread(
            target=self._poll_position, daemon=True)
        self.thread_poll_position.start()

    # Moves the robot by giving commands to execute the trajectory
    def _poll_position(self):

        time.sleep(1)

        position = self.robot.get_position()

        if not self.stop_flag.is_set():
            if self.trajectory is None:
                return
            elif not self.trajectory is None and self.trajectory.shape[0] == 0:
                return
            else:
                # checks the position for last trajectory point 
                # if not gives the trajectory points in sequence
                if np.all(position == self.trajectory[-1]):
                    print("Trajectory executed successfully")
                    self.finish_flag.set()
                    return
                else:
                    self._send_navigation_command()
                    if (self.current_waypoint_idx < self.trajectory.shape[0]-1):
                        self.current_waypoint_idx += 1
        else:
            return

        self._poll_position()

    # Sends the command to robot
    def _send_navigation_command(self):
        if np.all(self.robot.get_position() == self.trajectory[self.current_waypoint_idx]):
            return
        print(f"Sending waypoint {self.current_waypoint_idx}")

        self.robot.set_navigation_command(
            self.trajectory[self.current_waypoint_idx])
