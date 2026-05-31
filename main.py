import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

from models.gbm import gbm
from models.delta_hedging import delta_hedging
from models.heston import heston
from models.merton import merton

gbm = {'model' : gbm, 'S_0' : 100, 'r' : 0.035, 'sigma' : 0.2, 'T' : 1, 'K' : 100}

heston = {'model' : heston, 'S_0' : 100, 'v_0' : 0.04, 'r' : 0.035, 'T' : 1, 'rho' : -0.7, 
          'xi' : 0.3, 'theta' : 0.04, 'kappa' : 1.5, 'K' : 100, 'sigma' : 0.2}

merton = {'model' : merton, 'S_0' : 100, 'sigma' : 0.2, 'r' : 0.035, 'T' : 1, 
          'lambda_jump' : 1, 'mu_jump' : -0.05, 'sigma_jump' : 0.1, 'K' : 100}

#Rolling mean and std

steps = 252
n_days = np.arange(0, steps+1)

pnl_paths_gbm = delta_hedging(model=gbm)
std_gbm = np.std(pnl_paths_gbm[:, -1])
mean_gbm = np.mean(pnl_paths_gbm[:, -1])

pnl_paths_h = delta_hedging(model=heston)
std_h = np.std(pnl_paths_h[:, -1])
mean_h = np.mean(pnl_paths_h[:, -1])

pnl_paths_m = delta_hedging(model=merton)
std_m = np.std(pnl_paths_m[:, -1])
mean_m = np.mean(pnl_paths_m[:, -1])

print(f"GBM. PnL mean is {mean_gbm}, PnL std is {std_gbm}")
print(f"Heston. PnL mean is {mean_h}, PnL std is {std_h}")
print(f"Merton. PnL mean is {mean_m}, PnL std is {std_m}")

accum_gbm_mean = np.mean(pnl_paths_gbm, axis=0)
accum_h_mean = np.mean(pnl_paths_h, axis=0)
accum_m_mean = np.mean(pnl_paths_m, axis=0)

plt.figure(figsize=(12,6))
plt.plot(n_days, accum_gbm_mean, color='blue', label='GBM')
plt.plot(n_days, accum_h_mean, color='green', label='Heston')
plt.plot(n_days, accum_m_mean, color='red', label='Merton')
plt.title('PnL Average over Time')
plt.xlabel('Marketing Days')
plt.ylabel('PnL Average')
plt.grid(True, alpha=0.2, color = "grey", ls='--', lw = 1,)
plt.legend(loc="lower left")
plt.show()

# Skew, kurtosis, VaR, ES

pnl_gbm = pnl_paths_gbm[:, -1]
pnl_h = pnl_paths_h[:, -1]
pnl_m = pnl_paths_m[:, -1]

skew_gbm = stats.skew(pnl_gbm)
k_gbm = stats.kurtosis(pnl_gbm)

skew_h = stats.skew(pnl_h)
k_h = stats.kurtosis(pnl_h)

skew_m = stats.skew(pnl_m)
k_m = stats.kurtosis(pnl_m)

print(f"GBM. Skewness: {skew_gbm}, kurtosis: {k_gbm}")
print(f"Heston. Skewness: {skew_h}, kurtosis: {k_h}")
print(f"Merton. Skewness: {skew_m}, kurtosis: {k_m}")

var99_gbm = np.percentile(pnl_gbm, 1)
es99_gbm = np.mean(pnl_gbm[pnl_gbm <= var99_gbm])

var99_h = np.percentile(pnl_h, 1)
es99_h = np.mean(pnl_h[pnl_h <= var99_h])

var99_m = np.percentile(pnl_m, 1)
es99_m = np.mean(pnl_m[pnl_m <= var99_m])

print(f"GBM. VaR99: {var99_gbm}, ES99: {es99_gbm}")
print(f"Heston. VaR99: {var99_h}, ES99: {es99_h}")
print(f"Merton. VaR99: {var99_m}, ES99: {es99_m}")

plt.figure(figsize=(12,6))
plt.hist(pnl_gbm, bins=100, density=True, color='blue', alpha=0.5, label='GBM')
plt.hist(pnl_h, bins=100, density=True, color='green', alpha=0.5, label='Heston')
plt.hist(pnl_m, bins=100, density=True, color='red', alpha=0.5, label='Merton')
plt.grid(True, alpha=0.2, color = "grey", ls='--', lw = 1,)
plt.title('PnL Distribution')
plt.xlabel('PnL')
plt.legend()
plt.show()

