import streamlit as st
import pandas as pd

# Initialize session state for storing data
if 'data' not in st.session_state:
    st.session_state['data'] = {}
    
# Define years and months
years = [2023, 2024, 2025]
months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Expense categories
expense_categories = [
    "BANK CHARGES", "CC FEES", "CONTRACT LABOR", "OFFICE SUPPLY", "INSURANCE PREMIUMS", 
    "INTEREST", "LEGAL FEE", "MAINTENANCE", "WASTE MANAGEMENT", "RENT",
    "SECURITY", "SUPPLIES", "TAXES & LICENSE", "TELEPHONES", "UTILITIES",
    "CC CHARGE", "STORE EXPENSES", "GASOLINE EXPENSES", "PAY ROLL", "PAY ROLL TAXES",
    "Gasoline Purchase", "INVENTORY STOCK", "INVENTORY CASH", "INVENTORY ACCOUNT 2"
]

# Sidebar for selecting year and month
st.sidebar.header("Select Year and Month")
year_selected = st.sidebar.selectbox("Year", years)
month_selected = st.sidebar.selectbox("Month", months)

# Initialize data structure for selected year and month
if year_selected not in st.session_state['data']:
    st.session_state['data'][year_selected] = {}
if month_selected not in st.session_state['data'][year_selected]:
    # Initialize income data
    st.session_state['data'][year_selected][month_selected] = {
        "Income": pd.DataFrame({
            "Date": [f"{month_selected[:3]} {day}" for day in range(1, 32)],
            "Taxable": [0]*31,
            "Non-tax": [0]*31,
            "CC": [0]*31,
            "Sales Tax": [0]*31,
            "FS": [0]*31,
            "Lottery": [0]*31,
            "Lotto": [0]*31,
            "Fuel Sales": [0]*31,
            "Fuel Gallons": [0]*31,
            "Rebates": [0]*31,
            "ATM": [0]*31,
            "Other Income": [0]*31
        }),
        "Expenses": pd.DataFrame({
            "Expense": expense_categories,
            "Amount": [0]*len(expense_categories)
        })
    }

# Function to calculate totals
def calculate_totals(df_income, df_expenses):
    income_totals = df_income.sum(numeric_only=True)
    expenses_totals = df_expenses["Amount"].sum()
    return income_totals, expenses_totals

# Tabs for different months
tab = st.tabs(["Income", "Expenses", "Summary", "Yearly Summary"])

with tab[0]:
    st.header(f"Income Data for {month_selected} {year_selected}")
    df_income = st.session_state['data'][year_selected][month_selected]["Income"]
    
    # Input income data
    for idx, row in df_income.iterrows():
        with st.expander(f"Day {idx + 1} - {row['Date']}"):
            df_income.at[idx, "Taxable"] = st.number_input(
                f"Taxable - Day {idx + 1}",
                min_value=0,
                value=row["Taxable"],
                step=100,
                key=f"taxable_{year_selected}_{month_selected}_{idx}"
            )
            df_income.at[idx, "Non-tax"] = st.number_input(
                f"Non-tax - Day {idx + 1}",
                min_value=0,
                value=row["Non-tax"],
                step=100,
                key=f"nontax_{year_selected}_{month_selected}_{idx}"
            )
            df_income.at[idx, "CC"] = st.number_input(
                f"CC - Day {idx + 1}",
                min_value=0,
                value=row["CC"],
                step=100,
                key=f"cc_{year_selected}_{month_selected}_{idx}"
            )
            df_income.at[idx, "Sales Tax"] = st.number_input(
                f"Sales Tax - Day {idx + 1}",
                min_value=0,
                value=row["Sales Tax"],
                step=100,
                key=f"sales_tax_{year_selected}_{month_selected}_{idx}"
            )
            df_income.at[idx, "FS"] = st.number_input(
                f"FS - Day {idx + 1}",
                min_value=0,
                value=row["FS"],
                step=100,
                key=f"fs_{year_selected}_{month_selected}_{idx}"
            )
            df_income.at[idx, "Lottery"] = st.number_input(
                f"Lottery - Day {idx + 1}",
                min_value=0,
                value=row["Lottery"],
                step=100,
                key=f"lottery_{year_selected}_{month_selected}_{idx}"
            )
            df_income.at[idx, "Lotto"] = st.number_input(
                f"Lotto - Day {idx + 1}",
                min_value=0,
                value=row["Lotto"],
                step=100,
                key=f"lotto_{year_selected}_{month_selected}_{idx}"
            )
            df_income.at[idx, "Fuel Sales"] = st.number_input(
                f"Fuel Sales - Day {idx + 1}",
                min_value=0,
                value=row["Fuel Sales"],
                step=100,
                key=f"fuel_sales_{year_selected}_{month_selected}_{idx}"
            )
            df_income.at[idx, "Fuel Gallons"] = st.number_input(
                f"Fuel Gallons - Day {idx + 1}",
                min_value=0,
                value=row["Fuel Gallons"],
                step=10,
                key=f"fuel_gallons_{year_selected}_{month_selected}_{idx}"
            )
            df_income.at[idx, "Rebates"] = st.number_input(
                f"Rebates - Day {idx + 1}",
                min_value=0,
                value=row["Rebates"],
                step=100,
                key=f"rebates_{year_selected}_{month_selected}_{idx}"
            )
            df_income.at[idx, "ATM"] = st.number_input(
                f"ATM - Day {idx + 1}",
                min_value=0,
                value=row["ATM"],
                step=100,
                key=f"atm_{year_selected}_{month_selected}_{idx}"
            )
            df_income.at[idx, "Other Income"] = st.number_input(
                f"Other Income - Day {idx + 1}",
                min_value=0,
                value=row["Other Income"],
                step=100,
                key=f"other_income_{year_selected}_{month_selected}_{idx}"
            )
    
    # Update the session state
    st.session_state['data'][year_selected][month_selected]["Income"] = df_income
    
    # Display the income table with totals
    st.subheader("Income Data Table")
    df_display_income = df_income.copy()
    df_display_income.loc['Total'] = df_display_income.sum(numeric_only=True)
    st.dataframe(df_display_income)

