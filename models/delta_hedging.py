import numpy as np

from models.black_scholes import BlackScholes

from models.gbm import gbm
from models.heston import heston
from models.merton import merton

def delta_hedging(model, steps=252, n_sim=10000):

    S_0 = model['S_0']
    r = model['r']
    sigma = model['sigma']
    T = model['T']

    K = model['K']

    dt = 1/steps

    if model['model'] == gbm:
        S = gbm(S_0=S_0, r=r, sigma=sigma, T=T, steps=steps, n_sim=n_sim)

    elif model['model'] == heston:
        v_0 = model['v_0'] 
        rho = model['rho'] 
        xi = model['xi']
        theta = model['theta']
        kappa = model['kappa']
    
        S = heston(S_0=S_0, v_0=v_0, r=r, T=T, rho=rho, xi=xi, 
           theta=theta, kappa=kappa, steps=steps, n_sim=n_sim)
        
    elif model['model'] == merton:
        lambda_jump = model['lambda_jump']
        mu_jump = model['mu_jump'] 
        sigma_jump = model['sigma_jump']

        S = merton(S_0=S_0, sigma=sigma, r=r, T=T, lambda_jump=lambda_jump, 
                   mu_jump=mu_jump, sigma_jump=sigma_jump, steps=steps, n_sim=n_sim)
        
    else:
        raise ValueError('Please, enter a valid model: gbm, heston or merton')

    bs = BlackScholes(S_0, K, r, sigma, T)
    V_0 = bs.option_price(option="call")
    delta_0 = bs.compute_delta(option="call")

    B_0 = V_0 - delta_0 * S_0

    B = np.zeros((n_sim, steps+1))
    B[:, 0] = B_0

    t = np.linspace(0, T, steps+1)
    tau = T - t
    tau[-1] = 1e-10

    bs = BlackScholes(S=S, K=K, r=r, sigma=sigma, T=tau)
    delta = bs.compute_delta(option="call")
    opt_price = bs.option_price(option="call")

    pnl_paths = np.zeros((n_sim, steps+1))

    portfolio_value = np.zeros((n_sim, steps+1))
    portfolio_value[:, 0] = delta_0 * S_0 + B_0

    for i in range(1, steps+1):
        B[:, i] = B[:, i-1] * np.exp(r * dt)
        B[:, i] -= (delta[:, i] - delta[:, i-1]) * S[:, i]
        
        portfolio_value[:, i] = delta[:, i] * S[:, i] + B[:, i]

    pnl_paths = portfolio_value - opt_price
    
    return pnl_paths