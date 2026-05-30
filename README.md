# Delta hedging with GBM, Heston and Merton Models

Project by Alexsey Chernichenko. May 2026.

# Project Goal 

The goal of this project is to evaluate performance of delta hedging under different asset price dynamics. Using Monte Carlo simulation delta hedging strategy is implemented and compared for different models: the Geometric Brownian Motion (GBM), Heston stochastic volatility and Merton jump diffusion models. Hedging effectiveness is then assessed through the analysis of profit and loss (PnL), Value-at-Risk (VaR) and Expected Shortfall (ES). Additionally, parameter sensitivity analysis is performed for the Heston and Merton models. The project aims to quantify how stochastic volatility, jumps and hedging frequency distort hedging accuracy and residual risk.

# Background

## Delta Hedging

Delta hedging aims to eliminate sensitivity to small changes in the underlying price by constructing a locally risk-free portfolio. A delta-hedged portfolio is formed as:

$$ \Pi = V - \Delta S $$

Using Itô’s lemma, the stochastic term cancels and under continuous rebalancing the portfolio evolves deterministically:

$$ d \Pi = \bigg( \frac{\partial V}{\partial t} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2}\bigg) dt $$

In the Black–Scholes framework no-arbitrage implies:

$$ d \Pi = r \Pi dt $$

which leads to the Black–Scholes PDE. 

To put it simply, the idea is to offset the option’s exposure to the underlying by taking an opposite position in the stock. Since Delta measures how much the option price moves with the stock, holding $−Δ$ units of the underlying stock cancels the first-order price risk. As the stock price changes, Delta changes as well, so the hedge must be continuously rebalanced. In theory, continuous rebalancing removes all randomness from the portfolio, making it risk-free. In practice, rebalancing is discrete, which introduces hedging error that grows with volatility and lower rebalancing frequency.

In the Black–Scholes framework, the idea is extended since the stock position alone almost never has the same value as the option. However, an option can be replicated by a portfolio consisting of a position in the underlying asset and a risk-free cash account. The idea is reminiscent of the portfolio replication in the binomial model and this isn't a coincidence since the Black-Scholes is its continuous limit. So, at time $t_i$ the value of the replicating portfolio is:

$$ V_{t_i} = \Delta_{t_i} S_{t_i} + B_{t_i} $$

where $V_{t_i}$ is the option value, $S_{t_i}$ is the underlying asset price, $\Delta_{t_i}$ is the option delta and $B_{t_i}$ is the value of the cash account. Between rebalancing dates, the stock position remains unchanged while the cash account accumulates interest at the risk-free rate $r$.

$$ B_{t_{i+1}} = B_{t_i} e^{r (t_{i+1} - t_i)} $$

At the next rebalancing date $t_{i+1}$, the option delta is recalculated and the stock position is adjusted from $\Delta_{t_i}$ to $\Delta_{t_{i+1}}$. The cash account is updated according to

$$ B_{t_{i+1}} = B_{t_i} e^{r (t_{i+1} - t_i)} - (\Delta_{t_{i+1}} - \Delta_{t_i}) S_{i+1} $$

The portfolio value after rebalancing becomes

$$ V_{t_{i+1}} = \Delta_{t_{i+1}} S_{t_{i+1}} + B_{t_{i+1}} $$

Under continuous rebalancing, this replication strategy reproduces the Black–Scholes option value exactly. In practice however rebalancing is performed discretely which leads to replication errors.

## Geometric Brownian Motion

The Geometric Brownian Motion is a continuous-time stochastic process that assumes that asset prices evolve continuously with a constant drift and constant volatility. The corresponding stochastic differnetial equation (SDE) is

$$ dS_t = \mu S_t dt + \sigma S_t dW_t $$

Where $S_t$ is the asset price at time $t$, $\mu$ is the drift, $\sigma$ is the volatiltiy and $dW_t$ is the Wiener process/Brownian Motion. This SDE has the following analytic solution:

$$ S_t = S_0 \exp \bigg( (\mu - 0.5 \sigma^2) t + \sigma W_t \bigg) $$

The model is the foundation of the Black–Scholes framework. When the no-arbitrage principle is applied, the expected growth rate of any asset's price in a risk-neutral world must equal the risk-free rate $r$. Therefore, in the Black-Scholes world, the GBM has drift $\mu = r$.

$$ S_t = S_0 \exp \bigg( (r - 0.5 \sigma^2) t + \sigma W_t \bigg) $$

## Merton Model

