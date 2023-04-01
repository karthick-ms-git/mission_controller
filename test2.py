
import time
import numpy as np

from mission_controller.mission_controller import MissionController
from mission_controller.simulated_robot import SimulatedRobot, SimulatedRobotWithCommunicationDelay

# For input validation and check for controller.join
def test_normal_operation():

    print("Test2 : For input validation and check for controller.join")

    simulated_robot = SimulatedRobotWithCommunicationDelay(np.array([0.0, 0.0]))

    controller = MissionController(simulated_robot)

    # set the first trajectory as invalid

    controller.set_trajectory(np.array([[0.0, 0.0], [1.0]]))
    
    time.sleep(3)

    controller.set_trajectory(np.array([[2.0, 0.0], [3.0, 0.0]]))

    controller.set_trajectory(np.array([[2.0, 3.0], [3.0, 0.0]]))

    controller.join()
    print("Test complete")

    exit(0)


if __name__ == "__main__":
    test_normal_operation()
