# Sales Data Analytics

## Project Overview

This project performs a complete end-to-end sales data analysis using Python. It ingests a real-world retail sales dataset, cleans and validates the data, computes key business KPIs, produces 12 individual professional charts plus a full-page dashboard-style summary image, and concludes with data-driven business insights and actionable recommendations — all generated automatically from the dataset using pure Python.

The project is structured as a single, fully executable Python script that can be run by anyone with Python and three standard data science libraries installed.

---

## Problem Statement

Sales organisations generate large volumes of transactional data across multiple product categories, states, customers, and payment modes. Without systematic analysis it is difficult to identify which categories drive the most revenue, which regions are under-performing, or how profitability varies across the business. This project addresses those questions by building a reproducible Python analytics pipeline on top of a real sales dataset.

---

## Objectives

- Load and inspect the raw sales dataset and understand its structure.
- Perform a thorough data quality check (missing values, duplicates, invalid values).
- Clean and enrich the data with derived time-based columns.
- Calculate core business KPIs: Total Sales, Total Profit, Profit Margin, Average Order Value, and more.
- Explore sales and profit patterns across time, categories, sub-categories, states, and payment modes.
- Generate 12 professional charts and a single-page dashboard-style summary image.
- Derive 10 data-driven business insights and 8 actionable recommendations.

---

## Dataset

| Property | Detail |
|---|---|
| **Filename** | `Sales Dataset.csv` |
| **Records** | 1,194 rows |
| **Columns** | 12 |
| **Time period** | 2020 – 2025 |

### Column Reference

| Column | Type | Description |
|---|---|---|
| `Order ID` | String | Unique order identifier |
| `Amount` | Integer | Sales amount per line item ($) |
| `Profit` | Integer | Profit per line item ($) |
| `Quantity` | Integer | Units sold per line item |
| `Category` | String | Product category (Electronics, Furniture, Office Supplies) |
| `Sub-Category` | String | Product sub-category (12 unique values) |
| `PaymentMode` | String | Payment method (UPI, Credit Card, Debit Card, COD, EMI) |
| `Order Date` | String → Date | Date of the transaction (YYYY-MM-DD) |
| `CustomerName` | String | Customer full name |
| `State` | String | US state (Florida, Illinois, New York, California, Texas, Ohio) |
| `City` | String | City within the state |
| `Year-Month` | String | Pre-formatted period label (YYYY-MM) |

---

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3 | Core programming language |
| CSV (flat file) | Data storage format |

---

## Python Libraries

| Library | Version Requirement | Purpose |
|---|---|---|
| `pandas` | >= 2.0.0 | Data loading, cleaning, aggregation |
| `matplotlib` | >= 3.7.0 | Chart generation and dashboard layout |
| `seaborn` | >= 0.13.0 | Colour palettes and plot styling |

> **Built-in modules used** (no installation required): `os`, `warnings`

---

## Project Workflow

```
Sales Dataset.csv
        │
        ▼
┌─────────────────────┐
│   1. Data Loading   │  Read CSV · display shape, columns, dtypes, sample rows
└────────┬────────────┘
         ▼
┌──────────────────────────┐
│  2. Data Quality Check   │  Missing values · duplicates · range checks · date validation
└────────┬─────────────────┘
         ▼
┌─────────────────────┐
│   3. Data Cleaning  │  Type conversion · derived columns · whitespace trim · dedup
└────────┬────────────┘
         ▼
┌──────────────────────┐
│   4. KPI Analysis    │  9 core business metrics calculated from actual data
└────────┬─────────────┘
         ▼
┌───────────────────────────────┐
│  5. Exploratory Data Analysis │  10 aggregation views across time, category, state, payment
└────────┬──────────────────────┘
         ▼
┌─────────────────────────────┐
│  6. Professional Charts ×12 │  Individual PNG charts saved to charts/
└────────┬────────────────────┘
         ▼
┌──────────────────────────────────┐
│  7. Dashboard-Style Summary      │  Single-page dark-theme summary image
└────────┬─────────────────────────┘
         ▼
┌────────────────────────────────────────────────┐
│  8. Business Insights & Recommendations ×18    │  Printed to console, all data-driven
└────────────────────────────────────────────────┘
```

---

## Project Structure

```
Sales-Data-Analytics/
│
├── Sales Data Analytics.py   ← Main analytics script
├── Sales Dataset.csv         ← Source data (must be in the same folder)
├── requirements.txt          ← Python package dependencies
├── README.md                 ← This file
│
└── charts/                   ← Auto-created when the script runs
    ├── monthly_sales_trend.png
    ├── sales_by_category.png
    ├── profit_by_category.png
    ├── top_subcategories_by_sales.png
    ├── sales_by_state.png
    ├── profit_by_state.png
    ├── sales_vs_profit.png
    ├── sales_profit_distribution.png
    ├── category_sales_contribution.png
    ├── quantity_vs_sales.png
    ├── sales_by_payment_mode.png
    ├── yearly_sales_profit.png
    └── sales_dashboard.png
```

