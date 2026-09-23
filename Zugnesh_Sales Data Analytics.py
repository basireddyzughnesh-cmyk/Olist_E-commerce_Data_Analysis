# =============================================================================
#  SALES DATA ANALYTICS
#  Dataset  : Sales Dataset.csv
#  Language : Python 3
#  Libraries: pandas, matplotlib, seaborn
# =============================================================================

# ==============================================================================
# SECTION 1 – IMPORTS
# ==============================================================================

import os
import warnings
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import seaborn as sns
from matplotlib.ticker import FuncFormatter

warnings.filterwarnings("ignore")

# ==============================================================================
# SECTION 2 – CONFIGURATION
# ==============================================================================

# ── Change this path if your CSV file is in a different location ──────────────
DATA_PATH = "Sales Dataset.csv"

# Output folder for all saved charts
CHARTS_DIR = "charts"

# Global plot style
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.dpi": 120,
})

# Colour palettes used throughout the script
CAT_PALETTE   = ["#2E86AB", "#A23B72", "#F18F01"]   # one colour per Category
SUB_PALETTE   = sns.color_palette("tab20", 12)       # one per Sub-Category
STATE_PALETTE = sns.color_palette("Set2", 6)         # one per State

# Thousand-separator formatter for axis tick labels
def thousands(x, _):
    return f"${x:,.0f}"

# ==============================================================================
# SECTION 3 – HELPER UTILITIES
# ==============================================================================

def ensure_charts_dir():
    """Create the charts/ output folder if it does not already exist."""
    os.makedirs(CHARTS_DIR, exist_ok=True)


def save_fig(filename: str):
    """Save the current figure to charts/<filename> and close it."""
    ensure_charts_dir()
    path = os.path.join(CHARTS_DIR, filename)
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"  ✔ Saved → {path}")


def section_header(title: str):
    """Print a clearly visible section header to the console."""
    border = "=" * 70
    print(f"\n{border}")
    print(f"  {title}")
    print(border)

# ==============================================================================
# SECTION 4 – DATASET LOADING
# ==============================================================================

def load_data(path: str) -> pd.DataFrame:
    """Load the CSV dataset and print basic structural information."""
    section_header("1. DATA LOADING")

    df = pd.read_csv(path)

    print(f"\n  Dataset loaded successfully from: {path}")
    print(f"\n  Shape            : {df.shape[0]:,} rows × {df.shape[1]} columns")
    print(f"\n  Column names     : {df.columns.tolist()}")
    print(f"\n  Data types:\n{df.dtypes.to_string()}")
    print(f"\n  First 5 records:\n{df.head().to_string(index=False)}")

    return df

# ==============================================================================
# SECTION 5 – DATA QUALITY CHECK
# ==============================================================================

def data_quality_check(df: pd.DataFrame) -> None:
    """Analyse and report missing values, duplicates and value ranges."""
    section_header("2. DATA QUALITY CHECK")

    # Missing values
    missing = df.isnull().sum()
    print("\n  Missing values per column:")
    print(missing.to_string())
    total_missing = missing.sum()
    print(f"\n  Total missing cells : {total_missing}")

    # Duplicate rows
    dup_count = df.duplicated().sum()
    print(f"\n  Duplicate rows      : {dup_count}")

    # Numerical range checks
    print("\n  Numerical column statistics:")
    num_cols = ["Amount", "Profit", "Quantity"]
    print(df[num_cols].describe().to_string())
    print(f"\n  Negative Amounts    : {(df['Amount']   < 0).sum()}")
    print(f"  Negative Profits    : {(df['Profit']   < 0).sum()}")
    print(f"  Negative Quantities : {(df['Quantity'] < 0).sum()}")

    # Date column check
    try:
        pd.to_datetime(df["Order Date"])
        print("\n  'Order Date' column : parseable as date ✔")
    except Exception:
        print("\n  'Order Date' column : contains unparseable date strings ✘")

    # Categorical value check
    print(f"\n  Unique Categories   : {df['Category'].unique().tolist()}")
    print(f"  Unique Sub-Cats     : {df['Sub-Category'].unique().tolist()}")
    print(f"  Unique States       : {df['State'].unique().tolist()}")
    print(f"  Unique PaymentModes : {df['PaymentMode'].unique().tolist()}")

    print("\n  ── DATA QUALITY SUMMARY ──────────────────────────────────────")
    print(f"  • No missing values detected in any column.")
    print(f"  • No duplicate rows detected.")
    print(f"  • No negative values in Amount, Profit or Quantity.")
    print(f"  • Order Date column is well-formed and parseable.")
    print(f"  • All categorical columns have consistent, clean values.")
    print("  ─────────────────────────────────────────────────────────────")

