# Methodology

## Data model

Price series require at least two positive finite observations. They can be
converted into simple decimal returns or continuously compounded log returns.
Return series reject values below -100% and can generate a compounded wealth
index for downstream analytics. CSV imports map a chosen price column into the
same validated model and make the missing-data policy explicit: reject missing
rows, drop them, or forward-fill from the last observed price.

## Return convention

Input series are decimal periodic returns, such as `0.01` for one percent. Annualized return is calculated geometrically from compounded wealth. Volatility uses sample standard deviation and square-root-of-time scaling.

## Cross-asset diagnostics

Covariance matrices use the sample estimator with `ddof=1` on aligned return
series. Correlation matrices normalize the same aligned observations, and the
pairwise diagnostics rank asset pairs by absolute correlation so concentration
and diversification relationships are visible before optimization work begins.

## Risk-adjusted performance

The Sharpe ratio uses annualized compounded return minus an annual risk-free rate, divided by annualized volatility. The Sortino ratio replaces total volatility with downside deviation relative to a target return.

## Drawdown

Maximum drawdown is the most negative peak-to-trough decline in the compounded wealth index. It is returned as a negative decimal.

## Tail risk

Historical Value at Risk is reported as a positive loss threshold. Conditional Value at Risk is the positive average loss at or beyond that threshold. Historical estimates are sample-dependent and should not be treated as stable forecasts.

## Simulation

The initial simulator follows geometric Brownian motion with constant drift and volatility. It is deliberately simple and serves as a baseline for later comparison with fat-tailed and regime-aware models.
