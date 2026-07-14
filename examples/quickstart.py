"""Small reproducible QuantForge example."""

from quantforge import (
    PriceSeries,
    geometric_brownian_motion,
    historical_cvar,
    historical_var,
    max_drawdown,
    sharpe_ratio,
)

prices = PriceSeries.from_prices([100, 101.2, 100.6, 101.0, 101.9, 100.5, 101.2, 101.5])
returns = prices.simple_returns().values

print(f"Sharpe ratio: {sharpe_ratio(returns):.3f}")
print(f"Maximum drawdown: {max_drawdown(returns):.2%}")
print(f"95% historical VaR: {historical_var(returns):.2%}")
print(f"95% historical CVaR: {historical_cvar(returns):.2%}")

paths = geometric_brownian_motion(
    initial_price=100,
    annual_drift=0.08,
    annual_volatility=0.20,
    paths=10_000,
    seed=42,
)
print(f"Median simulated terminal price: {float(paths[-1].mean()):.2f}")
