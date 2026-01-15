

# Which Breaks First: Mean, Variance, or Distribution (NSE vs BSE)

## Overview

This repository contains the code and outputs for a statistical research analysis that investigates the hierarchy of breakdown in financial markets during crises. The research focuses on the question:

**Which statistical property of market returns breaks first during a crisis — the mean, the variance, or the distribution?**

Using daily log returns of the NIFTY 50 (NSE) and SENSEX (BSE) indices from 2018 to mid-2020, with emphasis on the COVID-19 crash period, this project shows that variance destabilises first, followed by distributional breakdown, while mean returns remain statistically stable.

The methodology and outputs are designed for transparency, reproducibility, and academic use.

---

## Research Question

Which statistical property of market returns deteriorates first during a financial crisis?

* Mean
* Variance
* Distribution

The analysis compares the NIFTY 50 and SENSEX to see whether these dynamics differ across two major Indian stock market indices.

---

## Data Source and Description

Daily adjusted closing prices of the NIFTY 50 and SENSEX indices are used for the period between January 2018 and June 2020. The data were obtained using the `yfinance` Python library, which provides access to publicly available historical financial data through Yahoo Finance.

Adjusted closing prices were converted into daily log returns to ensure stability with respect to price levels and to mitigate the effects of non-stationarity.

The year 2019 was treated as a baseline representing normal market conditions, against which crisis-period deviation was compared.

---

## Variables and Transformations

* **Daily log returns** are the primary variables of interest.
* Rolling transformations were applied using a 21-day window to capture time-varying statistical behavior while preserving short-term dynamics.
* Z-score normalisation was used to compare metrics uniformly over time.
* Diagnostic tests such as the Augmented Dickey–Fuller test and the Shapiro–Wilk test were used for stationarity and normality checks.

---

## Python Workflow and Architecture

1. **Data Acquisition**
   Historical price data is downloaded using the `yfinance` library for NSE and BSE.

2. **Preprocessing**
   Adjusted closing prices are converted into daily logarithmic returns.

3. **Baseline Definition**
   Returns from 2019 are stored as the reference distribution representing normal conditions.

4. **Rolling Computation**
   Rolling statistics — mean, variance, volatility, and distributional deviation — are calculated using a 21-day window.

5. **Z-Score Transformation**
   Rolling statistics are converted into Z-scores to identify significant structural changes.

6. **Crisis Extraction**
   A focused window from February to April 2020 is used to isolate crisis dynamics.

7. **Output Generation**
   Results are saved to CSV tables and figures are saved as PNG images in the output directory.

---

## Outputs

### Tables (CSV)

* **nifty_full_metrics.csv** — Full rolling metrics for NIFTY
* **sensex_full_metrics.csv** — Full rolling metrics for SENSEX
* **nifty_summary.csv** — Summary statistics for NIFTY
* **sensex_summary.csv** — Summary statistics for SENSEX
* **nifty_crash_metrics.csv** — Crash period Z-score statistics for NIFTY
* **sensex_crash_metrics.csv** — Crash period Z-score statistics for SENSEX
* **nse_bse_summary_comparison.csv** — Side-by-side summary of NIFTY and SENSEX

### Figures (PNG)

* **nifty_dashboard.png** — NIFTY variance vs distribution breakdown and return distribution plots
* **sensex_dashboard.png** — SENSEX variance vs distribution breakdown and return distribution plots
* **nse_bse_volatility_comparison.png** — Volatility comparison for NSE vs BSE

All outputs are referenced in the research article and saved in a publication-ready format.

---

## How to Run

1. **Clone the Repository**

   ```
   git clone https://github.com/DebugDatta/Which-Breaks-First-Mean-Variance-or-Distribution-NSE-vs-BSE
   ```

2. **Move into the Directory**

   ```
   cd Which-Breaks-First-Mean-Variance-or-Distribution-NSE-vs-BSE
   ```

3. **Install Dependencies**

   ```
   pip install -r requirements.txt
   ```

4. **Run the Analysis**

   ```
   python main.py
   ```

5. **View the Outputs**

   * Generated CSV tables and PNG figures will be saved in the output directory after the script runs.

---

## Reproducibility

* All data processing and analysis steps are fully reproducible.
* The code uses only publicly available data.
* No proprietary software or paid services are required.

---

