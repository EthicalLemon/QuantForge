# QuantForge

A reproducible quantitative-finance research toolkit built in public, one tested feature at a time.

QuantForge is designed to become a compact but credible portfolio project: not a collection of copied notebooks, and not a trading-profit promise. It focuses on transparent calculations, deterministic experiments, automated tests and documented assumptions.

## Current capabilities - v0.1.0

- Validated price and return series containers
- CSV price-series loader with explicit missing-value policies
- Compounded annualized return and volatility
- Covariance, correlation, and pairwise dependency diagnostics
- Sharpe and Sortino ratios
- Maximum drawdown
- Historical Value at Risk and Conditional Value at Risk
- Seeded geometric Brownian motion simulations
- Automated unit tests and CI

## Quick start

```bash
cd projects/quantforge
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -e ".[dev]"
pytest
python examples/quickstart.py
```

```python
from quantforge import correlation_diagnostics, load_price_series_csv

prices = load_price_series_csv("data/spy.csv", missing="ffill", name="SPY")
returns = prices.simple_returns()

diagnostics = correlation_diagnostics(
    {
        "SPY": [0.01, 0.02, -0.01, 0.015],
        "TLT": [0.004, -0.002, 0.003, 0.001],
    }
)
```

## Design principles

1. **Reproducible:** stochastic research uses explicit random seeds.
2. **Tested:** formulas and edge cases have automated tests.
3. **Explainable:** results expose assumptions rather than hiding them behind a UI.
4. **Modular:** analytics, simulation, data, optimization and backtesting remain separate.
5. **Honest:** this is educational research software, not investment advice.

## Planned system

```text
market data -> validation -> returns -> risk engine
                            -> strategy -> backtest
                            -> optimizer -> portfolio report
                                         -> dashboard
```

See [`ROADMAP.md`](ROADMAP.md) for the staged build plan and [`METHODOLOGY.md`](METHODOLOGY.md) for metric definitions.

## Disclaimer

QuantForge is for software engineering and quantitative-finance education. It does not provide financial advice, execution services or guarantees of investment performance.