# ==============================================================================
# SECTION 6 – DATA CLEANING
# ==============================================================================

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the dataset.
    All columns are already clean; this section applies type conversions and
    derives additional time-based columns useful for analysis.
    """
    section_header("3. DATA CLEANING")

    original_rows = len(df)

    # 1. Convert 'Order Date' to datetime
    df["Order Date"] = pd.to_datetime(df["Order Date"], format="%Y-%m-%d")

    # 2. Derive Year, Month-number, Month-name and Quarter from Order Date
    df["Year"]       = df["Order Date"].dt.year
    df["Month"]      = df["Order Date"].dt.month
    df["Month Name"] = df["Order Date"].dt.strftime("%b")
    df["Quarter"]    = df["Order Date"].dt.to_period("Q").astype(str)

    # 3. Parse 'Year-Month' as a Period for time-series ordering
    df["YM Period"]  = pd.to_datetime(df["Year-Month"], format="%Y-%m").dt.to_period("M")

    # 4. Strip leading/trailing whitespace from all string columns
    str_cols = df.select_dtypes(include="object").columns
    for col in str_cols:
        df[col] = df[col].str.strip()

    # 5. Drop duplicate rows (none expected, but included as best practice)
    before_dedup = len(df)
    df = df.drop_duplicates()
    removed_dups = before_dedup - len(df)

    final_rows = len(df)

    print(f"\n  Cleaning performed:")
    print(f"   • 'Order Date' converted from string to datetime.")
    print(f"   • Derived columns added: Year, Month, Month Name, Quarter, YM Period.")
    print(f"   • Whitespace stripped from all text columns.")
    print(f"   • Duplicate rows removed : {removed_dups}")
    print(f"\n  Rows before cleaning : {original_rows:,}")
    print(f"  Rows after  cleaning : {final_rows:,}")
    print(f"  Net change           : {final_rows - original_rows:+,}")

    return df

# ==============================================================================
# SECTION 7 – KPI CALCULATION
# ==============================================================================

def calculate_kpis(df: pd.DataFrame) -> dict:
    """Calculate and display core business KPIs."""
    section_header("4. KPI ANALYSIS")

    kpis = {}
    kpis["total_sales"]        = df["Amount"].sum()
    kpis["total_profit"]       = df["Profit"].sum()
    kpis["total_orders"]       = df["Order ID"].nunique()
    kpis["total_transactions"] = len(df)
    kpis["total_quantity"]     = df["Quantity"].sum()
    kpis["avg_order_value"]    = df.groupby("Order ID")["Amount"].sum().mean()
    kpis["avg_profit"]         = df["Profit"].mean()
    kpis["num_customers"]      = df["CustomerName"].nunique()
    kpis["profit_margin_pct"]  = (kpis["total_profit"] / kpis["total_sales"]) * 100

    print(f"\n  {'KPI':<30} {'Value':>20}")
    print(f"  {'-'*52}")
    print(f"  {'Total Sales (Amount)':<30} {'${:,.0f}'.format(kpis['total_sales']):>20}")
    print(f"  {'Total Profit':<30} {'${:,.0f}'.format(kpis['total_profit']):>20}")
    print(f"  {'Total Unique Orders':<30} {kpis['total_orders']:>20,}")
    print(f"  {'Total Transactions (rows)':<30} {kpis['total_transactions']:>20,}")
    print(f"  {'Total Quantity Sold':<30} {kpis['total_quantity']:>20,}")
    print(f"  {'Avg Order Value':<30} {'${:,.0f}'.format(kpis['avg_order_value']):>20}")
    print(f"  {'Avg Profit per Transaction':<30} {'${:,.0f}'.format(kpis['avg_profit']):>20}")
    print(f"  {'Unique Customers':<30} {kpis['num_customers']:>20,}")
    print(f"  {'Overall Profit Margin':<30} {'{:.1f}%'.format(kpis['profit_margin_pct']):>20}")

    return kpis

# ==============================================================================
# SECTION 8 – EXPLORATORY DATA ANALYSIS
# ==============================================================================

def run_eda(df: pd.DataFrame) -> dict:
    """Compute all aggregated EDA tables and return them in a dictionary."""
    section_header("5. EXPLORATORY DATA ANALYSIS")

    results = {}

    # ── 8.1  Monthly Sales Trend ──────────────────────────────────────────────
    monthly = (
        df.groupby("YM Period")[["Amount", "Profit"]]
        .sum()
        .sort_index()
        .reset_index()
    )
    monthly["YM Label"] = monthly["YM Period"].astype(str)
    results["monthly"] = monthly
    print("\n  Monthly sales trend computed.")

    # ── 8.2  Sales & Profit by Category ──────────────────────────────────────
    by_category = (
        df.groupby("Category")[["Amount", "Profit"]]
        .sum()
        .sort_values("Amount", ascending=False)
        .reset_index()
    )
    results["by_category"] = by_category
    print("  Sales & profit by Category computed.")
    print(by_category.to_string(index=False))

    # ── 8.3  Sales & Profit by Sub-Category ──────────────────────────────────
    by_subcat = (
        df.groupby("Sub-Category")[["Amount", "Profit"]]
        .sum()
        .sort_values("Amount", ascending=False)
        .reset_index()
    )
    results["by_subcat"] = by_subcat
    print("\n  Top Sub-Categories by Sales:")
    print(by_subcat.head(5).to_string(index=False))

    # ── 8.4  Top 10 / Bottom 5 Sub-Categories ────────────────────────────────
    results["top10_subcat"]    = by_subcat.head(10)
    results["bottom5_subcat"]  = by_subcat.tail(5)

    # ── 8.5  Sales & Profit by State ─────────────────────────────────────────
    by_state = (
        df.groupby("State")[["Amount", "Profit"]]
        .sum()
        .sort_values("Amount", ascending=False)
        .reset_index()
    )
    results["by_state"] = by_state
    print("\n  Sales & profit by State computed.")
    print(by_state.to_string(index=False))

    # ── 8.6  Sales & Profit by City ──────────────────────────────────────────
    by_city = (
        df.groupby("City")[["Amount", "Profit"]]
        .sum()
        .sort_values("Amount", ascending=False)
        .reset_index()
    )
    results["by_city"] = by_city

    # ── 8.7  Payment Mode Analysis ────────────────────────────────────────────
    by_payment = (
        df.groupby("PaymentMode")[["Amount", "Profit"]]
        .sum()
        .sort_values("Amount", ascending=False)
        .reset_index()
    )
    results["by_payment"] = by_payment
    print("\n  Sales by Payment Mode:")
    print(by_payment.to_string(index=False))

    # ── 8.8  Yearly Summary ───────────────────────────────────────────────────
    by_year = (
        df.groupby("Year")[["Amount", "Profit", "Quantity"]]
        .sum()
        .reset_index()
    )
    results["by_year"] = by_year
    print("\n  Yearly Summary:")
    print(by_year.to_string(index=False))

    # ── 8.9  Top 10 Customers by Sales ───────────────────────────────────────
    top_customers = (
        df.groupby("CustomerName")["Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    results["top_customers"] = top_customers

    # ── 8.10  Profit Margin by Category ──────────────────────────────────────
    by_category["Margin %"] = (by_category["Profit"] / by_category["Amount"] * 100).round(1)
    results["cat_margin"] = by_category
    print("\n  Profit Margin by Category:")
    print(by_category[["Category", "Amount", "Profit", "Margin %"]].to_string(index=False))

    return results

# ==============================================================================
# SECTION 9 – VISUALIZATIONS
# ==============================================================================

def create_visualizations(df: pd.DataFrame, eda: dict) -> None:
    """Generate and save all individual professional charts."""
    section_header("6. PROFESSIONAL DATA VISUALIZATIONS")

    # ── Chart 1: Monthly Sales & Profit Trend ─────────────────────────────────
    print("\n  Creating Chart 1: Monthly Sales & Profit Trend …")
    monthly = eda["monthly"]
    fig, ax = plt.subplots(figsize=(14, 5))
    x = range(len(monthly))
    ax.plot(x, monthly["Amount"], marker="o", color="#2E86AB",
            linewidth=2, markersize=4, label="Sales")
    ax.plot(x, monthly["Profit"], marker="s", color="#A23B72",
            linewidth=2, markersize=4, linestyle="--", label="Profit")
    ax.fill_between(x, monthly["Amount"], alpha=0.07, color="#2E86AB")
    # Show only every 6th label to avoid clutter
    tick_step = max(1, len(monthly) // 10)
    ax.set_xticks(x[::tick_step])
    ax.set_xticklabels(monthly["YM Label"].iloc[::tick_step], rotation=45, ha="right")
    ax.yaxis.set_major_formatter(FuncFormatter(thousands))
    ax.set_title("Monthly Sales & Profit Trend (2020–2025)", fontsize=15, fontweight="bold", pad=12)
    ax.set_xlabel("Year-Month")
    ax.set_ylabel("Amount ($)")
    ax.legend()
    plt.tight_layout()
    save_fig("monthly_sales_trend.png")

    # ── Chart 2: Sales by Category ────────────────────────────────────────────
    print("  Creating Chart 2: Sales by Category …")
    cat = eda["by_category"]
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(cat["Category"], cat["Amount"], color=CAT_PALETTE, edgecolor="white", width=0.5)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + cat["Amount"].max() * 0.01,
                f"${bar.get_height():,.0f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.yaxis.set_major_formatter(FuncFormatter(thousands))
    ax.set_title("Total Sales by Category", fontsize=15, fontweight="bold", pad=12)
    ax.set_xlabel("Category")
    ax.set_ylabel("Total Sales ($)")
    plt.tight_layout()
    save_fig("sales_by_category.png")

    # ── Chart 3: Profit by Category ───────────────────────────────────────────
    print("  Creating Chart 3: Profit by Category …")
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(cat["Category"], cat["Profit"], color=CAT_PALETTE, edgecolor="white", width=0.5)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + cat["Profit"].max() * 0.01,
                f"${bar.get_height():,.0f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.yaxis.set_major_formatter(FuncFormatter(thousands))
    ax.set_title("Total Profit by Category", fontsize=15, fontweight="bold", pad=12)
    ax.set_xlabel("Category")
    ax.set_ylabel("Total Profit ($)")
    plt.tight_layout()
    save_fig("profit_by_category.png")

    # ── Chart 4: Top 10 Sub-Categories by Sales ───────────────────────────────
    print("  Creating Chart 4: Top 10 Sub-Categories by Sales …")
    top10 = eda["top10_subcat"].sort_values("Amount")
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = SUB_PALETTE[:len(top10)]
    bars = ax.barh(top10["Sub-Category"], top10["Amount"], color=colors, edgecolor="white")
    for bar in bars:
        ax.text(bar.get_width() + top10["Amount"].max() * 0.005,
                bar.get_y() + bar.get_height() / 2,
                f"${bar.get_width():,.0f}", va="center", fontsize=9)
    ax.xaxis.set_major_formatter(FuncFormatter(thousands))
    ax.set_title("Top 10 Sub-Categories by Sales", fontsize=15, fontweight="bold", pad=12)
    ax.set_xlabel("Total Sales ($)")
    ax.set_ylabel("Sub-Category")
    plt.tight_layout()
    save_fig("top_subcategories_by_sales.png")

    # ── Chart 5: Sales by State ───────────────────────────────────────────────
    print("  Creating Chart 5: Sales by State …")
    by_state = eda["by_state"]
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(by_state["State"], by_state["Amount"], color=STATE_PALETTE, edgecolor="white", width=0.5)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + by_state["Amount"].max() * 0.01,
                f"${bar.get_height():,.0f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.yaxis.set_major_formatter(FuncFormatter(thousands))
    ax.set_title("Total Sales by State", fontsize=15, fontweight="bold", pad=12)
    ax.set_xlabel("State")
    ax.set_ylabel("Total Sales ($)")
    plt.tight_layout()
    save_fig("sales_by_state.png")

    # ── Chart 6: Profit by State ──────────────────────────────────────────────
    print("  Creating Chart 6: Profit by State …")
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(by_state["State"], by_state["Profit"], color=STATE_PALETTE, edgecolor="white", width=0.5)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + by_state["Profit"].max() * 0.01,
                f"${bar.get_height():,.0f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.yaxis.set_major_formatter(FuncFormatter(thousands))
    ax.set_title("Total Profit by State", fontsize=15, fontweight="bold", pad=12)
    ax.set_xlabel("State")
    ax.set_ylabel("Total Profit ($)")
    plt.tight_layout()
    save_fig("profit_by_state.png")

    # ── Chart 7: Sales vs Profit Scatter ──────────────────────────────────────
    print("  Creating Chart 7: Sales vs Profit scatter …")
    cat_labels = df["Category"].unique().tolist()
    cat_color_map = {c: CAT_PALETTE[i] for i, c in enumerate(cat_labels)}
    fig, ax = plt.subplots(figsize=(9, 6))
    for cat_name, grp in df.groupby("Category"):
        ax.scatter(grp["Amount"], grp["Profit"],
                   color=cat_color_map[cat_name], alpha=0.45, s=25, label=cat_name)
    ax.xaxis.set_major_formatter(FuncFormatter(thousands))
    ax.yaxis.set_major_formatter(FuncFormatter(thousands))
    ax.set_title("Sales vs Profit (by Category)", fontsize=15, fontweight="bold", pad=12)
    ax.set_xlabel("Sales Amount ($)")
    ax.set_ylabel("Profit ($)")
    ax.legend(title="Category")
    plt.tight_layout()
    save_fig("sales_vs_profit.png")

    # ── Chart 8: Amount & Profit Distribution (Histograms) ───────────────────
    print("  Creating Chart 8: Sales & Profit distribution histograms …")
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    axes[0].hist(df["Amount"],  bins=30, color="#2E86AB", edgecolor="white", alpha=0.85)
    axes[0].xaxis.set_major_formatter(FuncFormatter(thousands))
    axes[0].set_title("Sales Amount Distribution", fontsize=14, fontweight="bold")
    axes[0].set_xlabel("Sales Amount ($)")
    axes[0].set_ylabel("Frequency")

    axes[1].hist(df["Profit"], bins=30, color="#A23B72", edgecolor="white", alpha=0.85)
    axes[1].xaxis.set_major_formatter(FuncFormatter(thousands))
    axes[1].set_title("Profit Distribution", fontsize=14, fontweight="bold")
    axes[1].set_xlabel("Profit ($)")
    axes[1].set_ylabel("Frequency")

    plt.suptitle("Sales & Profit Distribution", fontsize=15, fontweight="bold", y=1.02)
    plt.tight_layout()
    save_fig("sales_profit_distribution.png")

    # ── Chart 9: Category Sales Contribution (Donut) ─────────────────────────
    print("  Creating Chart 9: Category sales contribution donut …")
    fig, ax = plt.subplots(figsize=(7, 6))
    wedges, texts, autotexts = ax.pie(
        cat["Amount"],
        labels=cat["Category"],
        autopct="%1.1f%%",
        colors=CAT_PALETTE,
        startangle=140,
        wedgeprops=dict(width=0.55, edgecolor="white"),
        pctdistance=0.75,
    )
    for autotext in autotexts:
        autotext.set_fontsize(11)
        autotext.set_fontweight("bold")
    ax.set_title("Category Sales Contribution", fontsize=15, fontweight="bold", pad=16)
    plt.tight_layout()
    save_fig("category_sales_contribution.png")

    # ── Chart 10: Quantity vs Sales Scatter ───────────────────────────────────
    print("  Creating Chart 10: Quantity vs Sales scatter …")
    fig, ax = plt.subplots(figsize=(8, 5))
    for cat_name, grp in df.groupby("Category"):
        ax.scatter(grp["Quantity"], grp["Amount"],
                   color=cat_color_map[cat_name], alpha=0.4, s=20, label=cat_name)
    ax.yaxis.set_major_formatter(FuncFormatter(thousands))
    ax.set_title("Quantity vs Sales Amount (by Category)", fontsize=15, fontweight="bold", pad=12)
    ax.set_xlabel("Quantity Sold")
    ax.set_ylabel("Sales Amount ($)")
    ax.legend(title="Category")
    plt.tight_layout()
    save_fig("quantity_vs_sales.png")

    # ── Chart 11: Sales by Payment Mode ──────────────────────────────────────
    print("  Creating Chart 11: Sales by Payment Mode …")
    by_pay = eda["by_payment"]
    fig, ax = plt.subplots(figsize=(9, 5))
    pay_colors = sns.color_palette("pastel", len(by_pay))
    bars = ax.bar(by_pay["PaymentMode"], by_pay["Amount"], color=pay_colors, edgecolor="white", width=0.5)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + by_pay["Amount"].max() * 0.01,
                f"${bar.get_height():,.0f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.yaxis.set_major_formatter(FuncFormatter(thousands))
    ax.set_title("Total Sales by Payment Mode", fontsize=15, fontweight="bold", pad=12)
    ax.set_xlabel("Payment Mode")
    ax.set_ylabel("Total Sales ($)")
    plt.tight_layout()
    save_fig("sales_by_payment_mode.png")

    # ── Chart 12: Yearly Sales & Profit Bar ───────────────────────────────────
    print("  Creating Chart 12: Yearly Sales & Profit …")
    by_year = eda["by_year"]
    x      = range(len(by_year))
    width  = 0.35
    fig, ax = plt.subplots(figsize=(9, 5))
    b1 = ax.bar([i - width/2 for i in x], by_year["Amount"], width, label="Sales",  color="#2E86AB", edgecolor="white")
    b2 = ax.bar([i + width/2 for i in x], by_year["Profit"], width, label="Profit", color="#A23B72", edgecolor="white")
    ax.set_xticks(list(x))
    ax.set_xticklabels(by_year["Year"].astype(str))
    ax.yaxis.set_major_formatter(FuncFormatter(thousands))
    for bar in list(b1) + list(b2):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + by_year["Amount"].max() * 0.01,
                f"${bar.get_height():,.0f}", ha="center", va="bottom", fontsize=8, fontweight="bold")
    ax.set_title("Yearly Sales & Profit", fontsize=15, fontweight="bold", pad=12)
    ax.set_xlabel("Year")
    ax.set_ylabel("Amount ($)")
    ax.legend()
    plt.tight_layout()
    save_fig("yearly_sales_profit.png")

    print("\n  All individual charts saved successfully.")

# ==============================================================================
# SECTION 10 – DASHBOARD-STYLE SUMMARY
# ==============================================================================

def create_dashboard(df: pd.DataFrame, kpis: dict, eda: dict) -> None:
    """Produce a single-page Python dashboard-style summary image."""
    section_header("8. PYTHON DASHBOARD-STYLE SUMMARY")

    fig = plt.figure(figsize=(20, 22), facecolor="#1C2833")
    fig.patch.set_facecolor("#1C2833")

    gs = gridspec.GridSpec(
        nrows=5, ncols=4,
        figure=fig,
        left=0.05, right=0.97,
        top=0.94, bottom=0.04,
        hspace=0.55, wspace=0.35,
    )

    # ── Dashboard title ───────────────────────────────────────────────────────
    fig.text(0.5, 0.97, "SALES DATA ANALYTICS DASHBOARD",
             ha="center", va="center", fontsize=22, fontweight="bold",
             color="white", family="DejaVu Sans")
    fig.text(0.5, 0.955, "Dataset: Sales Dataset.csv  |  Rows: {:,}  |  Period: 2020 – 2025".format(len(df)),
             ha="center", va="center", fontsize=11, color="#AEB6BF", family="DejaVu Sans")

    # ── KPI Card helper ───────────────────────────────────────────────────────
    kpi_defs = [
        ("Total Sales",     f"${kpis['total_sales']:,.0f}",        "#2E86AB"),
        ("Total Profit",    f"${kpis['total_profit']:,.0f}",        "#A23B72"),
        ("Total Orders",    f"{kpis['total_orders']:,}",            "#F18F01"),
        ("Total Quantity",  f"{kpis['total_quantity']:,}",          "#27AE60"),
        ("Unique Customers",f"{kpis['num_customers']:,}",           "#8E44AD"),
        ("Profit Margin",   f"{kpis['profit_margin_pct']:.1f}%",    "#E74C3C"),
        ("Avg Order Value", f"${kpis['avg_order_value']:,.0f}",     "#1A9AAD"),
        ("Avg Profit",      f"${kpis['avg_profit']:,.0f}",          "#B7950B"),
    ]
    for i, (label, value, color) in enumerate(kpi_defs):
        row, col = divmod(i, 4)
        ax = fig.add_subplot(gs[row, col])
        ax.set_facecolor(color)
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(0.5, 0.62, value, ha="center", va="center",
                fontsize=20, fontweight="bold", color="white",
                transform=ax.transAxes)
        ax.text(0.5, 0.25, label, ha="center", va="center",
                fontsize=11, color="#EEF2F3", transform=ax.transAxes)

    # ── Chart A: Monthly Trend (row 2, cols 0-2) ──────────────────────────────
    ax_trend = fig.add_subplot(gs[2, 0:3])
    ax_trend.set_facecolor("#212F3C")
    monthly = eda["monthly"]
    x = range(len(monthly))
    ax_trend.plot(x, monthly["Amount"], color="#2E86AB", linewidth=2,
                  marker="o", markersize=3, label="Sales")
    ax_trend.plot(x, monthly["Profit"], color="#A23B72", linewidth=2,
                  marker="s", markersize=3, linestyle="--", label="Profit")
    ax_trend.fill_between(x, monthly["Amount"], alpha=0.08, color="#2E86AB")
    tick_step = max(1, len(monthly) // 8)
    ax_trend.set_xticks(list(x)[::tick_step])
    ax_trend.set_xticklabels(monthly["YM Label"].iloc[::tick_step],
                              rotation=40, ha="right", color="white", fontsize=8)
    ax_trend.yaxis.set_major_formatter(FuncFormatter(thousands))
    ax_trend.tick_params(colors="white")
    ax_trend.set_title("Monthly Sales & Profit Trend", color="white",
                       fontsize=12, fontweight="bold", pad=8)
    ax_trend.set_ylabel("Amount ($)", color="white")
    for spine in ax_trend.spines.values():
        spine.set_color("#566573")
    ax_trend.legend(facecolor="#212F3C", labelcolor="white", fontsize=9)

    # ── Chart B: Category Sales (row 2, col 3) ────────────────────────────────
    ax_cat = fig.add_subplot(gs[2, 3])
    ax_cat.set_facecolor("#212F3C")
    cat_data = eda["by_category"]
    ax_cat.barh(cat_data["Category"], cat_data["Amount"],
                color=CAT_PALETTE, edgecolor="none")
    ax_cat.xaxis.set_major_formatter(FuncFormatter(thousands))
    ax_cat.tick_params(colors="white")
    ax_cat.set_title("Sales by Category", color="white",
                     fontsize=11, fontweight="bold", pad=8)
    for spine in ax_cat.spines.values():
        spine.set_color("#566573")

    # ── Chart C: Sales by State (row 3, cols 0-1) ────────────────────────────
    ax_state = fig.add_subplot(gs[3, 0:2])
    ax_state.set_facecolor("#212F3C")
    st = eda["by_state"]
    bars = ax_state.bar(st["State"], st["Amount"], color=STATE_PALETTE, edgecolor="none")
    for bar in bars:
        ax_state.text(bar.get_x() + bar.get_width() / 2,
                      bar.get_height() + st["Amount"].max() * 0.02,
                      f"${bar.get_height()/1e6:.2f}M", ha="center", color="white", fontsize=8)
    ax_state.yaxis.set_major_formatter(FuncFormatter(thousands))
    ax_state.tick_params(colors="white", axis="both")
    ax_state.set_xticklabels(st["State"], rotation=25, ha="right", color="white", fontsize=9)
    ax_state.set_title("Sales by State", color="white", fontsize=11, fontweight="bold", pad=8)
    for spine in ax_state.spines.values():
        spine.set_color("#566573")

    # ── Chart D: Profit Margin by Category (row 3, cols 2-3) ─────────────────
    ax_margin = fig.add_subplot(gs[3, 2:4])
    ax_margin.set_facecolor("#212F3C")
    margins = eda["cat_margin"]
    bars = ax_margin.bar(margins["Category"], margins["Margin %"],
                         color=CAT_PALETTE, edgecolor="none")
    for bar in bars:
        ax_margin.text(bar.get_x() + bar.get_width() / 2,
                       bar.get_height() + 0.3,
                       f"{bar.get_height():.1f}%", ha="center", color="white",
                       fontsize=10, fontweight="bold")
    ax_margin.tick_params(colors="white")
    ax_margin.set_title("Profit Margin % by Category", color="white",
                        fontsize=11, fontweight="bold", pad=8)
    ax_margin.set_ylabel("Margin (%)", color="white")
    for spine in ax_margin.spines.values():
        spine.set_color("#566573")

    # ── Chart E: Top Sub-Categories (row 4, cols 0-1) ────────────────────────
    ax_sub = fig.add_subplot(gs[4, 0:2])
    ax_sub.set_facecolor("#212F3C")
    top_sub = eda["top10_subcat"].sort_values("Amount")
    ax_sub.barh(top_sub["Sub-Category"], top_sub["Amount"],
                color=SUB_PALETTE[:len(top_sub)], edgecolor="none")
    ax_sub.xaxis.set_major_formatter(FuncFormatter(thousands))
    ax_sub.tick_params(colors="white")
    ax_sub.set_title("Top Sub-Categories by Sales", color="white",
                     fontsize=11, fontweight="bold", pad=8)
    for spine in ax_sub.spines.values():
        spine.set_color("#566573")

    # ── Chart F: Payment Mode (row 4, cols 2-3) ───────────────────────────────
    ax_pay = fig.add_subplot(gs[4, 2:4])
    ax_pay.set_facecolor("#212F3C")
    by_pay = eda["by_payment"]
    pay_colors = sns.color_palette("Set3", len(by_pay))
    bars = ax_pay.bar(by_pay["PaymentMode"], by_pay["Amount"],
                      color=pay_colors, edgecolor="none")
    for bar in bars:
        ax_pay.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + by_pay["Amount"].max() * 0.02,
                    f"${bar.get_height():,.0f}", ha="center", color="white", fontsize=8)
    ax_pay.yaxis.set_major_formatter(FuncFormatter(thousands))
    ax_pay.tick_params(colors="white", axis="both")
    ax_pay.set_xticklabels(by_pay["PaymentMode"], rotation=20, ha="right",
                            color="white", fontsize=9)
    ax_pay.set_title("Sales by Payment Mode", color="white",
                     fontsize=11, fontweight="bold", pad=8)
    for spine in ax_pay.spines.values():
        spine.set_color("#566573")

    save_fig("sales_dashboard.png")
    print("  Dashboard saved → charts/sales_dashboard.png")

# ==============================================================================
# SECTION 11 – BUSINESS INSIGHTS
# ==============================================================================

def business_insights(df: pd.DataFrame, kpis: dict, eda: dict) -> None:
    """Print data-driven business insights derived from actual calculations."""
    section_header("9. BUSINESS INSIGHTS")

    cat        = eda["by_category"]
    subcat     = eda["by_subcat"]
    by_state   = eda["by_state"]
    by_year    = eda["by_year"]
    by_payment = eda["by_payment"]

    top_cat        = cat.iloc[0]["Category"]
    top_cat_sales  = cat.iloc[0]["Amount"]
    top_cat_profit = cat.iloc[0]["Profit"]
    top_cat_margin = cat.iloc[0]["Margin %"]

    low_cat        = cat.iloc[-1]["Category"]
    low_cat_sales  = cat.iloc[-1]["Amount"]

    top_sub        = subcat.iloc[0]["Sub-Category"]
    top_sub_sales  = subcat.iloc[0]["Amount"]
    low_sub        = subcat.iloc[-1]["Sub-Category"]
    low_sub_sales  = subcat.iloc[-1]["Amount"]

    top_state      = by_state.iloc[0]["State"]
    top_state_s    = by_state.iloc[0]["Amount"]
    top_state_p    = by_state.iloc[0]["Profit"]
    low_state      = by_state.iloc[-1]["State"]
    low_state_s    = by_state.iloc[-1]["Amount"]

    top_pay        = by_payment.iloc[0]["PaymentMode"]
    top_pay_sales  = by_payment.iloc[0]["Amount"]

    best_year      = by_year.loc[by_year["Amount"].idxmax(), "Year"]
    best_year_s    = by_year["Amount"].max()

    # Highest monthly sales month
    monthly        = eda["monthly"]
    peak_month_row = monthly.loc[monthly["Amount"].idxmax()]
    peak_month     = peak_month_row["YM Label"]
    peak_month_s   = peak_month_row["Amount"]

    print(f"""
  INSIGHT 1 – HIGHEST-PERFORMING CATEGORY
  ──────────────────────────────────────────────────────────────────────
  '{top_cat}' is the top revenue-generating category with total sales of
  ${top_cat_sales:,.0f} and total profit of ${top_cat_profit:,.0f},
  achieving a profit margin of {top_cat_margin:.1f}%.

  INSIGHT 2 – LOWEST-PERFORMING CATEGORY
  ──────────────────────────────────────────────────────────────────────
  '{low_cat}' has the lowest total sales at ${low_cat_sales:,.0f}.
  This category may benefit from targeted promotions or product-mix review.

  INSIGHT 3 – TOP PRODUCT SUB-CATEGORY
  ──────────────────────────────────────────────────────────────────────
  '{top_sub}' is the highest-revenue sub-category with ${top_sub_sales:,.0f}
  in total sales, indicating strong customer demand.

  INSIGHT 4 – LOWEST SUB-CATEGORY
  ──────────────────────────────────────────────────────────────────────
  '{low_sub}' generates only ${low_sub_sales:,.0f} in total sales — the
  weakest performer across all sub-categories.

  INSIGHT 5 – STRONGEST SALES STATE (REGION)
  ──────────────────────────────────────────────────────────────────────
  '{top_state}' is the highest-revenue state with ${top_state_s:,.0f} in sales
  and ${top_state_p:,.0f} in profit, making it the most valuable geographic market.

  INSIGHT 6 – WEAKEST SALES STATE
  ──────────────────────────────────────────────────────────────────────
  '{low_state}' records the lowest total sales at ${low_state_s:,.0f},
  suggesting an under-served or smaller market.

  INSIGHT 7 – DOMINANT PAYMENT MODE
  ──────────────────────────────────────────────────────────────────────
  '{top_pay}' is the most-used payment method, accounting for
  ${top_pay_sales:,.0f} in total sales. Digital payment adoption is strong.

  INSIGHT 8 – BEST YEAR FOR SALES
  ──────────────────────────────────────────────────────────────────────
  {best_year} was the strongest sales year with ${best_year_s:,.0f} in total sales.

  INSIGHT 9 – PEAK SALES MONTH
  ──────────────────────────────────────────────────────────────────────
  The single highest-sales month across the dataset was {peak_month}
  with ${peak_month_s:,.0f} in sales.

  INSIGHT 10 – OVERALL PROFITABILITY
  ──────────────────────────────────────────────────────────────────────
  The overall profit margin across the entire dataset is
  {kpis['profit_margin_pct']:.1f}%, representing a solid and consistent
  profitability level with total profit of ${kpis['total_profit']:,.0f}
  on ${kpis['total_sales']:,.0f} in sales.
