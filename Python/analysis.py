import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# 1. PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "Data")
CHART_DIR = os.path.join(BASE_DIR, "charts")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(CHART_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

FILE_PATH = os.path.join(DATA_DIR, "Sales Dataset.csv")


# ============================================================
# 2. LOAD DATASET
# ============================================================

df = pd.read_csv(FILE_PATH)

print("=" * 70)
print("              SALES DATA ANALYSIS PROJECT")
print("=" * 70)

print("\n===== DATASET LOADED =====")
print("Rows    :", df.shape[0])
print("Columns :", df.shape[1])


# ============================================================
# 3. BASIC DATA EXPLORATION
# ============================================================

print("\n===== FIRST 5 ROWS =====")
print(df.head())

print("\n===== COLUMN NAMES =====")
print(df.columns.tolist())

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\n===== DATASET INFO =====")
print(df.info())

print("\n===== STATISTICAL SUMMARY =====")
print(df.describe(include="all"))


# ============================================================
# 4. DATA CLEANING
# ============================================================

print("\n" + "=" * 70)
print("                    DATA CLEANING")
print("=" * 70)

# Remove duplicate rows
duplicates = df.duplicated().sum()
print("\nDuplicate rows:", duplicates)

if duplicates > 0:
    df = df.drop_duplicates()
    print("Duplicates removed.")

# Missing values
print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

# Standardize column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

print("\n===== CLEANED COLUMN NAMES =====")
print(df.columns.tolist())


# ============================================================
# 5. DATE CONVERSION
# ============================================================

df["order_date"] = pd.to_datetime(
    df["order_date"],
    errors="coerce"
)

print("\nInvalid dates:", df["order_date"].isna().sum())

# Create date-related columns
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
df["month_name"] = df["order_date"].dt.strftime("%B")

df["year_month"] = df["order_date"].dt.to_period("M").astype(str)


# ============================================================
# 6. NUMERIC DATA VALIDATION
# ============================================================

numeric_columns = ["amount", "profit", "quantity"]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

print("\n===== NEGATIVE VALUES CHECK =====")

print("Negative Amount   :", (df["amount"] < 0).sum())
print("Negative Quantity :", (df["quantity"] < 0).sum())
print("Negative Profit   :", (df["profit"] < 0).sum())


# ============================================================
# 7. KPI CALCULATIONS
# ============================================================

total_sales = df["amount"].sum()
total_profit = df["profit"].sum()
total_quantity = df["quantity"].sum()

total_orders = df["order_id"].nunique()
total_customers = df["customername"].nunique()

average_order_value = total_sales / total_orders

profit_margin = (
    total_profit / total_sales
) * 100 if total_sales != 0 else 0


print("\n" + "=" * 70)
print("                       KEY KPIs")
print("=" * 70)

print(f"\nTotal Sales          : {total_sales:,.2f}")
print(f"Total Profit         : {total_profit:,.2f}")
print(f"Total Quantity       : {total_quantity:,.0f}")
print(f"Total Orders         : {total_orders:,}")
print(f"Total Customers      : {total_customers:,}")
print(f"Average Order Value  : {average_order_value:,.2f}")
print(f"Profit Margin        : {profit_margin:.2f}%")


# ============================================================
# 8. CATEGORY ANALYSIS
# ============================================================

print("\n===== CATEGORY ANALYSIS =====")

category_analysis = df.groupby("category").agg(
    Sales=("amount", "sum"),
    Profit=("profit", "sum"),
    Quantity=("quantity", "sum"),
    Orders=("order_id", "nunique")
).sort_values("Sales", ascending=False)

print(category_analysis)


# ============================================================
# 9. SUB-CATEGORY ANALYSIS
# ============================================================

print("\n===== TOP SUB-CATEGORIES BY SALES =====")

subcategory_analysis = df.groupby("sub_category").agg(
    Sales=("amount", "sum"),
    Profit=("profit", "sum"),
    Quantity=("quantity", "sum")
).sort_values("Sales", ascending=False)

print(subcategory_analysis.head(10))


# ============================================================
# 10. PAYMENT MODE ANALYSIS
# ============================================================

print("\n===== PAYMENT MODE ANALYSIS =====")

payment_analysis = df.groupby("paymentmode").agg(
    Sales=("amount", "sum"),
    Profit=("profit", "sum"),
    Orders=("order_id", "nunique")
).sort_values("Sales", ascending=False)

print(payment_analysis)


# ============================================================
# 11. STATE ANALYSIS
# ============================================================

print("\n===== TOP 10 STATES =====")

state_analysis = df.groupby("state").agg(
    Sales=("amount", "sum"),
    Profit=("profit", "sum"),
    Orders=("order_id", "nunique")
).sort_values("Sales", ascending=False)

print(state_analysis.head(10))


# ============================================================
# 12. CITY ANALYSIS
# ============================================================

print("\n===== TOP 10 CITIES =====")

city_analysis = df.groupby("city").agg(
    Sales=("amount", "sum"),
    Profit=("profit", "sum"),
    Orders=("order_id", "nunique")
).sort_values("Sales", ascending=False)

print(city_analysis.head(10))


# ============================================================
# 13. CUSTOMER ANALYSIS
# ============================================================

print("\n===== TOP 10 CUSTOMERS BY SALES =====")

customer_analysis = df.groupby("customername").agg(
    Sales=("amount", "sum"),
    Profit=("profit", "sum"),
    Orders=("order_id", "nunique")
).sort_values("Sales", ascending=False)

print(customer_analysis.head(10))


# ============================================================
# 14. MONTHLY SALES ANALYSIS
# ============================================================

monthly_sales = df.groupby("year_month").agg(
    Sales=("amount", "sum"),
    Profit=("profit", "sum"),
    Quantity=("quantity", "sum")
).reset_index()

print("\n===== MONTHLY SALES =====")
print(monthly_sales)


# ============================================================
# 15. YEARLY SALES ANALYSIS
# ============================================================

yearly_sales = df.groupby("year").agg(
    Sales=("amount", "sum"),
    Profit=("profit", "sum"),
    Quantity=("quantity", "sum")
)

print("\n===== YEARLY SALES =====")
print(yearly_sales)


# ============================================================
# 16. BEST / WORST PERFORMERS
# ============================================================

best_month = monthly_sales.loc[
    monthly_sales["Sales"].idxmax()
]

worst_month = monthly_sales.loc[
    monthly_sales["Sales"].idxmin()
]

best_category = category_analysis["Sales"].idxmax()
worst_category = category_analysis["Sales"].idxmin()

best_subcategory = subcategory_analysis["Sales"].idxmax()
worst_subcategory = subcategory_analysis["Sales"].idxmin()

best_state = state_analysis["Sales"].idxmax()

print("\n" + "=" * 70)
print("                  BUSINESS INSIGHTS")
print("=" * 70)

print("\nBest Sales Month:")
print(best_month)

print("\nLowest Sales Month:")
print(worst_month)

print("\nBest Category:", best_category)
print("Lowest Category:", worst_category)

print("\nBest Sub-Category:", best_subcategory)
print("Lowest Sub-Category:", worst_subcategory)

print("\nTop State:", best_state)


# ============================================================
# 17. PROFIT / LOSS ANALYSIS
# ============================================================

loss_records = df[df["profit"] < 0]

print("\n===== PROFIT / LOSS ANALYSIS =====")

print("Loss-making records:", len(loss_records))

print("\nTotal Loss:",
      loss_records["profit"].sum())

print("\nTop 10 Loss-Making Records:")

print(
    loss_records[
        ["order_id", "amount", "profit", "category", "sub_category"]
    ]
    .sort_values("profit")
    .head(10)
)


# ============================================================
# 18. OUTLIER ANALYSIS
# ============================================================

Q1 = df["amount"].quantile(0.25)
Q3 = df["amount"].quantile(0.75)

IQR = Q3 - Q1

lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

outliers = df[
    (df["amount"] < lower_limit) |
    (df["amount"] > upper_limit)
]

print("\n===== OUTLIER ANALYSIS =====")

print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)
print("Lower Limit:", lower_limit)
print("Upper Limit:", upper_limit)
print("Outlier Records:", len(outliers))


