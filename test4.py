
import time
import numpy as np

from mission_controller.mission_controller import MissionController, CustomError
from mission_controller.simulated_robot import SimulatedRobot, SimulatedRobotWithCommunicationDelay

# checking the custom error

def test_normal_operation():

    print("Test3 : checking the custom error")

    simulated_robot = SimulatedRobotWithCommunicationDelay(np.array([2.0,1.0]))

    try:
        controller = MissionController("robot")
    except CustomError as error:
        print("---ERROR :",error,"---")
        exit(1)

    controller = MissionController(simulated_robot)

    # set the first trajectory

    controller.set_trajectory(np.array([[4.0,3.0], [5.0, 3.0]]))
    
    controller.finish_flag.wait()

    controller.set_trajectory(np.array([[3.0,3.0], [5.0, 4.0]]))

    controller.join()

    print("Test4 complete")

    exit(0)


if __name__ == "__main__":
    test_normal_operation()
