import csv
import time


class DataLogger:
    """
    Registrador robusto de dados da simulação.
    Abre o arquivo uma única vez, grava em UTF-8 e fecha corretamente no final.
    """

    def __init__(self, filename="dados_simulacao.csv"):
        self.filename = filename
        self.start_time = time.time()

        self.file = open(self.filename, mode="w", newline="", encoding="utf-8")
        self.writer = csv.writer(self.file)

        self.header = [
            "time",
            "q1", "q2", "q3", "q4", "q5", "q6",
            "qd1", "qd2", "qd3", "qd4", "qd5", "qd6",
            "condition_number",
            "manipulability",
            "sigma_min",
            "sigma_max",
            "status",
            "speed_factor",
            "adaptive_gain"
        ]

        self.writer.writerow(self.header)
        self.file.flush()

    def log(self, q, q_dot, monitor_data, adaptive_gain):
        current_time = time.time() - self.start_time

        row = [
            current_time,
            q[0], q[1], q[2], q[3], q[4], q[5],
            q_dot[0], q_dot[1], q_dot[2], q_dot[3], q_dot[4], q_dot[5],
            monitor_data["condition_number"],
            monitor_data["manipulability"],
            monitor_data["sigma_min"],
            monitor_data["sigma_max"],
            monitor_data["status"],
            monitor_data["speed_factor"],
            adaptive_gain
        ]

        self.writer.writerow(row)
        self.file.flush()

    def close(self):
        if not self.file.closed:
            self.file.flush()
            self.file.close()