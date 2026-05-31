import numpy as np

def gbm(S_0=100, r=0.035, sigma=0.2, T=1, steps=252,
                n_sim=10000, Z=None, rng=None, return_paths=True):

    dt = T/steps

    if Z is None:
        if rng is None:
            rng = np.random.default_rng(42)
        Z = rng.standard_normal((n_sim, steps))

    drift = (r - 0.5 * sigma**2) * dt
    diffusion = sigma * np.sqrt(dt) * Z
    log_returns = drift + diffusion

    log_S = np.cumsum(log_returns, axis=1)
    log_S = np.hstack([np.zeros((n_sim, 1)), log_S])

    S = S_0 * np.exp(log_S)

    if return_paths:
        return S
    else:
        return S[:, -1]

