import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

omega_f = 23.4 # generator angular frequency
A = 0.034 # generator amplitude
gamma = 0.25 # vibration damping coefficient
omega_2 = 110 / 0.011 # omega_2 = k / M

M = np.eye(12) * (-gamma)

for i in range(1, 12, 2):
    M[i][i - 1] = 1

for i in range(2, 10, 2):
    M[i][i - 1] = omega_2
    M[i][i + 1] = -2 * omega_2
    M[i][i + 3] = omega_2

M[0][1] = -2 * omega_2
M[0][3] = omega_2
M[10][9] = omega_2
M[10][11] = -2 * omega_2


def deriv_u(u, t):
    return M @ u + np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, A * np.sin(omega_f * t), 0])

# array of initial conditions (even - u_i, odd - u_i derivative)
u0 = np.zeros(12)
#u0 = np.array([0, 0.075, 0, 0.075 * 2, 0, 0.075 * 3, 0, 0.075 * 4, 0, 0.075 * 5, 0, 0.075 * 6])

t = np.linspace(22, 25, 100000)
u = odeint(deriv_u, u0, t)


u_ = [[u[i][k] for i in range(len(u))] for k in range(1, 12, 2)]
n = len(t) // 20

#plt.scatter([u_[i+1][n] - u_[i][n] for i in range(5)], [(u_[i+1][n] - u_[i][n]) /2 for i in range(5)])
#plt.show()

plt.figure(figsize=(12, 10))
for u_i in u_[:2]:
    plt.plot(t, np.array(u_i) * np.e**6 * 10000 / 3.7)
plt.legend(['1', '2'])
plt.plot(t, 0 * t)
plt.xlabel('Time, seconds')
plt.ylabel('U(t), centimeters')
plt.show()