import yfinance as yf
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import os

# --- Configuration ---
TICKERS = {
    "NIFTY": "^NSEI",
    "SENSEX": "^BSESN"
}

START_DATE = "2018-01-01"
END_DATE = "2020-06-30"
ROLLING_WINDOW = 21
BASELINE_PERIOD = 2019
OUTPUT_DIR = "outputs_nse_bse"

os.makedirs(OUTPUT_DIR, exist_ok=True)

class StructuralBreakEngine:
    def __init__(self, name, ticker):
        self.name = name
        self.ticker = ticker
        self.df = None
        self.baseline = None

    def fetch(self):
        # Added repair=True for better yfinance data integrity
        self.df = yf.download(
            self.ticker,
            start=START_DATE,
            end=END_DATE,
            auto_adjust=True,
            progress=False
        )

        # FIXED: Robust handling for yfinance MultiIndex columns
        if isinstance(self.df.columns, pd.MultiIndex):
            try:
                # Try to extract the specific ticker level (Standard yfinance v0.2+)
                self.df = self.df.xs(self.ticker, axis=1, level=1)
            except KeyError:
                # Fallback: flatten the top level if 'xs' fails
                self.df.columns = self.df.columns.get_level_values(0)

        # Safety check if column exists
        if "Close" not in self.df.columns:
            # Sometimes auto_adjust=True returns only 'Close' without caps or just 'Price'
            # We assume the first column is the closing price if 'Close' is missing
            self.df.rename(columns={self.df.columns[0]: "Close"}, inplace=True)

        self.df["Log_Return"] = np.log(self.df["Close"] / self.df["Close"].shift(1))
        self.df.dropna(inplace=True)

        # Extract Baseline
        self.baseline = self.df.loc[self.df.index.year == BASELINE_PERIOD, "Log_Return"].values
        
        # Error Check: Ensure baseline has data
        if len(self.baseline) < 10:
            print(f"WARNING: Insufficient baseline data for {self.name} in year {BASELINE_PERIOD}")

    def compute(self):
        r = self.df["Log_Return"]

        self.df["Roll_Mean"] = r.rolling(ROLLING_WINDOW).mean()
        self.df["Roll_Vol"] = r.rolling(ROLLING_WINDOW).std()

        def ks_roll(x):
            # Check for NaN or insufficient data in window
            if len(x) < 10 or len(self.baseline) < 10 or np.isnan(x).any():
                return np.nan
            return stats.ks_2samp(x, self.baseline)[0]

        self.df["Roll_KS"] = r.rolling(ROLLING_WINDOW).apply(ks_roll, raw=True)
        self.df.dropna(inplace=True)

        # Calculate Z-Scores
        # ddof=1 for sample standard deviation
        self.df["Z_Mean"] = stats.zscore(self.df["Roll_Mean"], nan_policy='omit')
        self.df["Z_Vol"] = stats.zscore(self.df["Roll_Vol"], nan_policy='omit')
        self.df["Z_KS"] = stats.zscore(self.df["Roll_KS"], nan_policy='omit')

    def plot_dashboard(self):
        fig = plt.figure(figsize=(18, 10))
        gs = gridspec.GridSpec(2, 2)

        ax1 = plt.subplot(gs[0, :])
        ax1.plot(self.df.index, self.df["Z_Vol"], label="Volatility Z", linewidth=1, color='red')
        ax1.plot(self.df.index, self.df["Z_KS"], label="KS Z (Dist Break)", linewidth=1, color='blue')
        ax1.axhline(3, linestyle="--", linewidth=0.8, color='black')
        ax1.set_title(f"{self.name}: Variance vs Distribution Breakdown")
        ax1.set_ylabel("Z Score")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        ax2 = plt.subplot(gs[1, 0])
        sns.histplot(self.df["Log_Return"], kde=True, ax=ax2, color='purple')
        ax2.set_title(f"{self.name}: Log Return Distribution")

        ax3 = plt.subplot(gs[1, 1])
        stats.probplot(self.df["Log_Return"], dist="norm", plot=ax3)
        ax3.set_title(f"{self.name}: Q-Q Plot")

        plt.tight_layout()
        plt.savefig(f"{OUTPUT_DIR}/{self.name.lower()}_dashboard.png", dpi=300)
        plt.close()

    def plot_mean_stability(self):
        plt.figure(figsize=(14, 5))
        plt.plot(self.df.index, self.df["Z_Mean"], linewidth=1, color='green')
        plt.axhline(3, linestyle="--", linewidth=0.8, color='black')
        plt.axhline(-3, linestyle="--", linewidth=0.8, color='black')
        plt.title(f"{self.name}: Rolling Mean Stability")
        plt.ylabel("Mean Z Score")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"{OUTPUT_DIR}/{self.name.lower()}_mean_stability.png", dpi=300)
        plt.close()

    def plot_ks_only(self):
        plt.figure(figsize=(14, 5))
        plt.plot(self.df.index, self.df["Z_KS"], linewidth=1, color='blue')
        plt.axhline(3, linestyle="--", linewidth=0.8, color='black')
        plt.title(f"{self.name}: Distributional Breakdown Only")
        plt.ylabel("KS Z Score")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(f"{OUTPUT_DIR}/{self.name.lower()}_ks_breakdown.png", dpi=300)
        plt.close()

# --- Execution ---
engines = []

for name, ticker in TICKERS.items():
    print(f"Processing {name} ({ticker})...")
    try:
        e = StructuralBreakEngine(name, ticker)
        e.fetch()
        e.compute()
        e.plot_dashboard()
        e.plot_mean_stability()
        e.plot_ks_only()
        engines.append(e)
    except Exception as err:
        print(f"Skipping {name} due to error: {err}")

# Comparison Plot
if engines:
    plt.figure(figsize=(14, 6))
    for e in engines:
        plt.plot(e.df.index, e.df["Z_Vol"], label=f"{e.name} Volatility", linewidth=1)

    plt.axhline(3, linestyle="--", linewidth=0.8, color='black')
    plt.title("NSE vs BSE: Volatility Breakdown Comparison")
    plt.ylabel("Z Score")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/nse_bse_volatility_comparison.png", dpi=300)
    plt.close()
    print("\nProcessing Complete. Check the 'outputs_nse_bse' folder.")
