"""Small reproducible QuantForge example."""

from quantforge import (
    geometric_brownian_motion,
    historical_cvar,
    historical_var,
    max_drawdown,
    sharpe_ratio,
)

returns = [0.012, -0.006, 0.004, 0.009, -0.014, 0.007, 0.003]

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