# Hedging frequency

steps_list = [10, 25, 50, 100, 252, 500]

gbm_steps_std = [np.std(delta_hedging(model=gbm, steps=s)[:, -1]) for s in steps_list]
h_steps_std = [np.std(delta_hedging(model=heston, steps=s)[:, -1]) for s in steps_list]
m_steps_std = [np.std(delta_hedging(model=merton, steps=s)[:, -1]) for s in steps_list]

plt.figure(figsize=(12,6))
plt.plot(steps_list, gbm_steps_std, color='blue', label='GBM')
plt.plot(steps_list, h_steps_std, color='green', label='Heston')
plt.plot(steps_list, m_steps_std, color='red', label='Merton')
plt.xlabel("Number of Hedging Steps")
plt.ylabel("Std of Hedging Error")
plt.title("Hedging Error vs Rebalancing Frequency")
plt.grid(True, alpha=0.2, color = "grey", ls='--', lw = 1,)
plt.legend()
plt.show()

# Heston. Parameter Sensitivity Tests

# Xi vs Std(PnL)

xi = [0.1, 0.2, 0.3, 0.4, 0.5]
pnl_xi = [delta_hedging(model={**heston, "xi" : x}) for x in xi]
std_xi = [np.std(pnl_x) for pnl_x in pnl_xi]

heston['xi'] = 0.3

plt.figure(figsize=(12,6))
plt.plot(xi, std_xi, color='green')
plt.xlabel("Xi")
plt.ylabel("std(PnL)")
plt.title("Heston Model. Vol-of-vol vs PnL std")
plt.grid(True, alpha=0.2, color = "grey", ls='--', lw = 1,)
plt.show()

# Xi vs VaR/ES

var99_xi = [np.percentile(pnl, 1) for pnl in pnl_xi]
es99_xi = [np.mean(pnl[pnl <= var]) for pnl, var in zip(pnl_xi, var99_xi)]

plt.figure(figsize=(12,6))
plt.plot(xi, es99_xi, color='blue', label='ES')
plt.plot(xi, var99_xi, color='red', label='VaR')
plt.xlabel("Xi")
plt.ylabel("VaR and ES")
plt.title("Heston Model. Vol-of-vol vs ES99 and VaR99")
plt.grid(True, alpha=0.2, color = "grey", ls='--', lw = 1,)
plt.legend()
plt.show()

# Rho vs kurtosis and VaR/ES

rho = [0.9, 0.6, 0.3, -0.3, -0.6, -0.9]

pnl_rho = [delta_hedging(model={**heston, "rho" : r})[:, -1] for r in rho]
k_rho = [stats.kurtosis(pnl_r) for pnl_r in pnl_rho]
sk_rho = [stats.skew(pnl_r) for pnl_r in pnl_rho]

heston['rho'] = -0.7

fig, ax = plt.subplots(2, 3, figsize=(15, 8))
fig.suptitle('Correlation vs PnL distribution')
ax[0,0].hist(pnl_rho[0], bins=100, density=True); ax[0,0].set_title(f"rho {rho[0]}: kurtosis {k_rho[0]:.2f}, skewness {sk_rho[0]:.2f}")
ax[0,1].hist(pnl_rho[1], bins=100, density=True); ax[0,1].set_title(f"rho {rho[1]}: kurtosis {k_rho[1]:.2f}, skewness {sk_rho[1]:.2f}")
ax[0,2].hist(pnl_rho[2], bins=100, density=True); ax[0,2].set_title(f"rho {rho[2]}: kurtosis {k_rho[2]:.2f}, skewness {sk_rho[2]:.2f}")
ax[1,0].hist(pnl_rho[3], bins=100, density=True); ax[1,0].set_title(f"rho {rho[3]}: kurtosis {k_rho[3]:.2f}, skewness {sk_rho[3]:.2f}")
ax[1,1].hist(pnl_rho[4], bins=100, density=True); ax[1,1].set_title(f"rho {rho[4]}: kurtosis {k_rho[4]:.2f}, skewness {sk_rho[4]:.2f}")
ax[1,2].hist(pnl_rho[5], bins=100, density=True); ax[1,2].set_title(f"rho {rho[5]}: kurtosis {k_rho[5]:.2f}, skewness {sk_rho[5]:.2f}")
plt.show()