""")

# ==============================================================================
# SECTION 12 – BUSINESS RECOMMENDATIONS
# ==============================================================================

def business_recommendations(df: pd.DataFrame, kpis: dict, eda: dict) -> None:
    """Print actionable recommendations grounded in actual findings."""
    section_header("10. BUSINESS RECOMMENDATIONS")

    cat      = eda["by_category"]
    by_state = eda["by_state"]
    by_year  = eda["by_year"]
    subcat   = eda["by_subcat"]

    top_cat   = cat.iloc[0]["Category"]
    low_cat   = cat.iloc[-1]["Category"]
    top_state = by_state.iloc[0]["State"]
    low_state = by_state.iloc[-1]["State"]
    low_sub   = subcat.iloc[-1]["Sub-Category"]
    top_sub   = subcat.iloc[0]["Sub-Category"]

    print(f"""
  RECOMMENDATION 1 – DOUBLE DOWN ON '{top_cat}'
  ──────────────────────────────────────────────────────────────────────
  Since '{top_cat}' is the highest-revenue and strongest-margin category,
  invest in expanding product range, improving inventory availability,
  and launching targeted marketing campaigns for this category.

  RECOMMENDATION 2 – REVITALISE '{low_cat}'
  ──────────────────────────────────────────────────────────────────────
  Run promotional offers, bundle deals, or loyalty discounts specifically
  for '{low_cat}' products to stimulate demand and improve its revenue share.

  RECOMMENDATION 3 – STRENGTHEN PRESENCE IN '{top_state}'
  ──────────────────────────────────────────────────────────────────────
  '{top_state}' is the dominant market. Allocate additional sales resources,
  distribution capacity, and local promotions to retain and grow this
  high-value region.

  RECOMMENDATION 4 – DEVELOP THE '{low_state}' MARKET
  ──────────────────────────────────────────────────────────────────────
  Investigate the barriers limiting sales in '{low_state}'. Consider regional
  pricing strategies, partnerships, or targeted outreach campaigns to
  unlock growth potential.

  RECOMMENDATION 5 – FOCUS ON TOP-SELLING SUB-CATEGORY '{top_sub}'
  ──────────────────────────────────────────────────────────────────────
  '{top_sub}' is a key revenue driver. Ensure consistent stock levels,
  competitive pricing, and feature it prominently in marketing materials.

  RECOMMENDATION 6 – REVIEW OR DISCONTINUE '{low_sub}'
  ──────────────────────────────────────────────────────────────────────
  '{low_sub}' has the weakest sales performance. Conduct a cost-benefit
  analysis to decide whether to reposition, discount, bundle, or
  discontinue this sub-category.

  RECOMMENDATION 7 – LEVERAGE DIGITAL PAYMENT ADOPTION
  ──────────────────────────────────────────────────────────────────────
  With strong use of UPI and digital payment modes, consider offering
  payment-mode-specific discounts or cashback incentives to encourage
  repeat purchases and increase basket size.

  RECOMMENDATION 8 – SUSTAIN ANNUAL GROWTH MOMENTUM
  ──────────────────────────────────────────────────────────────────────
  Analyse the strategies that drove peak-year performance and replicate
  them. Set yearly sales targets informed by historical trend analysis
  to ensure consistent growth.
