from random import randrange
import re
import numpy as np, matplotlib.pyplot as plt
import eel
from math import pi


class State:
    def __init__(self, c=1.65, k=0.59, R=5, uc=0, l=0.5, alpha=0.003, T=40, I=64, K=64*64) -> None:
        self.c = c
        self.k = k
        self.R = R
        self.uc = uc
        self.l = l
        self.alpha = alpha
        self.T = T
        self.I = I
        self.K = K

        self.t = np.linspace(0, T, K + 1)
        self.theta = np.linspace(0.001, pi-0.001, I + 1)

        self.h_t = self.t[2] - self.t[1]
        self.h_theta = self.theta[2] - self.theta[1]

    def psi(self, theta):
        return self.uc + np.cos(theta) ** 4


class Implicits:
    def __init__(self, state) -> None:
        self.state = state

        self.A = self.state.k / (self.state.c * self.state.R ** 2)
        self.B = self.state.alpha / (self.state.c * self.state.l)

        self.gam = - self.A * self.state.h_t / (self.state.h_theta ** 2) * (1 + self.state.h_theta / (2 * np.tan(self.state.theta[:-1])))
        self.eps = - self.A * self.state.h_t / (self.state.h_theta ** 2) * (1 - self.state.h_theta / (2 * np.tan(self.state.theta[1:])))
        self.eta = self.B * self.state.h_t * self.state.uc

        sigma = - 2 * self.A * self.state.h_t / (self.state.h_theta ** 2)

        self.beta = (self.B * self.state.h_t + 2 * self.A * self.state.h_t / (self.state.h_theta ** 2) + 1) * np.ones(self.state.I + 1)
        self.eps[-1] = sigma
        self.gam[0] = sigma

    def tri_diag_solver_right(self, a, c, b, f):
        n = c.size
        k = n - 1
        alpha = np.zeros(k)
        beta = np.zeros(k)
        x = np.zeros(n)
        
        alpha[0] = - b[0] / c[0]
        beta[0] = f[0] / c[0]
        
        for ind in range(1, k):
            alpha[ind] = - b[ind] / (a[ind - 1] * alpha[ind - 1] + c[ind])
            beta[ind] = (f[ind] - a[ind - 1] * beta[ind - 1]) / (a[ind - 1] * alpha[ind - 1] + c[ind])
            
        x[-1] = (f[-1] - a[-1] * beta[-1]) / (a[-1] * alpha[-1] + c[-1])
        
        for ind in range(n - 2, -1, -1):
            x[ind] = alpha[ind] * x[ind + 1] + beta[ind]
        return x

    def solve(self):
        # matrix = np.diag(self.beta) + np.diag(self.eps, -1) + np.diag(self.gam, 1) # для м. м.

        v = np.zeros([self.state.K + 1, self.state.I + 1])
        v[0, :] = self.state.psi(self.state.theta)

        for k_ind in range(1, self.state.K+1):
            eel.setProgress(round((1 - (self.state.K - k_ind + 1) / self.state.K) * 100, 0))
            # v[k_ind, :] = np.linalg.inv(matrix) @ v[k_ind - 1, :] # матричный метод (медленный в 40 раз менее производительный)
            v[k_ind, :] = self.tri_diag_solver_right(self.eps, self.beta, self.gam, v[k_ind - 1, :])
        return v, self.state.theta, self.state.t


class GFTool:
    def __init__(self, solution, theta_array, time_array) -> None:
        # solution - матрица, представляющая из себя решение
        self.v = solution
        self.theta_array = theta_array
        self.time_array = time_array
        [self.K, self.I] = solution.shape

    def plot_solution(self):
        f = plt.figure(figsize=[12, 6])
        plt.plot(self.theta_array, self.v[0, :], lw=4, c='black', label='t=0')
        for coef in [1/4, 1/2, 3/4, 1]:
            plt.plot(self.theta_array, self.v[int((self.K - 1) * coef), :], lw=4, label='t='+str(self.time_array[int((self.K - 1) * coef)]))

        plt.xlim([self.theta_array[1], self.theta_array[-1]])
        plt.xlabel('${\\theta}$', fontsize=20)
        plt.ylabel('${v(\\theta)}$', fontsize=20)
        plt.xticks([0, pi/4, pi/2, 3*pi/4, pi], ['0', '$\\pi / 4$', '$\\pi / 2$', '$3 \\pi / 4$', '$\\pi$'], fontsize=20)
        # plt.yticks([0, 0.5, 1], ['0', '0.5', '1'], fontsize=20)
        plt.legend()
        plt.grid()
        plt.show()

    def plot_image(self):
        f = plt.figure(figsize=[4, 3])
        plt.imshow(self.v)
        plt.show()


class Explicits:
    def __init__(self, state) -> None:
        self.state = state

        self.gam = state.k * state.h_t / (state.R ** 2) / state.c / (state.h_theta ** 2)
        self.beta = state.alpha * state.h_t / state.l / state.c
        self.omega = state.k * state.h_t / (state.R ** 2) / np.tan(state.theta) / 2 / state.h_theta / state.c

    def solve(self):
        v = np.zeros([self.state.K + 1, self.state.I + 1])
        v[0, :] = self.state.psi(self.state.theta)

        for k_ind in range(1, self.state.K + 1):
            eel.setProgress(round((1 - (self.state.K - k_ind + 1) / self.state.K) * 100, 0))
            v[k_ind, 0] = (1 - self.beta - 2 * self.gam) * v[k_ind - 1, 0] + 2 * self.gam * (v[k_ind - 1, 1])
            for i_ind in range(1, self.state.I):
                v[k_ind, i_ind] = (1 - 2 * self.gam - self.beta) * v[k_ind - 1, i_ind] + (self.omega[i_ind] + self.gam) * v[k_ind - 1, i_ind + 1] + (self.gam - self.omega[i_ind]) * v[k_ind - 1, i_ind - 1]
            v[k_ind, self.state.I] = (1 - self.beta - 2 * self.gam) * v[k_ind - 1, self.state.I] + 2 * self.gam * (v[k_ind - 1, self.state.I - 1])

        return v, self.state.theta, self.state.t
