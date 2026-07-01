import numpy as np


class UR10Kinematics:
    """
    Modelo cinemático aproximado do robô UR10.
    Responsável por calcular:
    - matrizes de transformação homogênea;
    - cinemática direta;
    - Jacobiano Geométrico 6x6.
    """

    def __init__(self):
        # Parâmetros DH aproximados do UR10 em metros
        # Cada linha representa: [a, alpha, d, theta_offset]
        self.dh_params = np.array([
            [0.0,        np.pi / 2,  0.1273, 0.0],
            [-0.612,     0.0,        0.0,    0.0],
            [-0.5723,    0.0,        0.0,    0.0],
            [0.0,        np.pi / 2,  0.163941, 0.0],
            [0.0,       -np.pi / 2,  0.1157, 0.0],
            [0.0,        0.0,        0.0922, 0.0],
        ])

    def dh_transform(self, a, alpha, d, theta):
        """
        Calcula a matriz homogênea usando a convenção DH clássica.
        """
        ct = np.cos(theta)
        st = np.sin(theta)
        ca = np.cos(alpha)
        sa = np.sin(alpha)

        return np.array([
            [ct, -st * ca,  st * sa, a * ct],
            [st,  ct * ca, -ct * sa, a * st],
            [0.0, sa,       ca,      d],
            [0.0, 0.0,      0.0,     1.0]
        ])

    def forward_kinematics(self, q):
        """
        Calcula a cinemática direta do UR10.

        Parâmetro:
            q: vetor de juntas [q1, q2, q3, q4, q5, q6] em radianos.

        Retorna:
            T_0_6: matriz homogênea do efetuador final.
            transformations: lista com as transformações intermediárias.
        """
        T = np.eye(4)
        transformations = [T.copy()]

        for i in range(6):
            a, alpha, d, theta_offset = self.dh_params[i]
            theta = q[i] + theta_offset

            A_i = self.dh_transform(a, alpha, d, theta)
            T = T @ A_i
            transformations.append(T.copy())

        return T, transformations

    def geometric_jacobian(self, q):
        """
        Calcula o Jacobiano Geométrico 6x6.

        Parte linear:
            Jv_i = z_i x (o_n - o_i)

        Parte angular:
            Jw_i = z_i

        Retorna:
            J: matriz Jacobiana 6x6.
        """
        T_0_6, transformations = self.forward_kinematics(q)

        o_n = T_0_6[0:3, 3]
        J = np.zeros((6, 6))

        for i in range(6):
            T_i = transformations[i]

            z_i = T_i[0:3, 2]
            o_i = T_i[0:3, 3]

            J_v = np.cross(z_i, o_n - o_i)
            J_w = z_i

            J[0:3, i] = J_v
            J[3:6, i] = J_w

        return J

    def tcp_position(self, q):
        """
        Retorna apenas a posição cartesiana do TCP.
        """
        T, _ = self.forward_kinematics(q)
        return T[0:3, 3]