The Merton jump-diffusion model enhances the GBM framework by incorporating sudden and discontinuous price movements through a Poisson jump process. Asset prices can experience random jumps of varying size and direction. This feature allows the model to capture extreme market events and fat-tailed return distributions that are not explained by the standard Black–Scholes assumptions. As a result, the model provides a more realistic description of tail risk and hedging performance during market shocks. The corresponing SDE has the follwoing form:

$$ dS_t = (\mu - \lambda k) S_t dt + \sigma S_t dW_t + S_t (J - 1) dN_t $$

Aside from the parameters that also appear in the GBM, the new parameters are $\lambda$ that is the expected number of jumps per year or simply jump rate, $J$ is the jump magnitude, which is typically assumed to be log-normally distributed and can be therefroe written as $e^{N \mu_J + \sqrt{N} \sigma_J Z}$, where $N$ is number of jumps, $\mu_J$ is the mean log-jump size (the directional tendency), $\sigma_J$ is the volatility/uncertainty of the log-jump size and $Z_i$ is a standard normal random variable. $dN_t$ is a Poisson process where $dN = 1$ if a jump occurs and $0$ otherwise. Finally, $k$ represents the expected percentage change in the asset price caused by a single jump and is $E\[ J - 1\]$. Given that, the analytical solution can be derived in a similar manner as for the GBM. 

$$ S_t = S_0 \exp \bigg( (\mu - \lambda k - 0.5 \sigma^2) t + \sigma W_t \bigg) \prod_{i=1}^N J_i $$

## Heston Model

The Heston model adds some complexity and extends the GBM framework by introducing stochastic volatility. Instead of assuming a constant volatility, the variance follows its own mean-reverting stochastic process. This allows the model to capture important market phenomena such as volatility clustering and the volatility smile observed in option markets. Overall, the model provides a more realistic reperesenation of market dynamics. 

The model is therefore fully described by two SDEs - one for the asset price $S_t$ and the other one for its $\nu_t$.

$$ dS_t = \mu S_{t} dt + \sqrt{\nu_t} S_t dW_t^S $$

$$ d\nu_t = \kappa (\theta - \nu_t) dt + \xi \sqrt{\nu_t} dW_t^\nu $$

Where $dW_t^S$ and $dW_t^\nu$ are the Wiener processes\Brownian Motions for the asset price $S_t$ and volatility $\nu_t$ respectively. $\kappa$ is the rate at which νt reverts to $\theta$, which in its turn is the long variance or long-run average variance of the price (as $t$ tends to infinity, the expected value of $\nu_t$ tends to $\theta$). Finally, $\rho$ is the correlation between $dW_t^S$ and $dW_t^\nu$, and $\xi$ is the volatility of the volatility (vol-of-vol). The existence of $\xi$ is of course explained by the fact that volatility itself becomes a stochastic process.

Besides the SDEs above, there are two important conditions:

$$ W_t^S W_t^\nu = \rho dt $$

which indicates that the two Wiener processes are correlated, and

$$ 2\kappa \theta > \xi^2 $$

which is called the Feller condition. This condition ensures that that the volatiltiy $\nu_t$ is strictly positive. 

Unfortunately, the SDEs has no analytical solution. Nevertheless, a discretized approximation can be derived:

$$ S_{t + \Delta t} = S_t \exp \bigg( (\mu - 0.5 \nu_t) \Delta t + \sqrt{v_t \Delta t} Z_S \bigg) $$

$$ \nu_{t + \Delta t} = v_t + \kappa (\theta - \nu_t) \Delta t + \xi \sqrt{\nu_t \Delta t} Z_\nu $$

Where $Z_S$ and $Z_\nu$ are two standard normal random variables, which are linked by the Cholesky decomposition.

$$ Z_S = Z_1 $$

$$ Z_\nu = \rho Z_1 + \sqrt{1 - \rho^2} Z_2 $$

Note: for direct comparison with GBM, it's assumed that both Merton and Heston models have drift $\mu$ = $r$. 

# Methodolgy 

Asset price paths were simulated using Monte Carlo methods under three different models: GBM, the Heston and the Merton models. For each model, a discrete-time delta hedging strategy was implemented using Black–Scholes deltas and rebalanced at predetermined intervals.

Hedging performance was evaluated by analyzing the resulting PnL distributions, including measures such as rolling mean PnL, standard deviation, VaR ES. The impact of hedging frequency on replication accuracy was investigated and parameter sensitivity analyses were performed to assess how key model parameters influence hedging risk and performance.

The standard values that were used for the GBM were $S$ = 100, $K$ = 100, $r$ = 0.035, $\sigma$ = 0.2, $T$ = 1, number of steps = 252 and number of simulations = 10000. For the Merton model: $\lambda$ = 1, $mu_J$ = - 0.05 and $\sigma_J$ = 0.1. Finally, for the Heston model: $\nu_0$ = 0.04, $\rho$ = -0.7, $xi$ = 0.3, $\theta$ = 0.04 and $\kappa$ = 1.5. 

