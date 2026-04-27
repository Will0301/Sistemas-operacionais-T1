import matplotlib.pyplot as plt
import numpy as np

N = np.array([2, 4, 8])

# =========================
# DADOS x86
# =========================
T1_x86 = np.array([0.97, 0.31, 0.19])
T2_x86 = np.array([7.9, 15.3, 15.0])
P1_x86 = np.array([0.71, 0.39, 0.25])
P2_x86 = np.array([81.56, 90.72, 135.55])  # segundos

# =========================
# DADOS ARM
# =========================
T1_arm = np.array([0.736, 0.315, 0.187])
T2_arm = np.array([8.077, 16.632, 15.163])
P1_arm = np.array([0.732, 0.340, 0.212])
P2_arm = np.array([3067.7, 2323.0, 3292.94])  # segundos

# =========================
# FUNÇÃO DE PLOT
# =========================
def plot_graph(T1, T2, P1, P2, title, filename):
    plt.figure(figsize=(10, 6))

    plt.plot(N, T1, 'o-', linewidth=2, label='T1 - Threads (sem mutex)')
    plt.plot(N, T2, 'o-', linewidth=2, label='T2 - Threads (mutex)')
    plt.plot(N, P1, 'o-', linewidth=2, label='P1 - Processos (sem sync)')
    plt.plot(N, P2, 'o-', linewidth=2, label='P2 - Processos (semáforo)')

    # Tendência
    def tendencia(x, y):
        coef = np.polyfit(x, y, 1)
        poly = np.poly1d(coef)
        return poly(x)

    plt.plot(N, tendencia(N, T1), '--', alpha=0.5)
    plt.plot(N, tendencia(N, T2), '--', alpha=0.5)
    plt.plot(N, tendencia(N, P1), '--', alpha=0.5)
    plt.plot(N, tendencia(N, P2), '--', alpha=0.5)

    # Labels
    for x, y in zip(N, T1):
        plt.text(x, y, f"{y:.2f}s", ha='center', va='bottom')

    for x, y in zip(N, T2):
        plt.text(x, y, f"{y:.1f}s", ha='center', va='bottom')

    for x, y in zip(N, P1):
        plt.text(x, y, f"{y:.2f}s", ha='center', va='bottom')

    for x, y in zip(N, P2):
        plt.text(x, y, f"{y/60:.1f}m", ha='center', va='bottom')  # minutos

    plt.yscale('log')

    plt.title(title)
    plt.xlabel('Número de Workers (N)')
    plt.ylabel('Tempo de Execução (escala log)')

    plt.xticks(N)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()

# =========================
# GERAR GRÁFICOS
# =========================
plot_graph(T1_x86, T2_x86, P1_x86, P2_x86,
           'Escalabilidade - x86',
           'grafico_x86.png')

plot_graph(T1_arm, T2_arm, P1_arm, P2_arm,
           'Escalabilidade - ARM',
           'grafico_arm.png')