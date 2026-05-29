# Delta hedging with GBM, Heston and Merton

Project by Alexsey Chernichenko. May 2026.

# Project Goal 

# Background

## Delta Hedging

## Geometric Brownian Motion

$$ dS_t = mu S_t dt + \sigma S_t dW_t $$

$$ S_t = S_0 \exp \bigg( (\mu - 0.5 \sigma^2) t + \sigma W_t \bigg) $$

$$ S_t = S_0 \exp \bigg( (r - 0.5 \sigma^2) t + \sigma W_t \bigg) $$

## Merton Model

$$ dS_t = (r - \lambda k) S_t dt + \sigma S_t dW_t + S_t (J - 1) dN_t $$

$$ S_t = S_0 \exp \bigg( (r - \lambda k - 0.5 \sigma^2) t + \sigma W_t \bigg) \prod_{i=1}^N J_i $$

## Heston Model

$$ dS_t = \mu S_{t} dt + \sqrt{\nu_t} S_t dW_t^S $$

$$ d\nu_t = \kappa (\theta - \nu_t) dt + \xi \sqrt{\nu_t} dW_t^\nu $$

$$ W_t^S W_t^\nu = \rho dt $$

$$ 2\kappa \theta > \xi^2 $$

$$ S_{t + dt} = S_t * \exp \bigg( (r - 0.5 \nu_t) dt + \sqrt(v_t dt) Z_S) $$

$$ \nu_{t + dt} = v_t + \kappa * (theta - \nu_t) * dt + \xi * \sqrt(\nu_t dt) * Z_\nu $$

$$ Z_S = Z_1 $$

$$ Z_\nu = \rho Z_1 + \sqrt{1 - \rho^2} Z_2 $$

# Methodolgy 

# Structure

# Results

## Rolling Mean

## VaR, ES, skewness and kurtosis

## Hedging Frequency 

## Parameter Sensitivity of the Heston Model

### Vol-of-vol ($ \xi $)

### Correlaton 

### Rate of Reversion 

## Parameter Sensitivity of the Merton Model

# Discussion
