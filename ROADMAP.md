# QuantForge roadmap

Development is split into small, reviewable daily increments. Every feature should include tests and documentation.

## Phase 1 - Research foundation

- [x] Core risk and performance metrics
- [x] Reproducible geometric Brownian motion simulator
- [x] Unit-test baseline
- [x] Validated price/return data model
- [ ] CSV market-data loader with missing-value policy
- [ ] Optional live-data adapter with local caching

## Phase 2 - Portfolio analytics

- [ ] Covariance and correlation diagnostics
- [ ] Portfolio return, volatility and marginal risk contribution
- [ ] Long-only minimum-variance optimizer
- [ ] Maximum-Sharpe optimizer with explicit constraints
- [ ] Efficient-frontier generation and visualization

## Phase 3 - Backtesting engine

- [ ] Strategy interface and signal validation
- [ ] Buy-and-hold and moving-average baselines
- [ ] Transaction costs and slippage
- [ ] Walk-forward evaluation
- [ ] Benchmark comparison and tear sheet

## Phase 4 - Advanced research

- [ ] CAPM beta and alpha estimation
- [ ] Multi-factor regression
- [ ] Bootstrap confidence intervals
- [ ] Stress scenarios and Monte Carlo portfolio loss
- [ ] Parameter-sensitivity analysis

## Phase 5 - Presentation and release

- [ ] Interactive dashboard
- [ ] Example research notebook
- [ ] Generated sample report
- [ ] API documentation
- [ ] Packaging, coverage and security checks
- [ ] v1.0 release notes