# Structure

# Results

## Rolling Mean

<img width="1200" height="600" alt="Figure_1" src="https://github.com/user-attachments/assets/c4148df2-1bc8-4a8c-ba74-d4ce94e2b299" />

<img width="1200" height="600" alt="Figure_2" src="https://github.com/user-attachments/assets/3c3fd008-67b0-42e4-9d57-8d0b87f11d4a" />

## PnL mean, PnL std, skewness, kurtosis, VaR and ES

<img width="1200" height="600" alt="Figure_3" src="https://github.com/user-attachments/assets/ce501363-5d34-44c6-81a0-6ad966287a04" />

|          |   GBM   |   Merton   |   Heston   |
| -------- | ------- | ---------- | ---------- |
| PnL mean | 0.0015  |   -1.07    |   0.16     |
| PnL std  | 0.44    |    2.04    |   1.77     |
| Skewness | -0.15   |   -2.93    |   -0.69    |
| Kurtosis | 1.62    |   12.69    |    1.56    |
| VaR99    | -1.16   |   -9.38    |   -5.03    |
| ES99     | -1.47   |   -11.77   |   -6.25    |

## Hedging Frequency 

Number of steps used are 10, 25, 50, 100, 252 and 500.

<img width="1200" height="600" alt="Figure_4" src="https://github.com/user-attachments/assets/2e21664a-0e30-4a1f-bf46-dc7b6c6b42c6" />

## Parameter Sensitivity of the Merton Model

### Jump rate ($\lambda$)

Number of expected jumps per year used are 0.5, 1, 1.5, 2.5 and 4.

<img width="1200" height="600" alt="Figure_11" src="https://github.com/user-attachments/assets/6e037284-00c5-417d-b56b-dc1a5e593b1d" />

<img width="1200" height="600" alt="Figure_12" src="https://github.com/user-attachments/assets/f20e31c3-faed-465a-ab63-1ea46e2f5e9e" />

### Jump size/direction ($\mu_J$)

Jump sizes/directions used are -0.25, -0.1, -0.05, 0.05, 0.1 and 0.25

<img width="1440" height="800" alt="Figure_18" src="https://github.com/user-attachments/assets/fdce359a-df11-45c3-a60f-cb2f8846a5f6" />

<img width="1200" height="600" alt="Figure_14" src="https://github.com/user-attachments/assets/519b3e4a-563f-4841-a46a-bb05d150ac7e" />

### Jump volatiltiy/uncertainty ($\nu_J$)

Jump volatilities/uncertainties used are 0.01, 0.05, 0.1, 0.15, 0.25 and 0.4

<img width="1440" height="800" alt="Figure_19" src="https://github.com/user-attachments/assets/10232af5-5706-40df-acbb-680f871171c4" />

<img width="1200" height="600" alt="Figure_16" src="https://github.com/user-attachments/assets/7f21c5af-ed7c-466f-ac87-b373296f6e27" />

## Parameter Sensitivity of the Heston Model

### Vol-of-vol ($\xi$)

Vol-of-vol used are 0.1, 0.2, 0.3, 0.4 and 0.5.

<img width="1200" height="600" alt="Figure_5" src="https://github.com/user-attachments/assets/f54fa2f8-b9a3-4117-8479-36f0b317d170" />

<img width="1200" height="600" alt="Figure_6" src="https://github.com/user-attachments/assets/458af505-283e-44e4-9e7e-a16d0423f644" />

### Correlaton ($\rho$)

Correlations used are 0.5, 0.1, -0.4, -0.7, -0.9 and -0.99.

<img width="1440" height="800" alt="Figure_17" src="https://github.com/user-attachments/assets/ce84d0ba-fb56-44fd-9fc8-24cf68fbee95" />

<img width="1200" height="600" alt="Figure_8" src="https://github.com/user-attachments/assets/71047ed7-146a-4eee-b8bd-b9399fd6e6ae" />

### Rate of Reversion ($\kappa$)

Rates of reversion used are 1.2, 1.5, 2.5, 3.5 and 4.0.

<img width="1200" height="600" alt="Figure_9" src="https://github.com/user-attachments/assets/8107f20e-0b89-4024-8a0c-06cf7a3d0810" />

<img width="1200" height="600" alt="Figure_10" src="https://github.com/user-attachments/assets/b7eafcfe-bcd9-4533-877a-886b57800dbc" />

# Discussion
