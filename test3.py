
import time
import numpy as np

from mission_controller.mission_controller import MissionController, CustomError
from mission_controller.simulated_robot import SimulatedRobot, SimulatedRobotWithCommunicationDelay

# checking the finish flag

def test_normal_operation():

    print("Test3 : checking the finish flag")

    simulated_robot = SimulatedRobotWithCommunicationDelay(np.array([2.0,1.0]))

    controller = MissionController(simulated_robot)

    # set the first trajectory

    controller.set_trajectory(np.array([[4.0,3.0], [5.0, 3.0]]))
    
    controller.finish_flag.wait()

    controller.set_trajectory(np.array([[3.0,3.0], [5.0, 4.0]]))

    controller.join()

    print("Test3 complete")

    exit(0)


if __name__ == "__main__":
    test_normal_operation()
