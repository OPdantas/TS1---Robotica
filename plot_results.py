import os
import pandas as pd
import matplotlib.pyplot as plt


def create_output_folder(folder="figuras"):
    if not os.path.exists(folder):
        os.makedirs(folder)


def plot_condition_number(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df["time"], df["condition_number"])
    plt.xlabel("Tempo (s)")
    plt.ylabel("Número de Condição")
    plt.title("Evolução do Número de Condição do Jacobiano")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figuras/numero_condicao.png", dpi=300)
    plt.close()


def plot_manipulability(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df["time"], df["manipulability"])
    plt.xlabel("Tempo (s)")
    plt.ylabel("Manipulabilidade")
    plt.title("Índice de Manipulabilidade de Yoshikawa")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figuras/manipulabilidade.png", dpi=300)
    plt.close()


def plot_singular_values(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df["time"], df["sigma_min"], label="sigma_min")
    plt.plot(df["time"], df["sigma_max"], label="sigma_max")
    plt.xlabel("Tempo (s)")
    plt.ylabel("Valor Singular")
    plt.title("Valores Singulares do Jacobiano")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figuras/valores_singulares.png", dpi=300)
    plt.close()


def plot_adaptive_gain(df):
    plt.figure(figsize=(10, 5))
    plt.plot(df["time"], df["adaptive_gain"])
    plt.xlabel("Tempo (s)")
    plt.ylabel("Ganho Adaptativo")
    plt.title("Ganho Adaptativo em Função do Condicionamento")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figuras/ganho_adaptativo.png", dpi=300)
    plt.close()


def plot_joint_velocities(df):
    plt.figure(figsize=(10, 5))

    for joint in ["qd1", "qd2", "qd3", "qd4", "qd5", "qd6"]:
        plt.plot(df["time"], df[joint], label=joint)

    plt.xlabel("Tempo (s)")
    plt.ylabel("Velocidade Articular (rad/s)")
    plt.title("Velocidades Articulares Calculadas pelo Controlador")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figuras/velocidades_articulares.png", dpi=300)
    plt.close()


def plot_status_distribution(df):
    status_counts = df["status"].value_counts()

    plt.figure(figsize=(7, 5))
    plt.bar(status_counts.index, status_counts.values)
    plt.xlabel("Estado Operacional")
    plt.ylabel("Quantidade de Amostras")
    plt.title("Distribuição dos Estados de Risco")
    plt.grid(axis="y")
    plt.tight_layout()
    plt.savefig("figuras/distribuicao_status.png", dpi=300)
    plt.close()


def main():
    create_output_folder()

    csv_file = "dados_simulacao.csv"

    if not os.path.exists(csv_file):
        print("[ERRO] Arquivo dados_simulacao.csv não encontrado.")
        print("[INFO] Execute primeiro o arquivo main.py.")
        return

    df = pd.read_csv(csv_file)

    plot_condition_number(df)
    plot_manipulability(df)
    plot_singular_values(df)
    plot_adaptive_gain(df)
    plot_joint_velocities(df)
    plot_status_distribution(df)

    print("[OK] Gráficos gerados na pasta figuras/")


if __name__ == "__main__":
    main()