"""Summary numbers and plots."""
from pathlib import Path
 
import matplotlib.pyplot as plt
 
HOURS = 5 / 60
 
 
def summarise(result, battery):
    """Key numbers for a simulation result."""
    discharged = result["power_mw"].clip(lower=0).sum() * HOURS
    charged = -result["power_mw"].clip(upper=0).sum() * HOURS
    days = result.index.normalize().nunique()
    return {
        "revenue_$": round(float(result["revenue"].sum())),
        "energy_charged_mwh": round(float(charged), 1),
        "energy_discharged_mwh": round(float(discharged), 1),
        "cycles_per_day": round(float(discharged / battery.energy_mwh / days), 2),
        "revenue_per_mwh_capacity_$": round(float(result["revenue"].sum() / battery.energy_mwh)),
    }
 
 
def plot_daily_shape(prices, path="figures/daily_price_shape.png"):
    """Average price by hour of day."""
    shape = prices.groupby(prices.index.hour).mean()
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(shape.index, shape.values, marker="o")
    ax.set_xlabel("Hour of day")
    ax.set_ylabel("Average price ($/MWh)")
    ax.set_title("Average VIC spot price by hour")
    ax.grid(alpha=0.3)
    fig.tight_layout()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    return fig
 
 
def plot_soc_vs_price(result, start, end, path="figures/soc_vs_price.png"):
    """Price and state of charge on the same chart for a few days."""
    window = result.loc[start:end]
    fig, ax1 = plt.subplots(figsize=(10, 4))
    ax1.plot(window.index, window["price"], color="tab:gray", lw=1)
    ax1.set_ylabel("Price ($/MWh)")
    # zoom in past rare price spikes so the daily pattern is visible
    ax1.set_ylim(window["price"].min() - 10, window["price"].quantile(0.99) * 1.3)
    ax2 = ax1.twinx()
    ax2.plot(window.index, window["soc_mwh"], color="tab:blue", lw=2)
    ax2.set_ylabel("State of charge (MWh)", color="tab:blue")
    ax1.set_title("Battery state of charge vs price")
    fig.tight_layout()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    return fig