var99_rho = [np.percentile(pnl, 1) for pnl in pnl_rho]
es99_rho = [np.mean(pnl[pnl <= var]) for pnl, var in zip(pnl_rho, var99_rho)]

plt.figure(figsize=(12,6))
plt.plot(rho, es99_rho, color='blue', label='ES')
plt.plot(rho, var99_rho, color='red', label='VaR')
plt.xlabel("Rho")
plt.ylabel("VaR and ES")
plt.title("Heston Model. Correlation vs VaR99 and ES99")
plt.grid(True, alpha=0.2, color = "grey", ls='--', lw = 1,)
plt.legend()
plt.show()

# Kappa vs std and VaR/ES

kappa = [1.2, 1.5, 2.5, 3.5, 4.0]

pnl_kappa = [delta_hedging(model={**heston, "kappa" : k}) for k in kappa]
std_kappa = [np.std(pnl_k) for pnl_k in pnl_kappa]

plt.figure(figsize=(12,6))
plt.plot(kappa, std_kappa, color='green')
plt.xlabel("Kappa")
plt.ylabel("std(PnL)")
plt.title("Heston Model. Rate of reversion vs PnL std")
plt.grid(True, alpha=0.2, color = "grey", ls='--', lw = 1,)
plt.show()

var99_kappa = [np.percentile(pnl, 1) for pnl in pnl_kappa]
es99_kappa = [np.mean(pnl[pnl <= var]) for pnl, var in zip(pnl_kappa, var99_kappa)]

plt.figure(figsize=(12,6))
plt.plot(kappa, es99_kappa, color='blue', label='ES')
plt.plot(kappa, var99_kappa, color='red', label='VaR')
plt.xlabel("Kappa")
plt.ylabel("VaR and ES")
plt.title("Heston Model. Rate of reversion vs VaR99 and ES99")
plt.grid(True, alpha=0.2, color = "grey", ls='--', lw = 1,)
plt.legend()
plt.show()

# Merton. Parameter Sensitivity Tests

# Exp # jumps vs std and VaR/ES

lambda_jump = [0.5, 1, 1.5, 2.5, 4]

pnl_lambda = [delta_hedging(model={**merton, "lambda_jump" : l}) for l in lambda_jump]
std_lambda = [np.std(pnl_l) for pnl_l in pnl_lambda]

merton['lambda_jump'] = 1

plt.figure(figsize=(12,6))
plt.plot(lambda_jump, std_lambda, color='red')
plt.xlabel("Lambda")
plt.ylabel("std(PnL)")
plt.title("Merton Model. Jump rate vs PnL std")
plt.grid(True, alpha=0.2, color = "grey", ls='--', lw = 1,)
plt.show()

var99_lambda = [np.percentile(pnl, 1) for pnl in pnl_lambda]
es99_lambda = [np.mean(pnl[pnl <= var]) for pnl, var in zip(pnl_lambda, var99_lambda)]

plt.figure(figsize=(12,6))
plt.plot(lambda_jump, es99_lambda, color='blue', label='ES')
plt.plot(lambda_jump, var99_lambda, color='red', label='VaR')
plt.xlabel("Lambda")
plt.ylabel("VaR and ES")
plt.title("Merton Model. Jump rate vs VaR99 and ES99")
plt.grid(True, alpha=0.2, color = "grey", ls='--', lw = 1,)
plt.legend()
plt.show()

# Average jump size vs skewness

mu_jump = [-0.25, -0.1, -0.05, 0.05, 0.1, 0.25]

pnl_mu = [delta_hedging(model={**merton, "mu_jump" : mu})[:, -1] for mu in mu_jump]
k_mu = [stats.kurtosis(pnl_m) for pnl_m in pnl_mu]
sk_mu = [stats.skew(pnl_m) for pnl_m in pnl_mu]

merton['mu_jump'] = -0.05

