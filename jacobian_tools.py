import numpy as np


class JacobianTools:
    """
    Ferramentas matemáticas para análise do Jacobiano.
    """

    @staticmethod
    def singular_values(J):
        return np.linalg.svd(J, compute_uv=False)

    @staticmethod
    def condition_number(J, epsilon=1e-9):
        s = JacobianTools.singular_values(J)
        sigma_max = np.max(s)
        sigma_min = np.min(s)

        if sigma_min < epsilon:
            return np.inf

        return sigma_max / sigma_min

    @staticmethod
    def manipulability(J):
        value = np.linalg.det(J @ J.T)

        if value < 0:
            value = 0.0

        return np.sqrt(value)

    @staticmethod
    def pseudo_inverse(J, damping=0.01):
        m, _ = J.shape
        identity = np.eye(m)

        return J.T @ np.linalg.inv(J @ J.T + (damping ** 2) * identity)

    @staticmethod
    def classify_condition(condition_number):
        """
        Limiares ajustados para demonstrar a atuação do sistema
        durante o cenário de teste próximo a singularidades.
        """
        if condition_number < 8:
            return "NORMAL"
        elif condition_number < 9:
            return "WARNING"
        elif condition_number < 10:
            return "RISK"
        else:
            return "CRITICAL"