> The `charts/` folder is created automatically. You do not need to create it manually.

---

## Data Cleaning

The dataset arrived in good condition. The following steps were applied:

| Step | Action |
|---|---|
| Date conversion | `Order Date` converted from string to `datetime64` using format `%Y-%m-%d` |
| Derived columns | `Year`, `Month`, `Month Name`, `Quarter`, and `YM Period` extracted from `Order Date` |
| Time-series ordering | `Year-Month` parsed into a `pandas.Period` for correct chronological sorting |
| Whitespace trimming | Leading/trailing spaces stripped from all text columns |
| Duplicate removal | `drop_duplicates()` applied as a best-practice safeguard (zero duplicates found) |

No records were deleted. All 1,194 rows were retained after cleaning.

---

## KPIs

The following Key Performance Indicators are calculated directly from the dataset:

| KPI | Description |
|---|---|
| **Total Sales** | Sum of the `Amount` column across all transactions |
| **Total Profit** | Sum of the `Profit` column across all transactions |
| **Total Unique Orders** | Count of distinct `Order ID` values |
| **Total Transactions** | Total row count (1,194) |
| **Total Quantity Sold** | Sum of the `Quantity` column |
| **Average Order Value** | Mean of per-order summed `Amount` |
| **Average Profit per Transaction** | Mean of `Profit` column |
| **Unique Customers** | Count of distinct `CustomerName` values |
| **Overall Profit Margin** | `(Total Profit / Total Sales) × 100` |

---

## Exploratory Data Analysis

| Analysis | Description |
|---|---|
| Monthly Sales Trend | Sales and profit aggregated by `YM Period` and sorted chronologically |
| Sales & Profit by Category | Grouped totals for Electronics, Furniture, Office Supplies |
| Sales & Profit by Sub-Category | All 12 sub-categories ranked by revenue |
| Top 10 Sub-Categories | Highest-revenue sub-categories |
| Bottom Sub-Categories | Lowest-performing sub-categories |
| Sales & Profit by State | Revenue and profit across all 6 states |
| Sales & Profit by City | City-level aggregation |
| Sales by Payment Mode | Revenue breakdown across UPI, Credit Card, Debit Card, COD, EMI |
| Yearly Summary | Annual totals for Amount, Profit, and Quantity |
| Top 10 Customers | Customers ranked by total spend |
| Profit Margin by Category | Margin percentage computed per category |

---

## Visualizations

13 PNG images are generated and saved to the `charts/` folder:

| # | Filename | Chart Type | What It Shows |
|---|---|---|---|
| 1 | `monthly_sales_trend.png` | Line chart | Sales and profit trend month-by-month (2020–2025) |
| 2 | `sales_by_category.png` | Bar chart | Total sales per category with value labels |
| 3 | `profit_by_category.png` | Bar chart | Total profit per category with value labels |
| 4 | `top_subcategories_by_sales.png` | Horizontal bar chart | Top 10 sub-categories ranked by sales |
| 5 | `sales_by_state.png` | Bar chart | Total sales across all 6 states |
| 6 | `profit_by_state.png` | Bar chart | Total profit across all 6 states |
| 7 | `sales_vs_profit.png` | Scatter plot | Relationship between sales amount and profit, coloured by category |
| 8 | `sales_profit_distribution.png` | Dual histogram | Frequency distribution of sales amount and profit values |
| 9 | `category_sales_contribution.png` | Donut chart | Percentage revenue share of each category |
| 10 | `quantity_vs_sales.png` | Scatter plot | Quantity sold vs sales amount per transaction, coloured by category |
| 11 | `sales_by_payment_mode.png` | Bar chart | Total sales across all 5 payment methods |
| 12 | `yearly_sales_profit.png` | Grouped bar chart | Annual sales and profit side-by-side (2020–2025) |
| 13 | `sales_dashboard.png` | Dashboard image | Full single-page summary (see below) |

Every chart includes a title, labelled axes, value annotations where useful, a legend, and `tight_layout()`.

---

## Python Dashboard-Style Analysis

The script produces a single-page dark-themed dashboard image (`charts/sales_dashboard.png`) built entirely with `matplotlib` using `GridSpec`. No external BI tool is used.

The dashboard contains:

- **8 KPI cards** — one each for Total Sales, Total Profit, Total Orders, Total Quantity, Unique Customers, Profit Margin, Average Order Value, and Average Profit. Each card displays the metric value in large white text on a distinct colour background.
- **Monthly Sales & Profit Trend** — dual-line chart spanning the full date range.
- **Sales by Category** — horizontal bar chart.
- **Sales by State** — vertical bar chart with value labels.
- **Profit Margin % by Category** — bar chart with percentage labels.
- **Top Sub-Categories by Sales** — horizontal bar chart.
- **Sales by Payment Mode** — vertical bar chart.

