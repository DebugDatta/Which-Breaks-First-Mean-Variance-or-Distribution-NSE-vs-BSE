import yfinance as yf
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from statsmodels.tsa.stattools import adfuller
import os

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
        self.summary = None

    def fetch(self):
        self.df = yf.download(
            self.ticker,
            start=START_DATE,
            end=END_DATE,
            auto_adjust=True,
            progress=False
        )
        if isinstance(self.df.columns, pd.MultiIndex):
            self.df.columns = self.df.columns.get_level_values(0)

        self.df['Log_Return'] = np.log(self.df['Close'] / self.df['Close'].shift(1))
        self.df.dropna(inplace=True)

        self.baseline = self.df.loc[self.df.index.year == BASELINE_PERIOD, 'Log_Return'].values

    def compute(self):
        r = self.df['Log_Return']

        adf = adfuller(r)
        shapiro_p = stats.shapiro(r)[1]

        self.summary = pd.DataFrame({
            "Market": self.name,
            "Metric": ["ADF Statistic", "ADF P-Value", "Shapiro P-Value", "Skewness", "Kurtosis"],
            "Value": [adf[0], adf[1], shapiro_p, r.skew(), r.kurt()]
        })

        self.df['Roll_Mean'] = r.rolling(ROLLING_WINDOW).mean()
        self.df['Roll_Vol'] = r.rolling(ROLLING_WINDOW).std()

        def ks_roll(x):
            if len(x) < 10 or len(self.baseline) < 10:
                return np.nan
            return stats.ks_2samp(x, self.baseline)[0]

        self.df['Roll_KS'] = r.rolling(ROLLING_WINDOW).apply(ks_roll, raw=True)
        self.df.dropna(inplace=True)

    def save_outputs(self):
        self.df.to_csv(f"{OUTPUT_DIR}/{self.name.lower()}_full_metrics.csv")
        self.summary.to_csv(f"{OUTPUT_DIR}/{self.name.lower()}_summary.csv", index=False)

        crash = self.df.loc["2020-02-15":"2020-04-01"].copy()
        crash['Z_Vol'] = stats.zscore(crash['Roll_Vol'])
        crash['Z_KS'] = stats.zscore(crash['Roll_KS'])
        crash.to_csv(f"{OUTPUT_DIR}/{self.name.lower()}_crash_metrics.csv")

    def plot(self):
        fig = plt.figure(figsize=(18, 10))
        gs = gridspec.GridSpec(2, 2)

        ax1 = plt.subplot(gs[0, :])
        ax1.plot(self.df.index, stats.zscore(self.df['Roll_Vol']), label="Rolling Volatility (Z)", linewidth=1)
        ax1.plot(self.df.index, stats.zscore(self.df['Roll_KS']), label="Distributional Break (KS Z)", linewidth=1)
        ax1.axhline(3, linestyle="--", linewidth=0.8)
        ax1.set_title(f"{self.name}: Variance vs Distribution Breakdown")
        ax1.set_ylabel("Z-Score")
        ax1.legend()

        ax2 = plt.subplot(gs[1, 0])
        sns.histplot(self.df['Log_Return'], kde=True, ax=ax2)
        ax2.set_title(f"{self.name}: Log Return Distribution")
        ax2.set_xlabel("Log Return")

        ax3 = plt.subplot(gs[1, 1])
        stats.probplot(self.df['Log_Return'], dist="norm", plot=ax3)
        ax3.set_title(f"{self.name}: Q-Q Plot")

        plt.tight_layout()
        plt.savefig(f"{OUTPUT_DIR}/{self.name.lower()}_dashboard.png", dpi=300)
        plt.close()

engines = []

for name, ticker in TICKERS.items():
    e = StructuralBreakEngine(name, ticker)
    e.fetch()
    e.compute()
    e.save_outputs()
    e.plot()
    engines.append(e)

comparison = pd.concat([e.summary for e in engines])
comparison.to_csv(f"{OUTPUT_DIR}/nse_bse_summary_comparison.csv", index=False)

plt.figure(figsize=(14, 6))
for e in engines:
    plt.plot(
        e.df.index,
        stats.zscore(e.df['Roll_Vol']),
        label=f"{e.name} Volatility",
        linewidth=1
    )

plt.axhline(3, linestyle="--", linewidth=0.8)
plt.title("NSE vs BSE: Volatility Breakdown Comparison")
plt.ylabel("Z-Score")
plt.legend()
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/nse_bse_volatility_comparison.png", dpi=300)
plt.close()
