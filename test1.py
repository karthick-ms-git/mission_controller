
import time
import numpy as np

from mission_controller.mission_controller import MissionController
from mission_controller.simulated_robot import SimulatedRobot, SimulatedRobotWithCommunicationDelay

# Test case given in instructions.md

def test_normal_operation():

    print("Test1 : Test case given in instructions.md")
    
    simulated_robot = SimulatedRobotWithCommunicationDelay(np.array([2.0,1.0]))

    controller = MissionController(simulated_robot)

    # set the first trajectory

    controller.set_trajectory(np.array([[4.0,3.0], [5.0, 3.0]]))
    
    time.sleep(1.5)

    controller.set_trajectory(np.array([[3.0,3.0], [5.0, 4.0]]))

    while(not np.all(simulated_robot.get_position() == np.array([3.0,3.0]))):
        time.sleep(0.1)
    
    time.sleep(1.5)

    controller.set_trajectory(np.array([]))

    time.sleep(2)

    controller.join()

    print("Test1 complete")

    exit(0)


if __name__ == "__main__":
    test_normal_operation()
