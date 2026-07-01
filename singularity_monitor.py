from jacobian_tools import JacobianTools


class SingularityMonitor:
    """
    Aplicação 1:
    Sistema de proteção ativa contra singularidades.
    """

    def __init__(self):
        self.tools = JacobianTools()

    def analyze(self, J):
        condition = self.tools.condition_number(J)
        manipulability = self.tools.manipulability(J)
        singular_values = self.tools.singular_values(J)
        status = self.tools.classify_condition(condition)
        speed_factor = self.get_speed_factor(status)

        emergency_stop = status == "CRITICAL"

        return {
            "condition_number": condition,
            "manipulability": manipulability,
            "sigma_min": min(singular_values),
            "sigma_max": max(singular_values),
            "status": status,
            "speed_factor": speed_factor,
            "emergency_stop": emergency_stop
        }

    def get_speed_factor(self, status):
        if status == "NORMAL":
            return 1.0

        if status == "WARNING":
            return 0.60

        if status == "RISK":
            return 0.25

        if status == "CRITICAL":
            return 0.0

        return 0.0