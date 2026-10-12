import pandas as pd
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('Sales Dataset.csv')
df['Order Date'] = pd.to_datetime(df['Order Date'], format='%Y-%m-%d')
df['Year'] = df['Order Date'].dt.year
df['YM Period'] = pd.to_datetime(df['Year-Month'], format='%Y-%m').dt.to_period('M')

# KPIs
total_sales = df['Amount'].sum()
total_profit = df['Profit'].sum()
total_orders = df['Order ID'].nunique()
total_tx = len(df)
total_qty = df['Quantity'].sum()
avg_ov = df.groupby('Order ID')['Amount'].sum().mean()
avg_profit = df['Profit'].mean()
num_cust = df['CustomerName'].nunique()
margin = (total_profit / total_sales) * 100

print(f'Total Sales: {total_sales}')
print(f'Total Profit: {total_profit}')
print(f'Total Orders: {total_orders}')
print(f'Total Transactions: {total_tx}')
print(f'Total Quantity: {total_qty}')
print(f'Avg Order Value: {avg_ov:.2f}')
print(f'Avg Profit: {avg_profit:.2f}')
print(f'Num Customers: {num_cust}')
print(f'Profit Margin: {margin:.2f}')

# Category
cat = df.groupby('Category')[['Amount','Profit']].sum().sort_values('Amount', ascending=False).reset_index()
cat['Margin'] = (cat['Profit']/cat['Amount']*100).round(1)
print('\n--- CATEGORY ---')
for _, r in cat.iterrows():
    print(f"{r['Category']}: Sales={r['Amount']}, Profit={r['Profit']}, Margin={r['Margin']}%")

# Sub-category
sub = df.groupby('Sub-Category')[['Amount','Profit']].sum().sort_values('Amount', ascending=False).reset_index()
print('\n--- SUB-CATEGORY ALL ---')
for _, r in sub.iterrows():
    print(f"{r['Sub-Category']}: Sales={r['Amount']}, Profit={r['Profit']}")

# State
st = df.groupby('State')[['Amount','Profit']].sum().sort_values('Amount', ascending=False).reset_index()
print('\n--- STATE ---')
for _, r in st.iterrows():
    print(f"{r['State']}: Sales={r['Amount']}, Profit={r['Profit']}")

# Payment
pay = df.groupby('PaymentMode')[['Amount','Profit']].sum().sort_values('Amount', ascending=False).reset_index()
print('\n--- PAYMENT ---')
for _, r in pay.iterrows():
    print(f"{r['PaymentMode']}: Sales={r['Amount']}, Profit={r['Profit']}")

# Year
yr = df.groupby('Year')[['Amount','Profit','Quantity']].sum().reset_index()
print('\n--- YEAR ---')
for _, r in yr.iterrows():
    print(f"{int(r['Year'])}: Sales={r['Amount']}, Profit={r['Profit']}, Qty={int(r['Quantity'])}")

# Peak month
monthly = df.groupby('YM Period')[['Amount','Profit']].sum().sort_index().reset_index()
monthly['YM Label'] = monthly['YM Period'].astype(str)
peak = monthly.loc[monthly['Amount'].idxmax()]
print(f"\nPeak Month: {peak['YM Label']} Sales={peak['Amount']}")

# Top 5 customers
tc = df.groupby('CustomerName')['Amount'].sum().sort_values(ascending=False).head(5).reset_index()
print('\n--- TOP 5 CUSTOMERS ---')
for _, r in tc.iterrows():
    print(f"{r['CustomerName']}: {r['Amount']}")

print(f'\nUnique Cities: {df["City"].nunique()}')
print(f'Unique States: {df["State"].nunique()}')
print(f'Date range: {df["Order Date"].min().date()} to {df["Order Date"].max().date()}')

# Amount & Profit ranges
print(f'\nAmount min={df["Amount"].min()}, max={df["Amount"].max()}, mean={df["Amount"].mean():.0f}')
print(f'Profit min={df["Profit"].min()}, max={df["Profit"].max()}, mean={df["Profit"].mean():.0f}')
print(f'Quantity min={df["Quantity"].min()}, max={df["Quantity"].max()}, mean={df["Quantity"].mean():.1f}')