with tab[1]:
    st.header(f"Expenses Data for {month_selected} {year_selected}")
    df_expenses = st.session_state['data'][year_selected][month_selected]["Expenses"]
    
    # Input expenses data
    for idx, row in df_expenses.iterrows():
        df_expenses.at[idx, "Amount"] = st.number_input(
            f"{row['Expense']}",
            min_value=0,
            value=row["Amount"],
            step=100,
            key=f"expense_{year_selected}_{month_selected}_{idx}"
        )
    
    # Update the session state
    st.session_state['data'][year_selected][month_selected]["Expenses"] = df_expenses
    
    # Display the expenses table with totals
    st.subheader("Expenses Data Table")
    df_display_expenses = df_expenses.copy()
    total_expenses = df_display_expenses["Amount"].sum()
    df_display_expenses.loc['Total'] = ["Total Expenses", total_expenses]
    st.dataframe(df_display_expenses)

with tab[2]:
    st.header(f"Financial Summary for {month_selected} {year_selected}")
    
    # Get current month's income and expenses
    df_income = st.session_state['data'][year_selected][month_selected]["Income"]
    df_expenses = st.session_state['data'][year_selected][month_selected]["Expenses"]
    
    # Calculate totals
    income_totals, expenses_totals = calculate_totals(df_income, df_expenses)
    
    st.write(f"**Total Income:** ${income_totals.sum():,.2f}")
    st.write(f"**Total Expenses:** ${expenses_totals:,.2f}")
    st.write(f"**Net Profit:** ${income_totals.sum() - expenses_totals:,.2f}")

with tab[3]:
    st.header(f"Yearly Summary for {year_selected}")
    
    # Initialize totals
    yearly_income = pd.DataFrame({
        "Taxable": [],
        "Non-tax": [],
        "CC": [],
        "Sales Tax": [],
        "FS": [],
        "Lottery": [],
        "Lotto": [],
        "Fuel Sales": [],
        "Fuel Gallons": [],
        "Rebates": [],
        "ATM": [],
        "Other Income": []
    })
    yearly_expenses = 0
    
    for month in months:
        if month in st.session_state['data'][year_selected]:
            df_income = st.session_state['data'][year_selected][month]["Income"]
            df_expenses = st.session_state['data'][year_selected][month]["Expenses"]
            
            # Sum income for the month
            monthly_income = df_income.sum(numeric_only=True)
            yearly_income = yearly_income.append(monthly_income, ignore_index=True)
            
            # Sum expenses for the month
            monthly_expenses = df_expenses["Amount"].sum()
            yearly_expenses += monthly_expenses
    
    # Calculate yearly totals
    yearly_income_total = yearly_income.sum()
    
    # Display yearly totals
    st.subheader("Yearly Income Totals")
    df_yearly_income = pd.DataFrame([yearly_income_total])
    df_yearly_income.index = ["Total"]
    st.table(df_yearly_income)
    
    st.subheader("Yearly Expenses Total")
    st.write(f"**Total Expenses:** ${yearly_expenses:,.2f}")
    
    st.subheader("Yearly Financial Statement")
    st.write(f"**Total Income:** ${yearly_income_total.sum():,.2f}")
    st.write(f"**Total Expenses:** ${yearly_expenses:,.2f}")
    st.write(f"**Net Profit:** ${yearly_income_total.sum() - yearly_expenses:,.2f}")

# Option to download the data
st.sidebar.header("Download Data")
if st.sidebar.button("Download Yearly Income as CSV"):
    yearly_income_sum = pd.DataFrame([yearly_income_total])
    yearly_income_sum.index = ["Total"]
    csv = yearly_income_sum.to_csv(index=True)
    st.sidebar.download_button(label="Download Yearly Income CSV", data=csv, mime="text/csv", file_name=f"Yearly_Income_{year_selected}.csv")

if st.sidebar.button("Download Yearly Expenses as CSV"):
    df_yearly_expenses = pd.DataFrame({
        "Expense": ["Total Expenses"],
        "Amount": [yearly_expenses]
    })
    csv_exp = df_yearly_expenses.to_csv(index=False)
    st.sidebar.download_button(label="Download Yearly Expenses CSV", data=csv_exp, mime="text/csv", file_name=f"Yearly_Expenses_{year_selected}.csv")
