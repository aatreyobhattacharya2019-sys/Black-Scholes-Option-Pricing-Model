"""
Visualize how the Black-Scholes option price and Greeks change as the
underlying stock price moves. Produces a chart with two panels:
  1. Call & Put price vs. Stock Price
  2. Delta vs. Stock Price (for both call and put)

Saves the chart as 'option_sensitivity.png' in the current folder,
and displays it on screen if run locally.
"""

import numpy as np
import matplotlib.pyplot as plt

from black_scholes import bs_price, greeks

# ---- Fixed option parameters ----
K = 100        # Strike price
T = 0.5        # Time to expiry (years)
r = 0.05       # Risk-free rate
sigma = 0.25   # Volatility

# ---- Range of stock prices to evaluate ----
stock_prices = np.linspace(50, 150, 200)

call_prices = [bs_price(S, K, T, r, sigma, "call") for S in stock_prices]
put_prices = [bs_price(S, K, T, r, sigma, "put") for S in stock_prices]

call_deltas = [greeks(S, K, T, r, sigma, "call")["delta"] for S in stock_prices]
put_deltas = [greeks(S, K, T, r, sigma, "put")["delta"] for S in stock_prices]

# ---- Plot ----
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].plot(stock_prices, call_prices, label="Call Price", color="#2563eb")
axes[0].plot(stock_prices, put_prices, label="Put Price", color="#dc2626")
axes[0].axvline(K, color="gray", linestyle="--", linewidth=1, label="Strike (K)")
axes[0].set_title("Option Price vs. Stock Price")
axes[0].set_xlabel("Stock Price (S)")
axes[0].set_ylabel("Option Price")
axes[0].legend()
axes[0].grid(alpha=0.3)

axes[1].plot(stock_prices, call_deltas, label="Call Delta", color="#2563eb")
axes[1].plot(stock_prices, put_deltas, label="Put Delta", color="#dc2626")
axes[1].axvline(K, color="gray", linestyle="--", linewidth=1, label="Strike (K)")
axes[1].set_title("Delta vs. Stock Price")
axes[1].set_xlabel("Stock Price (S)")
axes[1].set_ylabel("Delta")
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig("option_sensitivity.png", dpi=150)
print("Chart saved as option_sensitivity.png")
