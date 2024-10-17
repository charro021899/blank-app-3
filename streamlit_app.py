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
            "Category": ["Taxable", "Non-tax", "CC", "Sales Tax", "FS", "Lottery", "Lotto", "Fuel Sales", "Fuel Gallons", "Rebates", "ATM", "Other Income"],
            **{f"Day {i}": [0]*12 for i in range(1, 32)}  # Create columns for each day
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
    
    # Display day-by-day inputs in row format
    st.subheader("Input Daily Data")
    for category in df_income["Category"]:
        cols = st.columns(31)  # Create 31 columns for the days
        st.write(f"### {category}")
        for day in range(1, 32):
            df_income.at[df_income[df_income["Category"] == category].index[0], f"Day {day}"] = cols[day-1].number_input(
                f"Day {day}", min_value=0, value=df_income.loc[df_income["Category"] == category, f"Day {day}"].values[0], step=100, key=f"{category}_{day}_{month_selected}_{year_selected}"
            )
    
    # Update the session state
    st.session_state['data'][year_selected][month_selected]["Income"] = df_income
    
    # Display the income table with totals
    st.subheader("Income Data Table")
    df_display_income = df_income.copy()
    df_display_income["Total"] = df_display_income.sum(axis=1, numeric_only=True)
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
            monthly_income = df_income.sum(axis=1, numeric_only=True)
            yearly_income = pd.concat([yearly_income, monthly_income], axis=1)
            
            # Sum expenses for the month
            monthly_expenses = df_expenses["Amount"].sum()
            yearly_expenses += monthly_expenses
    
    # Calculate yearly totals
    yearly_income_total = yearly_income.sum(axis=1)
    
    # Display yearly totals
    st.subheader("Yearly Income Totals")
    st.write(yearly_income_total)
    
    st.subheader("Yearly Expenses Total")
    st.write(f"**Total Expenses:** ${yearly_expenses:,.2f}")
    
    st.subheader("Yearly Financial Statement")
    st.write(f"**Total Income:** ${yearly_income_total.sum():,.2f}")
    st.write(f"**Total Expenses:** ${yearly_expenses:,.2f}")
    st.write(f"**Net Profit:** ${yearly_income_total.sum() - yearly_expenses:,.2f}")

# Saving and Uploading Work
st.sidebar.header("Save/Upload Work")
if st.sidebar.button("Download Current Income Data"):
    csv = df_display_income.to_csv(index=False)
    st.sidebar.download_button(label="Download Income CSV", data=csv, mime="text/csv", file_name=f"Income_{month_selected}_{year_selected}.csv")

if st.sidebar.button("Download Current Expense Data"):
    csv_exp = df_display_expenses.to_csv(index=False)
    st.sidebar.download_button(label="Download Expenses CSV", data=csv_exp, mime="text/csv", file_name=f"Expenses_{month_selected}_{year_selected}.csv")

# Option to upload data
uploaded_file = st.sidebar.file_uploader("Upload Income CSV", type="csv")
if uploaded_file is not None:
    df_income_uploaded = pd.read_csv(uploaded_file)
    st.session_state['data'][year_selected][month_selected]["Income"] = df_income_uploaded
    st.success("Income data uploaded successfully!")