fig, ax = plt.subplots(2, 3, figsize=(15, 8))
fig.suptitle('Jump size/direction vs PnL distribution')
ax[0,0].hist(pnl_mu[0], bins=100, density=True); ax[0,0].set_title(f"mu {mu_jump[0]}: kurtosis {k_mu[0]:.2f}, skewness {sk_mu[0]:.2f}")
ax[0,1].hist(pnl_mu[1], bins=100, density=True); ax[0,1].set_title(f"mu {mu_jump[1]}: kurtosis {k_mu[1]:.2f}, skewness {sk_mu[1]:.2f}")
ax[0,2].hist(pnl_mu[2], bins=100, density=True); ax[0,2].set_title(f"mu {mu_jump[2]}: kurtosis {k_mu[2]:.2f}, skewness {sk_mu[2]:.2f}")
ax[1,0].hist(pnl_mu[3], bins=100, density=True); ax[1,0].set_title(f"mu {mu_jump[3]}: kurtosis {k_mu[3]:.2f}, skewness {sk_mu[3]:.2f}")
ax[1,1].hist(pnl_mu[4], bins=100, density=True); ax[1,1].set_title(f"mu {mu_jump[4]}: kurtosis {k_mu[4]:.2f}, skewness {sk_mu[4]:.2f}")
ax[1,2].hist(pnl_mu[5], bins=100, density=True); ax[1,2].set_title(f"mu {mu_jump[5]}: kurtosis {k_mu[5]:.2f}, skewness {sk_mu[5]:.2f}")
plt.show()

var99_mu = [np.percentile(pnl, 1) for pnl in pnl_mu]
es99_mu = [np.mean(pnl[pnl <= var]) for pnl, var in zip(pnl_mu, var99_mu)]

plt.figure(figsize=(12,6))
plt.plot(mu_jump, es99_mu, color='blue', label='ES')
plt.plot(mu_jump, var99_mu, color='red', label='VaR')
plt.xlabel("Mu")
plt.ylabel("VaR and ES")
plt.title("Merton Model. Jump size/direction vs VaR99 and ES99")
plt.grid(True, alpha=0.2, color = "grey", ls='--', lw = 1,)
plt.legend()
plt.show()

# Jump volatility/uncertainty vs kurtosis/ES99

sigma_jump = [0.01, 0.05, 0.1, 0.15, 0.25, 0.4]

pnl_sigma = [delta_hedging(model={**merton, "sigma_jump" : sigma})[:, -1] for sigma in sigma_jump]
k_sigma = [stats.kurtosis(pnl_s) for pnl_s in pnl_sigma]
sk_sigma = [stats.skew(pnl_s) for pnl_s in pnl_sigma]

merton['sigma_jump'] = 0.1

fig, ax = plt.subplots(2, 3, figsize=(15, 8))
fig.suptitle('Jump volatility/uncertainty vs PnL distribution')
ax[0,0].hist(pnl_sigma[0], bins=100, density=True); ax[0,0].set_title(f"sigma {sigma_jump[0]}: kurtosis {k_sigma[0]:.2f}, skewness {sk_sigma[0]:.2f}")
ax[0,1].hist(pnl_sigma[1], bins=100, density=True); ax[0,1].set_title(f"sigma {sigma_jump[1]}: kurtosis {k_sigma[1]:.2f}, skewness {sk_sigma[1]:.2f}")
ax[0,2].hist(pnl_sigma[2], bins=100, density=True); ax[0,2].set_title(f"sigma {sigma_jump[2]}: kurtosis {k_sigma[2]:.2f}, skewness {sk_sigma[2]:.2f}")
ax[1,0].hist(pnl_sigma[3], bins=100, density=True); ax[1,0].set_title(f"sigma {sigma_jump[3]}: kurtosis {k_sigma[3]:.2f}, skewness {sk_sigma[3]:.2f}")
ax[1,1].hist(pnl_sigma[4], bins=100, density=True); ax[1,1].set_title(f"sigma {sigma_jump[4]}: kurtosis {k_sigma[4]:.2f}, skewness {sk_sigma[4]:.2f}")
ax[1,2].hist(pnl_sigma[5], bins=100, density=True); ax[1,2].set_title(f"sigma {sigma_jump[5]}: kurtosis {k_sigma[5]:.2f}, skewness {sk_sigma[5]:.2f}")
plt.show()

var99_sigma = [np.percentile(pnl, 1) for pnl in pnl_sigma]
es99_sigma = [np.mean(pnl[pnl <= var]) for pnl, var in zip(pnl_sigma, var99_sigma)]

plt.figure(figsize=(12,6))
plt.plot(sigma_jump, es99_sigma, color='blue', label='ES')
plt.plot(sigma_jump, var99_sigma, color='red', label='VaR')
plt.xlabel("Sigma")
plt.ylabel("VaR and ES")
plt.title("Merton Model. Jump volatility/uncertainty vs VaR99 and ES99")
plt.grid(True, alpha=0.2, color = "grey", ls='--', lw = 1,)
plt.legend()
plt.show()