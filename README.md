# Black-Scholes Option Pricing Model

A Python implementation of the **Black-Scholes-Merton model** for pricing European call and put options, including the calculation of the option **Greeks** (Delta, Gamma, Vega, Theta, Rho).

This project was built to demonstrate practical application of quantitative finance concepts using Python.


The Black-Scholes model is one of the most widely used methods for pricing European-style options. It estimates the theoretical price of an option based on five inputs:

- **S** — Current price of the underlying stock
- **K** — Strike price of the option
- **T** — Time to expiration (in years)
- **r** — Risk-free interest rate
- **σ (sigma)** — Volatility of the underlying stock

The model assumes the stock price follows a lognormal distribution and that markets are frictionless (no transaction costs, continuous trading, constant volatility, and a constant risk-free rate).

**Call option formula:**

```
C = S·N(d1) − K·e^(−rT)·N(d2)
```

**Put option formula:**

```
P = K·e^(−rT)·N(−d2) − S·N(−d1)
```

where `N(x)` is the cumulative distribution function of the standard normal distribution, and:

```
d1 = [ln(S/K) + (r + σ²/2)·T] / (σ·√T)
d2 = d1 − σ·√T
```

## Features

- Calculate European call and put option prices
- Calculate all major Greeks: **Delta, Gamma, Vega, Theta, Rho**
- Visualize how option price and Delta change as the stock price moves


## Possible Extensions

- Implied volatility solver (reverse-engineer sigma from market price)
- American option pricing via binomial tree
- Monte Carlo simulation for option pricing
- Simple web interface (e.g. Streamlit) for interactive pricing

## License

This project is open source and available under the [MIT License](LICENSE).
