import matplotlib.pyplot as plt
import numpy as np

N = np.array([2, 4, 8])

T1 = np.array([0.97, 0.31, 0.19])
T2 = np.array([7.9, 15.3, 15.0])
P1 = np.array([0.71, 0.39, 0.25])

plt.figure(figsize=(10, 6))

# Linhas principais
plt.plot(N, T1, 'o-', linewidth=2, label='T1 - Threads (sem mutex)', color='#1f77b4')
plt.plot(N, T2, 'o-', linewidth=2, label='T2 - Threads (mutex)', color='#ff7f0e')
plt.plot(N, P1, 'o-', linewidth=2, label='P1 - Processos (sem sync)', color='#2ca02c')

# 🔮 Tendência (agora com legenda!)
def tendencia(x, y):
    coef = np.polyfit(x, y, 1)
    poly = np.poly1d(coef)
    return poly(x)

plt.plot(N, tendencia(N, T1), '--', alpha=0.6, label='Tendência T1')
plt.plot(N, tendencia(N, T2), '--', alpha=0.6, label='Tendência T2')
plt.plot(N, tendencia(N, P1), '--', alpha=0.6, label='Tendência P1')

# 📌 Labels nos pontos
for x, y in zip(N, T1):
    plt.text(x, y + 0.05, f"{y:.2f}s", ha='center')

for x, y in zip(N, T2):
    plt.text(x, y + 0.3, f"{y:.1f}s", ha='center')

for x, y in zip(N, P1):
    plt.text(x, y - 0.08, f"{y:.2f}s", ha='center')

# 🔥 SOLUÇÃO PRA VISUAL:
plt.yscale('log')  # 👈 resolve o problema das linhas esmagadas

plt.title('Escalabilidade: Threads vs Processos', fontsize=14)
plt.xlabel('Número de Workers (N)')
plt.ylabel('Tempo de Execução (segundos - escala log)')

plt.xticks(N)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()

plt.tight_layout()
plt.savefig("grafico_escalabilidade_log.png", dpi=300)
plt.show()