# ============================================================
# 19. CHART 1 - MONTHLY SALES TREND
# ============================================================

plt.figure(figsize=(12, 6))

plt.plot(
    monthly_sales["year_month"],
    monthly_sales["Sales"],
    marker="o"
)

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "01_monthly_sales_trend.png")
)

plt.close()


# ============================================================
# 20. CHART 2 - YEARLY SALES
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    yearly_sales.index.astype(str),
    yearly_sales["Sales"]
)

plt.title("Yearly Sales")
plt.xlabel("Year")
plt.ylabel("Sales")

plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "02_yearly_sales.png")
)

plt.close()


# ============================================================
# 21. CHART 3 - CATEGORY SALES
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    category_analysis.index,
    category_analysis["Sales"]
)

plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")

plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "03_category_sales.png")
)

plt.close()


# ============================================================
# 22. CHART 4 - CATEGORY PROFIT
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    category_analysis.index,
    category_analysis["Profit"]
)

plt.title("Profit by Category")
plt.xlabel("Category")
plt.ylabel("Profit")

plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "04_category_profit.png")
)

plt.close()


# ============================================================
# 23. CHART 5 - TOP 10 SUB-CATEGORIES
# ============================================================

top_subcategories = subcategory_analysis.head(10)

plt.figure(figsize=(10, 6))

