# What Breaks First? A Statistical Analysis of Mean, Variance, and Distribution in NSE and BSE Markets

## Overview

This repository contains the code and outputs for a statistical research analysis that investigates the hierarchy of breakdown in Indian financial markets during the COVID-19 crisis. The research focuses on the question:

**Which statistical property of market returns breaks first during a crisis — the mean, the variance, or the distribution?**

Using daily log returns of the NIFTY 50 (NSE) and SENSEX (BSE) indices from 2018 to mid-2020, this project performs a "statistical autopsy" of the March 2020 crash. The results demonstrate that **Variance (Volatility)** is the leading indicator of a crash, followed by a **Distributional (Structural)** breakdown, while the **Mean (Trend)** acts as a lagging indicator.

The methodology is designed for transparency, utilizing non-parametric tests and rolling-window analysis to isolate market regimes.

---

## Research Question

Which statistical property of market returns deteriorates first during a financial crisis?

* **Mean:** The directional trend of the market.
* **Variance:** The volatility or "fear" in the market.
* **Distribution:** The fundamental probability shape (normality vs. fat tails) of returns.

The analysis compares the NIFTY 50 and SENSEX to determine if these dynamics are systemic across the Indian equity market.

---

## Data Source and Description

Daily adjusted closing prices of the **NIFTY 50** and **SENSEX** indices are used for the period between **January 2018 and June 2020**. The data were obtained using the `yfinance` Python library, which provides access to publicly available historical financial data through Yahoo Finance.

* **Preprocessing:** Adjusted closing prices were converted into **Daily Log Returns** () to ensure additivity and stationarity.
* **Baseline:** The year **2019** was established as the "Control Group" representing normal market conditions.

---

## Variables and Transformations

* **Daily Log Returns:** The primary variable of interest.
* **Rolling Statistics:** Calculated using a **21-day rolling window** (approx. 1 trading month).
* *Rolling Variance:* To track risk.
* *Rolling KS-Statistic:* A non-parametric Kolmogorov-Smirnov test comparing the current window's distribution against the 2019 baseline.


* **Z-Score Normalization:** All metrics were standardized () to allow for direct comparison between volatility (%), distributional distance (D-stat), and price trend.

---

## Python Workflow and Architecture

1. **Data Acquisition**
Historical price data is fetched via `yfinance` for ticker symbols `^NSEI` (Nifty) and `^BSESN` (Sensex).
2. **Preprocessing**
Conversion of raw prices to log returns and handling of missing data.
3. **Baseline Extraction**
Isolating the 2019 dataset to serve as the statistical reference point for the KS Test.
4. **Structural Break Engine**
A custom class calculates rolling Z-scores for Mean, Variance, and the KS Statistic simultaneously.
5. **Visualization**
Generation of comparative plots and dashboards to visually identify the "moment of break" for each metric.
6. **Output Generation**
High-resolution charts are saved to the `outputs_nse_bse` directory.

---

## Outputs

### Figures (PNG/JPG)

The analysis generates 7 key visualizations located in the `outputs_nse_bse` folder:

* **nse_bse_volatility_comparison.png** — The primary result showing Volatility Z-scores for NSE vs BSE.
* **nifty_dashboard.jpg** — Comprehensive 3-panel dashboard for NIFTY (Variance vs KS, Histogram, Q-Q Plot).
* **sensex_dashboard.jpg** — Comprehensive 3-panel dashboard for SENSEX.
* **nifty_ks_breakdown.png** — Isolated timeline of the NIFTY Distributional/Structural break.
* **sensex_ks_breakdown.png** — Isolated timeline of the SENSEX Distributional/Structural break.
* **nifty_mean_stability.png** — Timeline showing the lagging nature of the Mean trend.
* **sensex_mean_stability.png** — Timeline showing the lagging nature of the Mean trend.

---

## How to Run

1. **Clone the Repository**
```bash
git clone https://github.com/DebugDatta/Which-Breaks-First-Mean-Variance-or-Distribution-NSE-vs-BSE.git

```


2. **Move into the Directory**
```bash
cd Which-Breaks-First-Mean-Variance-or-Distribution-NSE-vs-BSE

```


3. **Install Dependencies**
```bash
pip install -r requirements.txt

```


4. **Run the Analysis**
```bash
python main.py

```


5. **View the Results**
* The script will print statistical summary tables to the terminal.
* All charts will be generated and saved in the `outputs_nse_bse` folder.



---

## Reproducibility

* **Open Source:** All code is open-source and available in this repository.
* **Data Integrity:** The analysis uses standard public data sources (`yfinance`), ensuring that any researcher can replicate the results without proprietary access.
* **Environment:** A `requirements.txt` file is provided to replicate the exact Python environment used for the study.
