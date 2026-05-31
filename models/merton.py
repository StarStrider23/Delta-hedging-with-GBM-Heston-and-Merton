import numpy as np

def merton(S_0=100, sigma=0.2, r=0.035, T=1, lambda_jump=1, mu_jump=-0.05, 
           sigma_jump=0.1, steps=252, n_sim=10000, return_paths = True):
    
    dt = T/steps

    S = np.zeros((n_sim, steps+1))
    S[:, 0] = S_0

    rng = np.random.default_rng(42)

    k = np.exp(mu_jump + sigma_jump**2/2) - 1

    Z = rng.standard_normal((n_sim, steps))

    Z_jump = rng.standard_normal((n_sim, steps))

    N = rng.poisson(lambda_jump * dt, (n_sim, steps))

    drift = (r - lambda_jump * k - sigma**2/2) * dt
    diffusion = sigma * np.sqrt(dt) * Z
    jumps = N * mu_jump + np.sqrt(N) * sigma_jump * Z_jump

    log_returns = drift + diffusion + jumps

    log_S = np.cumsum(log_returns, axis=1)
    log_S = np.hstack([np.zeros((n_sim, 1)), log_S])

    S = S_0 * np.exp(log_S)

    if return_paths:
        return S
    else:
        return S[:, -1]
    