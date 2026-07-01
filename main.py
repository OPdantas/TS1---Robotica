import time
import numpy as np

from config import (
    URSIM_IP,
    CONTROL_FREQUENCY,
    DT,
    SIMULATION_TIME,
    DAMPING,
    MAX_JOINT_SPEED,
    DESIRED_CARTESIAN_VELOCITY
)

from ur10_kinematics import UR10Kinematics
from singularity_monitor import SingularityMonitor
from adaptive_controller import AdaptiveCartesianController
from data_logger import DataLogger


def connect_to_ursim(ip):
    """
    Tenta conectar ao URSim usando a biblioteca ur-rtde.

    Para instalar:
        pip install ur-rtde
    """
    try:
        import rtde_control
        import rtde_receive

        rtde_c = rtde_control.RTDEControlInterface(ip)
        rtde_r = rtde_receive.RTDEReceiveInterface(ip)

        print("[OK] Conectado ao URSim via RTDE.")
        return rtde_c, rtde_r

    except Exception as error:
        print("[AVISO] Não foi possível conectar ao URSim.")
        print(f"[DETALHE] {error}")
        print("[INFO] O programa será executado em modo de simulação local.")
        return None, None


def generate_local_joint_state(t):
    """
    Trajetória local projetada para aproximar o UR10 de uma região
    cinematicamente desfavorável, evidenciando a atuação do monitor
    de singularidades e do controlador adaptativo.

    A trajetória aproxima gradualmente as juntas 2 e 3 de uma postura
    mais estendida, condição típica de pior manipulabilidade.
    """

    # Progresso suave entre 0 e 1
    s = min(t / SIMULATION_TIME, 1.0)

    # Interpolação suave
    smooth = 3 * s**2 - 2 * s**3

    q_initial = np.array([
        0.0,
        -1.40,
        1.40,
        -1.20,
        1.00,
        0.0
    ])

    q_singular_region = np.array([
        0.0,
        -0.15,
        0.10,
        -0.05,
        0.05,
        0.0
    ])

    # Pequena oscilação para tornar os gráficos mais ricos
    oscillation = np.array([
        0.10 * np.sin(0.5 * t),
        0.05 * np.sin(0.4 * t),
        0.04 * np.cos(0.6 * t),
        0.04 * np.sin(0.7 * t),
        0.03 * np.cos(0.5 * t),
        0.05 * np.sin(0.8 * t)
    ])

    q = (1 - smooth) * q_initial + smooth * q_singular_region + oscillation

    return q


def get_joint_positions(rtde_r, t):
    """
    Lê as posições articulares reais do URSim.
    Caso não exista conexão, usa uma trajetória simulada local.
    """
    if rtde_r is not None:
        return np.array(rtde_r.getActualQ())

    return generate_local_joint_state(t)


def send_joint_speed(rtde_c, q_dot):
    """
    Envia velocidades articulares ao URSim usando speedJ.

    speedJ(qd, acceleration, time)
    """
    if rtde_c is not None:
        rtde_c.speedJ(q_dot.tolist(), 0.5, DT)


def stop_robot(rtde_c):
    """
    Interrompe o movimento do robô de forma segura.
    """
    if rtde_c is not None:
        rtde_c.speedStop()
        rtde_c.stopScript()


def main():
    print("==============================================")
    print("Sistema Jacobiano UR10 - Proteção e Controle")
    print("==============================================")

    kinematics = UR10Kinematics()
    monitor = SingularityMonitor()
    controller = AdaptiveCartesianController(
        damping=DAMPING,
        max_joint_speed=MAX_JOINT_SPEED
    )
    logger = DataLogger("dados_simulacao.csv")

    desired_velocity = np.array(DESIRED_CARTESIAN_VELOCITY)

    rtde_c, rtde_r = connect_to_ursim(URSIM_IP)

    start_time = time.time()
    next_cycle = start_time

    try:
        while True:
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time >= SIMULATION_TIME:
                print("[INFO] Tempo de simulação finalizado.")
                break

            q = get_joint_positions(rtde_r, elapsed_time)

            J = kinematics.geometric_jacobian(q)

            monitor_data = monitor.analyze(J)

            q_dot, adaptive_gain, condition_number = controller.compute_joint_velocity(
                J,
                desired_velocity
            )

            q_dot = q_dot * monitor_data["speed_factor"]

            logger.log(q, q_dot, monitor_data, adaptive_gain)

            print(
                f"t={elapsed_time:05.2f}s | "
                f"status={monitor_data['status']:8s} | "
                f"kappa={monitor_data['condition_number']:8.2f} | "
                f"manip={monitor_data['manipulability']:.6f} | "
                f"gain={adaptive_gain:.2f}"
            )

            if monitor_data["emergency_stop"]:
                print("[CRÍTICO] Singularidade severa detectada. Movimento interrompido.")
                stop_robot(rtde_c)
                break

            send_joint_speed(rtde_c, q_dot)

            next_cycle += DT
            sleep_time = next_cycle - time.time()

            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\n[INFO] Execução interrompida pelo usuário.")

    finally:
        stop_robot(rtde_c)
        logger.close()
        print("[OK] Sistema encerrado com segurança.")
        print("[OK] Dados salvos em dados_simulacao.csv.")


if __name__ == "__main__":
    main()