import sqlite3
import pandas as pd
import os

# =========================================================
# 1. PROJECT PATHS
# =========================================================

BASE_DIR = r"C:\Users\Zugne\OneDrive\Desktop\Project1"

DATA_FILE = os.path.join(
    BASE_DIR,
    "data",
    "Sales Dataset.csv"
)

SQL_DIR = os.path.join(
    BASE_DIR,
    "SQL"
)

DB_FILE = os.path.join(
    SQL_DIR,
    "sales.db"
)

OUTPUT_DIR = os.path.join(
    BASE_DIR,
    "output"
)

os.makedirs(SQL_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================================================
# 2. LOAD DATASET
# =========================================================

print("=" * 60)
print("SALES DATA ANALYSIS - SQL")
print("=" * 60)

print("\nLoading dataset...")

df = pd.read_csv(DATA_FILE)

print("Dataset loaded successfully!")
print("Rows    :", df.shape[0])
print("Columns :", df.shape[1])

print("\nColumns:")
print(list(df.columns))


# =========================================================
# 3. CONNECT TO SQLITE DATABASE
# =========================================================

print("\nCreating SQLite database...")

conn = sqlite3.connect(DB_FILE)

df.to_sql(
    "sales",
    conn,
    if_exists="replace",
    index=False
)

print("Database created successfully!")
print("Database location:")
print(DB_FILE)


# =========================================================
# 4. TOTAL RECORDS
# =========================================================

query = """
SELECT COUNT(*) AS Total_Records
FROM sales;
"""

result = pd.read_sql_query(query, conn)

print("\n" + "=" * 60)
print("1. TOTAL RECORDS")
print("=" * 60)
print(result.to_string(index=False))

result.to_csv(
    os.path.join(OUTPUT_DIR, "sql_total_records.csv"),
    index=False
)


# =========================================================
# 5. TOTAL SALES
# =========================================================

query = """
SELECT
    ROUND(SUM(Amount), 2) AS Total_Sales
FROM sales;
"""

result = pd.read_sql_query(query, conn)

print("\n" + "=" * 60)
print("2. TOTAL SALES")
print("=" * 60)
print(result.to_string(index=False))

result.to_csv(
    os.path.join(OUTPUT_DIR, "sql_total_sales.csv"),
    index=False
)


# =========================================================
# 6. TOTAL PROFIT
# =========================================================

query = """
SELECT
    ROUND(SUM(Profit), 2) AS Total_Profit
FROM sales;
"""

result = pd.read_sql_query(query, conn)

print("\n" + "=" * 60)
print("3. TOTAL PROFIT")
print("=" * 60)
print(result.to_string(index=False))

result.to_csv(
    os.path.join(OUTPUT_DIR, "sql_total_profit.csv"),
    index=False
)


# =========================================================
# 7. TOTAL QUANTITY
# =========================================================

query = """
SELECT
    SUM(Quantity) AS Total_Quantity
FROM sales;
"""

result = pd.read_sql_query(query, conn)

print("\n" + "=" * 60)
print("4. TOTAL QUANTITY")
print("=" * 60)
print(result.to_string(index=False))

result.to_csv(
    os.path.join(OUTPUT_DIR, "sql_total_quantity.csv"),
    index=False
)


# =========================================================
# 8. CATEGORY PERFORMANCE
# =========================================================

query = """
SELECT
    Category,
    ROUND(SUM(Amount), 2) AS Sales,
    ROUND(SUM(Profit), 2) AS Profit,
    SUM(Quantity) AS Quantity
FROM sales
GROUP BY Category
ORDER BY Sales DESC;
"""

result = pd.read_sql_query(query, conn)

print("\n" + "=" * 60)
print("5. CATEGORY PERFORMANCE")
print("=" * 60)
print(result.to_string(index=False))

result.to_csv(
    os.path.join(OUTPUT_DIR, "sql_category_performance.csv"),
    index=False
)


# =========================================================
# 9. SUB-CATEGORY PERFORMANCE
# =========================================================

query = """
SELECT
    "Sub-Category" AS Sub_Category,
    ROUND(SUM(Amount), 2) AS Sales,
    ROUND(SUM(Profit), 2) AS Profit,
    SUM(Quantity) AS Quantity
FROM sales
GROUP BY "Sub-Category"
ORDER BY Sales DESC;
"""

result = pd.read_sql_query(query, conn)

print("\n" + "=" * 60)
print("6. SUB-CATEGORY PERFORMANCE")
print("=" * 60)
print(result.to_string(index=False))

result.to_csv(
    os.path.join(OUTPUT_DIR, "sql_subcategory_performance.csv"),
    index=False
)


# =========================================================
# 10. TOP 10 SUB-CATEGORIES BY SALES
# =========================================================

query = """
SELECT
    "Sub-Category" AS Sub_Category,
    ROUND(SUM(Amount), 2) AS Sales
FROM sales
GROUP BY "Sub-Category"
ORDER BY Sales DESC
LIMIT 10;
"""

result = pd.read_sql_query(query, conn)

print("\n" + "=" * 60)
print("7. TOP 10 SUB-CATEGORIES BY SALES")
print("=" * 60)
print(result.to_string(index=False))

result.to_csv(
    os.path.join(OUTPUT_DIR, "sql_top10_subcategories_sales.csv"),
    index=False
)


# =========================================================
# 11. TOP 10 PROFITABLE SUB-CATEGORIES
# =========================================================

query = """
SELECT
    "Sub-Category" AS Sub_Category,
    ROUND(SUM(Profit), 2) AS Profit
FROM sales
GROUP BY "Sub-Category"
ORDER BY Profit DESC
LIMIT 10;
"""

result = pd.read_sql_query(query, conn)

print("\n" + "=" * 60)
print("8. TOP 10 PROFITABLE SUB-CATEGORIES")
print("=" * 60)
print(result.to_string(index=False))

result.to_csv(
    os.path.join(OUTPUT_DIR, "sql_top10_profitable_subcategories.csv"),
    index=False
)


# =========================================================
# 12. LOSS-MAKING SUB-CATEGORIES
# =========================================================

query = """
SELECT
    "Sub-Category" AS Sub_Category,
    ROUND(SUM(Profit), 2) AS Profit
FROM sales
GROUP BY "Sub-Category"
HAVING SUM(Profit) < 0
ORDER BY Profit ASC;
"""

result = pd.read_sql_query(query, conn)

print("\n" + "=" * 60)
print("9. LOSS-MAKING SUB-CATEGORIES")
print("=" * 60)

if len(result) > 0:
    print(result.to_string(index=False))
else:
    print("No loss-making sub-categories found.")

result.to_csv(
    os.path.join(OUTPUT_DIR, "sql_loss_making_subcategories.csv"),
    index=False
)


# =========================================================
# 13. PAYMENT MODE ANALYSIS
# =========================================================

query = """
SELECT
    PaymentMode,
    ROUND(SUM(Amount), 2) AS Sales,
    SUM(Quantity) AS Quantity
FROM sales
GROUP BY PaymentMode
ORDER BY Sales DESC;
"""

result = pd.read_sql_query(query, conn)

print("\n" + "=" * 60)
print("10. PAYMENT MODE ANALYSIS")
print("=" * 60)
print(result.to_string(index=False))

result.to_csv(
    os.path.join(OUTPUT_DIR, "sql_payment_mode_analysis.csv"),
    index=False
)


# =========================================================
# 14. TOP 10 STATES
# =========================================================

query = """
SELECT
    State,
    ROUND(SUM(Amount), 2) AS Sales,
    ROUND(SUM(Profit), 2) AS Profit
FROM sales
GROUP BY State
ORDER BY Sales DESC
LIMIT 10;
"""

result = pd.read_sql_query(query, conn)

print("\n" + "=" * 60)
print("11. TOP 10 STATES BY SALES")
print("=" * 60)
print(result.to_string(index=False))

result.to_csv(
    os.path.join(OUTPUT_DIR, "sql_top10_states.csv"),
    index=False
)


# =========================================================
# 15. TOP 10 CITIES
# =========================================================

query = """
SELECT
    City,
    ROUND(SUM(Amount), 2) AS Sales,
    ROUND(SUM(Profit), 2) AS Profit
FROM sales
GROUP BY City
ORDER BY Sales DESC
LIMIT 10;
"""

result = pd.read_sql_query(query, conn)

print("\n" + "=" * 60)
print("12. TOP 10 CITIES BY SALES")
print("=" * 60)
print(result.to_string(index=False))

result.to_csv(
    os.path.join(OUTPUT_DIR, "sql_top10_cities.csv"),
    index=False
)


# =========================================================
# 16. MONTHLY SALES
# =========================================================

query = """
SELECT
    "Year-Month" AS Year_Month,
    ROUND(SUM(Amount), 2) AS Sales,
    ROUND(SUM(Profit), 2) AS Profit,
    SUM(Quantity) AS Quantity
FROM sales
GROUP BY "Year-Month"
ORDER BY "Year-Month";
"""

result = pd.read_sql_query(query, conn)

print("\n" + "=" * 60)
print("13. MONTHLY SALES PERFORMANCE")
print("=" * 60)
print(result.to_string(index=False))

result.to_csv(
    os.path.join(OUTPUT_DIR, "sql_monthly_sales.csv"),
    index=False
)


# =========================================================
# 17. YEARLY SALES
# =========================================================

query = """
SELECT
    substr("Year-Month", 1, 4) AS Year,
    ROUND(SUM(Amount), 2) AS Sales,
    ROUND(SUM(Profit), 2) AS Profit
FROM sales
GROUP BY substr("Year-Month", 1, 4)
ORDER BY Year;
"""

result = pd.read_sql_query(query, conn)

print("\n" + "=" * 60)
print("14. YEARLY SALES PERFORMANCE")
print("=" * 60)
print(result.to_string(index=False))

result.to_csv(
    os.path.join(OUTPUT_DIR, "sql_yearly_sales.csv"),
    index=False
)


# =========================================================
# 18. CATEGORY WITH HIGHEST SALES
# =========================================================

query = """
SELECT
    Category,
    ROUND(SUM(Amount), 2) AS Sales
FROM sales
GROUP BY Category
ORDER BY Sales DESC
LIMIT 1;
"""

result = pd.read_sql_query(query, conn)

print("\n" + "=" * 60)
print("15. HIGHEST SALES CATEGORY")
print("=" * 60)
print(result.to_string(index=False))


# =========================================================
# 19. CATEGORY WITH HIGHEST PROFIT
# =========================================================

query = """
SELECT
    Category,
    ROUND(SUM(Profit), 2) AS Profit
FROM sales
GROUP BY Category
ORDER BY Profit DESC
LIMIT 1;
"""

result = pd.read_sql_query(query, conn)

print("\n" + "=" * 60)
print("16. HIGHEST PROFIT CATEGORY")
print("=" * 60)
print(result.to_string(index=False))


# =========================================================
# 20. TOP 10 CUSTOMERS BY SALES
# =========================================================

query = """
SELECT
    CustomerName,
    ROUND(SUM(Amount), 2) AS Sales
FROM sales
GROUP BY CustomerName
ORDER BY Sales DESC
LIMIT 10;
"""

result = pd.read_sql_query(query, conn)

print("\n" + "=" * 60)
print("17. TOP 10 CUSTOMERS BY SALES")
print("=" * 60)
print(result.to_string(index=False))

result.to_csv(
    os.path.join(OUTPUT_DIR, "sql_top10_customers.csv"),
    index=False
)


# =========================================================
# 21. AVERAGE ORDER VALUE
# =========================================================

query = """
SELECT
    ROUND(AVG(Amount), 2) AS Average_Order_Value
FROM sales;
"""

result = pd.read_sql_query(query, conn)

print("\n" + "=" * 60)
print("18. AVERAGE ORDER VALUE")
print("=" * 60)
print(result.to_string(index=False))


# =========================================================
# 22. SALES AND PROFIT SUMMARY
# =========================================================

query = """
SELECT
    ROUND(SUM(Amount), 2) AS Total_Sales,
    ROUND(SUM(Profit), 2) AS Total_Profit,
    SUM(Quantity) AS Total_Quantity,
    COUNT(*) AS Total_Orders,
    ROUND(AVG(Amount), 2) AS Average_Order_Value
FROM sales;
"""

result = pd.read_sql_query(query, conn)

print("\n" + "=" * 60)
print("19. OVERALL BUSINESS SUMMARY")
print("=" * 60)
print(result.to_string(index=False))

result.to_csv(
    os.path.join(OUTPUT_DIR, "sql_business_summary.csv"),
    index=False
)


# =========================================================
# 23. CLOSE DATABASE
# =========================================================

conn.close()

print("\n" + "=" * 60)
print("SQL ANALYSIS COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nDatabase created:")
print(DB_FILE)

print("\nSQL result files saved in:")
print(OUTPUT_DIR)

print("\nNext Step:")
print("Power BI Dashboard")