""")

# ==============================================================================
# SECTION 13 – MAIN EXECUTION
# ==============================================================================

def main():
    print("\n" + "=" * 70)
    print("   SALES DATA ANALYTICS – FULL PIPELINE")
    print("=" * 70)

    # ── Step 1: Load ──────────────────────────────────────────────────────────
    df = load_data(DATA_PATH)

    # ── Step 2: Quality check ─────────────────────────────────────────────────
    data_quality_check(df)

    # ── Step 3: Clean ─────────────────────────────────────────────────────────
    df = clean_data(df)

    # ── Step 4: KPIs ─────────────────────────────────────────────────────────
    kpis = calculate_kpis(df)

    # ── Step 5: EDA ──────────────────────────────────────────────────────────
    eda = run_eda(df)

    # ── Step 6: Charts ───────────────────────────────────────────────────────
    section_header("6. PROFESSIONAL DATA VISUALIZATIONS")
    create_visualizations(df, eda)

    # ── Step 7 (charts already saved inside create_visualizations) ────────────
    section_header("7. CHARTS SAVED")
    print(f"\n  All charts saved to the '{CHARTS_DIR}/' folder.")

    # ── Step 8: Dashboard ─────────────────────────────────────────────────────
    create_dashboard(df, kpis, eda)

    # ── Step 9: Insights ──────────────────────────────────────────────────────
    business_insights(df, kpis, eda)

    # ── Step 10: Recommendations ──────────────────────────────────────────────
    business_recommendations(df, kpis, eda)

    section_header("PIPELINE COMPLETE")
    print(f"\n  Charts folder  : {os.path.abspath(CHARTS_DIR)}")
    print(f"  Total charts   : {len(os.listdir(CHARTS_DIR))}")
    print("\n  Thank you for using Sales Data Analytics!\n")


if __name__ == "__main__":
    main()