plt.barh(
    top_subcategories.index[::-1],
    top_subcategories["Sales"][::-1]
)

plt.title("Top 10 Sub-Categories by Sales")
plt.xlabel("Sales")
plt.ylabel("Sub-Category")

plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "05_top_subcategories.png")
)

plt.close()


# ============================================================
# 24. CHART 6 - PAYMENT MODE
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    payment_analysis.index,
    payment_analysis["Sales"]
)

plt.title("Sales by Payment Mode")
plt.xlabel("Payment Mode")
plt.ylabel("Sales")

plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "06_payment_mode_sales.png")
)

plt.close()


# ============================================================
# 25. CHART 7 - TOP 10 STATES
# ============================================================

top_states = state_analysis.head(10)

plt.figure(figsize=(10, 6))

plt.barh(
    top_states.index[::-1],
    top_states["Sales"][::-1]
)

plt.title("Top 10 States by Sales")
plt.xlabel("Sales")
plt.ylabel("State")

plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "07_top_states.png")
)

plt.close()


# ============================================================
# 26. CHART 8 - TOP 10 CITIES
# ============================================================

top_cities = city_analysis.head(10)

plt.figure(figsize=(10, 6))

plt.barh(
    top_cities.index[::-1],
    top_cities["Sales"][::-1]
)

plt.title("Top 10 Cities by Sales")
plt.xlabel("Sales")
plt.ylabel("City")

plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "08_top_cities.png")
)

plt.close()


# ============================================================
# 27. CHART 9 - SALES VS PROFIT
# ============================================================

plt.figure(figsize=(8, 6))

plt.scatter(
    df["amount"],
    df["profit"],
    alpha=0.6
)

plt.title("Sales vs Profit")
plt.xlabel("Sales Amount")
plt.ylabel("Profit")

plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "09_sales_vs_profit.png")
)

plt.close()


# ============================================================
# 28. CHART 10 - QUANTITY BY CATEGORY
# ============================================================

plt.figure(figsize=(8, 5))

plt.bar(
    category_analysis.index,
    category_analysis["Quantity"]
)

plt.title("Quantity Sold by Category")
plt.xlabel("Category")
plt.ylabel("Quantity")

plt.xticks(rotation=30)
plt.tight_layout()

plt.savefig(
    os.path.join(CHART_DIR, "10_quantity_by_category.png")
)

plt.close()


# ============================================================
# 29. SAVE CLEANED DATA
# ============================================================

cleaned_file = os.path.join(
    OUTPUT_DIR,
    "sales_cleaned.csv"
)

df.to_csv(
    cleaned_file,
    index=False
)


# ============================================================
# 30. SAVE ANALYSIS FILES
# ============================================================

category_analysis.to_csv(
    os.path.join(OUTPUT_DIR, "category_analysis.csv")
)

subcategory_analysis.to_csv(
    os.path.join(OUTPUT_DIR, "subcategory_analysis.csv")
)

payment_analysis.to_csv(
    os.path.join(OUTPUT_DIR, "payment_analysis.csv")
)

state_analysis.to_csv(
    os.path.join(OUTPUT_DIR, "state_analysis.csv")
)

city_analysis.to_csv(
    os.path.join(OUTPUT_DIR, "city_analysis.csv")
)

customer_analysis.to_csv(
    os.path.join(OUTPUT_DIR, "customer_analysis.csv")
)

monthly_sales.to_csv(
    os.path.join(OUTPUT_DIR, "monthly_sales.csv"),
    index=False
)

yearly_sales.to_csv(
    os.path.join(OUTPUT_DIR, "yearly_sales.csv")
)


# ============================================================
# 31. KPI FILE
# ============================================================

kpi_data = pd.DataFrame({
    "KPI": [
        "Total Sales",
        "Total Profit",
        "Total Quantity",
        "Total Orders",
        "Total Customers",
        "Average Order Value",
        "Profit Margin"
    ],
    "Value": [
        total_sales,
        total_profit,
        total_quantity,
        total_orders,
        total_customers,
        average_order_value,
        profit_margin
    ]
})

kpi_data.to_csv(
    os.path.join(OUTPUT_DIR, "kpi_summary.csv"),
    index=False
)


# ============================================================
# 32. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 70)
print("                 ANALYSIS COMPLETED")
print("=" * 70)

print("\nCharts saved in:")
print(CHART_DIR)

print("\nAnalysis files saved in:")
print(OUTPUT_DIR)

print("\nCreated 10 charts successfully.")

print("\nProject structure now contains:")
print("1. Python Data Analysis")
print("2. Data Cleaning")
print("3. KPI Analysis")
print("4. Business Analysis")
print("5. 10 Visualizations")
print("6. CSV Output Files")

print("\nNext Step: SQL Analysis + Power BI Dashboard")

print("=" * 70)