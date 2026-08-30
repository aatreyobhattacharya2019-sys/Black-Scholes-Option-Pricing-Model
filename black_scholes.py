"""
Black-Scholes Option Pricing Model
-----------------------------------
This module implements the Black-Scholes-Merton model for pricing
European call and put options, along with the option "Greeks"
(Delta, Gamma, Vega, Theta, Rho) which measure the option's
sensitivity to various market parameters.

Author: Aatreyo Bhattacharya
"""

import numpy as np
from scipy.stats import norm


def d1_d2(S, K, T, r, sigma):
    """
    Calculate the d1 and d2 terms used throughout the Black-Scholes formulas.

    Parameters
    ----------
    S : float -> Current stock price
    K : float -> Option strike price
    T : float -> Time to expiration, in years
    r : float -> Risk-free interest rate (annualized, as a decimal e.g. 0.05 = 5%)
    sigma : float -> Volatility of the underlying stock (annualized, as a decimal)

    Returns
    -------
    (d1, d2) : tuple of floats
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return d1, d2


def bs_price(S, K, T, r, sigma, option_type="call"):
    """
    Calculate the Black-Scholes price of a European call or put option.

    Parameters
    ----------
    S : float -> Current stock price
    K : float -> Strike price
    T : float -> Time to expiration in years
    r : float -> Risk-free rate (decimal)
    sigma : float -> Volatility (decimal)
    option_type : str -> "call" or "put"

    Returns
    -------
    price : float
    """
    if T <= 0 or sigma <= 0:
        # At/after expiry, or zero volatility -> payoff is intrinsic value
        if option_type == "call":
            return max(0.0, S - K)
        elif option_type == "put":
            return max(0.0, K - S)
        else:
            raise ValueError("option_type must be 'call' or 'put'")

    d1, d2 = d1_d2(S, K, T, r, sigma)

    if option_type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    return price


def greeks(S, K, T, r, sigma, option_type="call"):
    """
    Calculate the option Greeks: Delta, Gamma, Vega, Theta, Rho.

    Note: Theta is returned as the change in price per calendar day
    (annual theta / 365) since that's the most commonly quoted convention.
    Vega and Rho are returned per 1% change (i.e. already divided by 100).

    Returns
    -------
    dict with keys: delta, gamma, vega, theta, rho
    """
    d1, d2 = d1_d2(S, K, T, r, sigma)
    pdf_d1 = norm.pdf(d1)

    gamma = pdf_d1 / (S * sigma * np.sqrt(T))
    vega = S * pdf_d1 * np.sqrt(T) / 100  # per 1% change in vol

    if option_type == "call":
        delta = norm.cdf(d1)
        theta = (
            -(S * pdf_d1 * sigma) / (2 * np.sqrt(T))
            - r * K * np.exp(-r * T) * norm.cdf(d2)
        ) / 365
        rho = (K * T * np.exp(-r * T) * norm.cdf(d2)) / 100
    elif option_type == "put":
        delta = norm.cdf(d1) - 1
        theta = (
            -(S * pdf_d1 * sigma) / (2 * np.sqrt(T))
            + r * K * np.exp(-r * T) * norm.cdf(-d2)
        ) / 365
        rho = (-K * T * np.exp(-r * T) * norm.cdf(-d2)) / 100
    else:
        raise ValueError("option_type must be 'call' or 'put'")

    return {
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "rho": rho,
    }


if __name__ == "__main__":
   
    S = 100      # Current stock price
    K = 105      # Strike price
    T = 0.5      # 6 months to expiration
    r = 0.05     # 5% risk-free rate
    sigma = 0.20 # 20% annualized volatility

    call_price = bs_price(S, K, T, r, sigma, "call")
    put_price = bs_price(S, K, T, r, sigma, "put")

    call_greeks = greeks(S, K, T, r, sigma, "call")
    put_greeks = greeks(S, K, T, r, sigma, "put")

    print("=" * 50)
    print("Black-Scholes Option Pricing")
    print("=" * 50)
    print(f"Stock Price (S):      {S}")
    print(f"Strike Price (K):     {K}")
    print(f"Time to Expiry (T):   {T} years")
    print(f"Risk-Free Rate (r):   {r * 100:.2f}%")
    print(f"Volatility (sigma):   {sigma * 100:.2f}%")
    print("-" * 50)
    print(f"Call Option Price:    {call_price:.4f}")
    print(f"Put Option Price:     {put_price:.4f}")
    print("-" * 50)
    print("Call Greeks:")
    for k, v in call_greeks.items():
        print(f"  {k.capitalize():8s}: {v:.6f}")
    print("Put Greeks:")
    for k, v in put_greeks.items():
        print(f"  {k.capitalize():8s}: {v:.6f}")
    print("=" * 50)