All values shown in the dashboard are computed from the actual dataset at runtime.

---

## Business Insights

All insights below are generated dynamically by the script from actual computed values. The script prints the specific figures (category names, dollar amounts, percentages) at runtime.

1. **Highest-performing category** — identified by total sales and profit margin.
2. **Lowest-performing category** — identified by total sales.
3. **Top product sub-category** — highest revenue sub-category by aggregated sales.
4. **Lowest sub-category** — weakest performer across all 12 sub-categories.
5. **Strongest sales state** — state with the highest total sales and profit.
6. **Weakest sales state** — state with the lowest total sales.
7. **Dominant payment mode** — payment method accounting for the most revenue.
8. **Best year for sales** — the calendar year with the highest total sales.
9. **Peak sales month** — the individual month-year with the highest single-month sales.
10. **Overall profitability** — overall profit margin across the entire dataset.

---

## Business Recommendations

Eight actionable recommendations are generated by the script based on the computed findings:

1. Invest further in the top-performing category to sustain and grow its revenue lead.
2. Revitalise the lowest-performing category through promotions and bundle deals.
3. Deepen market presence in the strongest-performing state.
4. Investigate and develop the lowest-performing state market.
5. Protect stock levels and marketing focus on the top-selling sub-category.
6. Conduct a cost-benefit review of the lowest-selling sub-category.
7. Leverage strong digital payment adoption through mode-specific incentives.
8. Use peak-year performance strategies as the benchmark for future annual targets.

---

## Installation

### Step 1 — Verify Python is installed

```powershell
python --version
```

Python 3.8 or above is recommended.

### Step 2 — Place the dataset in the project folder

Ensure `Sales Dataset.csv` and `Sales Data Analytics.py` are in the **same folder**.

### Step 3 — Install dependencies

```powershell
python -m pip install -r requirements.txt
```

This installs:

```
pandas>=2.0.0
matplotlib>=3.7.0
seaborn>=0.13.0
```

---

## How to Run

```powershell
python "Sales Data Analytics.py"
```

### Dataset path

The dataset path is controlled by the `DATA_PATH` variable at the top of the script (line 28):

```python
DATA_PATH = "Sales Dataset.csv"
```

If you move the CSV to a different location, update this variable:

```python
DATA_PATH = r"C:\Users\YourName\Documents\Sales Dataset.csv"
```

### Where charts are saved

All charts are automatically saved to a `charts/` subfolder in the same directory as the script. The folder is created automatically if it does not exist.

---

## Expected Output

When the script runs successfully it prints the following sections to the console:

```
======================================================================
   SALES DATA ANALYTICS – FULL PIPELINE
======================================================================

  1. DATA LOADING
  2. DATA QUALITY CHECK
  3. DATA CLEANING
  4. KPI ANALYSIS
  5. EXPLORATORY DATA ANALYSIS
  6. PROFESSIONAL DATA VISUALIZATIONS
     ✔ Saved → charts/monthly_sales_trend.png
     ✔ Saved → charts/sales_by_category.png
     ... (12 charts total)
  7. CHARTS SAVED
  8. PYTHON DASHBOARD-STYLE SUMMARY
     ✔ Saved → charts/sales_dashboard.png
  9. BUSINESS INSIGHTS
 10. BUSINESS RECOMMENDATIONS

  PIPELINE COMPLETE
  Charts folder  : <absolute path to charts/>
  Total charts   : 13
```

---

## Results

The script runs a complete analytics pipeline on 1,194 sales transactions spanning 2020 to 2025 across 3 product categories, 12 sub-categories, 6 US states, and 5 payment modes. It calculates 9 KPIs, performs 11 EDA aggregations, produces 13 chart images, and prints 10 business insights and 8 recommendations — all derived from the actual dataset without any hard-coded values.

---

## Future Scope

The following enhancements are not part of the current implementation but represent natural extensions:

- **Interactive dashboard** — migrate charts to Plotly or Streamlit for interactive filtering.
- **Predictive analytics** — apply time-series forecasting (e.g. ARIMA, Prophet) to project future sales.
- **Customer segmentation** — use clustering (e.g. K-Means) to group customers by purchasing behaviour.
- **Profitability scoring** — rank sub-categories and regions by a combined sales + margin score.
- **Automated reporting** — export the KPI summary and insights to a PDF or Excel report.
- **Database integration** — connect directly to a SQL database instead of a flat CSV file.

---

## Author

| Field | Detail |
|---|---|
| **Name** | [Your Name] |
| **Role** | Data Analytics Student |
| **Project** | Sales Data Analytics |
