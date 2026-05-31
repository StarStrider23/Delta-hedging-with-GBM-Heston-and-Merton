import numpy as np

# Feller condition: 2 * kappa * theta > xi^2

def heston(S_0=100, v_0=0.04, r=0.035, T=1, rho=-0.7, xi=0.3, 
           theta=0.04, kappa=1.5, steps=252, n_sim=10000, return_paths = True):

    dt = T/steps

    S = np.zeros((n_sim, steps + 1))
    S[:, 0] = S_0

    v = np.zeros((n_sim, steps + 1))
    v[:, 0] = v_0

    rng = np.random.default_rng(42)

    for i in range(1, steps + 1):

        Z1 = rng.standard_normal(n_sim)
        Z2 = rng.standard_normal(n_sim)

        Z_S = Z1
        Z_v = rho * Z1 + np.sqrt(1 - rho**2) * Z2

        v[:, i] = v[:, i-1] + kappa * (theta - v[:, i-1]) * dt + xi * np.sqrt(v[:, i-1] * dt) * Z_v
        v[:, i] = np.maximum(v[:, i], 0)

        S[:, i] = S[:, i-1] * np.exp((r - 0.5 * v[:, i-1]) * dt + np.sqrt(v[:, i-1] * dt) * Z_S)

    if return_paths:
        return S
    else:
        return S[:, -1]