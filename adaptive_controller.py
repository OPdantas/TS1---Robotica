import numpy as np
from jacobian_tools import JacobianTools


class AdaptiveCartesianController:
    """
    Aplicação 2:
    Controle cartesiano adaptativo baseado na pseudo-inversa amortecida
    do Jacobiano.
    """

    def __init__(self, damping=0.03, max_joint_speed=0.8):
        self.damping = damping
        self.max_joint_speed = max_joint_speed
        self.tools = JacobianTools()

    def adaptive_gain(self, condition_number):
        if condition_number < 8:
            return 1.0

        if condition_number < 9:
            return 0.6

        if condition_number < 10:
            return 0.25

        return 0.0

    def compute_joint_velocity(self, J, desired_cartesian_velocity):
        condition_number = self.tools.condition_number(J)
        gain = self.adaptive_gain(condition_number)

        J_pinv = self.tools.pseudo_inverse(J, damping=self.damping)

        q_dot = gain * (J_pinv @ desired_cartesian_velocity)

        q_dot = self.limit_joint_speed(q_dot)

        return q_dot, gain, condition_number

    def limit_joint_speed(self, q_dot):
        return np.clip(q_dot, -self.max_joint_speed, self.max_joint_speed)