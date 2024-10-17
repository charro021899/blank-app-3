import streamlit as st
import pandas as pd

# Create tabs for years and months
years = ["2023", "2024", "2025"]
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# Sidebar to select Year and Month
year_selected = st.sidebar.selectbox("Select Year", years)
month_selected = st.sidebar.selectbox("Select Month", months)

st.title(f"Business Data for {month_selected} {year_selected}")

# Input for daily data: categories
st.subheader("Input Daily Data")

# Create empty lists to store data
dates = []
taxable = []
nontax = []
cc = []
sales_tax = []
fs = []
lottery = []
lotto = []
fuel_sales = []
fuel_gallons = []
rebates = []
atm = []
other_income = []

# Create input for each day of the month
for day in range(1, 32):  # Assuming up to 31 days in a month
    st.write(f"### Day {day}")
    dates.append(f"{day:02d}/{month_selected}/{year_selected}")
    taxable.append(st.number_input(f"Taxable - Day {day}", min_value=0, value=0, step=100, key=f"taxable_{day}"))
    nontax.append(st.number_input(f"Non-tax - Day {day}", min_value=0, value=0, step=100, key=f"nontax_{day}"))
    cc.append(st.number_input(f"CC - Day {day}", min_value=0, value=0, step=100, key=f"cc_{day}"))
    sales_tax.append(st.number_input(f"Sales Tax - Day {day}", min_value=0, value=0, step=100, key=f"sales_tax_{day}"))
    fs.append(st.number_input(f"FS - Day {day}", min_value=0, value=0, step=100, key=f"fs_{day}"))
    lottery.append(st.number_input(f"Lottery - Day {day}", min_value=0, value=0, step=100, key=f"lottery_{day}"))
    lotto.append(st.number_input(f"Lotto - Day {day}", min_value=0, value=0, step=100, key=f"lotto_{day}"))
    fuel_sales.append(st.number_input(f"Fuel Sales - Day {day}", min_value=0, value=0, step=100, key=f"fuel_sales_{day}"))
    fuel_gallons.append(st.number_input(f"Fuel Gallons - Day {day}", min_value=0, value=0, step=10, key=f"fuel_gallons_{day}"))
    rebates.append(st.number_input(f"Rebates - Day {day}", min_value=0, value=0, step=100, key=f"rebates_{day}"))
    atm.append(st.number_input(f"ATM - Day {day}", min_value=0, value=0, step=100, key=f"atm_{day}"))
    other_income.append(st.number_input(f"Other Income - Day {day}", min_value=0, value=0, step=100, key=f"other_income_{day}"))

# Create a dataframe for income data
income_data = {
    "Date": dates,
    "Taxable": taxable,
    "Non-tax": nontax,
    "CC": cc,
    "Sales Tax": sales_tax,
    "FS": fs,
    "Lottery": lottery,
    "Lotto": lotto,
    "Fuel Sales": fuel_sales,
    "Fuel Gallons": fuel_gallons,
    "Rebates": rebates,
    "ATM": atm,
    "Other Income": other_income
}
df_income = pd.DataFrame(income_data)
df_income.loc['Total'] = df_income.sum(numeric_only=True)

st.subheader(f"Income Data for {month_selected} {year_selected}")
st.dataframe(df_income)

# Expense Input Section
st.subheader("Input Monthly Expenses")

expense_categories = [
    "BANK CHARGES", "CC FEES", "CONTRACT LABOR", "OFFICE SUPPLY", "INSURANCE PREMIUMS", 
    "INTEREST", "LEGAL FEE", "MAINTENANCE", "WASTE MANAGEMENT", "RENT",
    "SECURITY", "SUPPLIES", "TAXES & LICENSE", "TELEPHONES", "UTILITIES",
    "CC CHARGE", "STORE EXPENSES", "GASOLINE EXPENSES", "PAY ROLL", "PAY ROLL TAXES",
    "Gasoline Purchase", "INVENTORY STOCK", "INVENTORY CASH", "INVENTORY ACCOUNT 2"
]

expense_amounts = []

# Input for each expense
for category in expense_categories:
    expense_amounts.append(st.number_input(f"{category}", min_value=0, value=0, step=100))

# Create a dataframe for expenses
expense_data = {"Expense": expense_categories, "Amount": expense_amounts}
df_expenses = pd.DataFrame(expense_data)
df_expenses.loc['Total'] = df_expenses["Amount"].sum()

st.subheader(f"Expense Data for {month_selected} {year_selected}")
st.dataframe(df_expenses)

# Financial Summary
st.subheader("Financial Summary")
total_income = df_income.loc['Total', "Taxable":"Other Income"].sum()
total_expenses = df_expenses.loc['Total', "Amount"]

st.write(f"Total Income: ${total_income}")
st.write(f"Total Expenses: ${total_expenses}")
st.write(f"Net Profit: ${total_income - total_expenses}")

# Option to download the data
st.download_button(label="Download Income Data as CSV", data=df_income.to_csv(), mime="text/csv")
st.download_button(label="Download Expense Data as CSV", data=df_expenses.to_csv(), mime="text/csv")
