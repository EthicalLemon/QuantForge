name: Daily QuantForge Health Check

on:
  schedule:
    - cron: "30 13 * * *" # 7:00 PM Asia/Kolkata
  workflow_dispatch:

permissions:
  contents: write

jobs:
  health-check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: python -m pip install --upgrade pip
      - run: python -m pip install -e ".[dev]"
      - name: Validate project
        run: |
          ruff check .
          pytest
      - name: Record transparent daily health result
        run: |
          {
            echo "# Daily health check"
            echo
            echo "- Date (UTC): $(date -u +'%Y-%m-%d')"
            echo "- Validation: passed"
            echo "- Python: $(python --version)"
            echo "- Purpose: automated CI health record"
          } > reports/daily-health.md
      - name: Commit health record
        run: |
          git config user.name "EthicalLemon"
          git config user.email "lemuelplayzer1510@gmail.com"
          git add reports/daily-health.md
          if git diff --cached --quiet; then
            exit 0
          fi
          git commit -m "chore: daily QuantForge health check"
          git push
