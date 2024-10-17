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

# Income categories (Updated: "Other Income" is now "OI")
income_categories = ["Taxable", "Non-tax", "CC", "Sales Tax", "FS", "Lottery", "Lotto", "Fuel Sales", "Fuel Gallons", "Rebates", "ATM", "OI"]

# Exclude "CC", "Sales Tax", "Fuel Gallons" from income totals and only count 5% of "Lottery" and "Lotto"
income_for_total = ["Taxable", "Non-tax", "FS", "Lottery", "Lotto", "Fuel Sales", "Rebates", "ATM", "OI"]  # Exclude "CC", "Sales Tax", "Fuel Gallons"

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
    # Initialize income data with days as rows and categories as columns
    st.session_state['data'][year_selected][month_selected] = {
        "Income": pd.DataFrame({
            "Day": [f"Day {i}" for i in range(1, 32)],  # Rows for each day of the month
            **{category: [0]*31 for category in income_categories}  # Columns for each category
        }),
        "Expenses": pd.DataFrame({
            "Expense": expense_categories,
            "Amount": [0]*len(expense_categories)
        })
    }

# Function to calculate totals excluding CC, Sales Tax, Fuel Gallons, and counting only 5% of Lottery and Lotto
def calculate_income_totals(df_income):
    df_totals = df_income.sum(axis=0, numeric_only=True)
    df_totals["Lottery"] = df_totals["Lottery"] * 0.05  # Only 5% of Lottery sales as income
    df_totals["Lotto"] = df_totals["Lotto"] * 0.05  # Only 5% of Lotto sales as income
    return df_totals[income_for_total]  # Exclude CC, Sales Tax, Fuel Gallons

# Tabs for different sections: Income, Expenses, Summary, and Yearly Summary
tab = st.tabs(["Income", "Expenses", "Summary", "Yearly Summary"])

### INCOME SECTION ###
with tab[0]:
    st.header(f"Income Data for {month_selected} {year_selected}")
    df_income = st.session_state['data'][year_selected][month_selected]["Income"]

    # Input data for each day with the column headers for every day
    st.subheader("Input Daily Data")
    for idx, day in enumerate(df_income["Day"]):
        st.write(f"### {day}")  # Display Day label for the row
        st.write("| " + " | ".join(income_categories) + " |")  # Display income categories above each day's inputs
        cols = st.columns(len(income_categories))  # Create columns for the categories
        for i, category in enumerate(income_categories):
            df_income.at[idx, category] = cols[i].number_input(
                label="",  # No label in the input box
                min_value=0, 
                value=df_income.loc[idx, category], 
                step=100, 
                key=f"{category}_{day}_{month_selected}_{year_selected}"
            )

    # Display the income table with totals
    st.subheader("Income Data Table")
    df_display_income = df_income.copy()
    df_display_income.loc['Total'] = df_display_income.sum(axis=0, numeric_only=True)
    st.dataframe(df_display_income)

### EXPENSES SECTION ###
with tab[1]:
    st.header(f"Expenses Data for {month_selected} {year_selected}")
    df_expenses = st.session_state['data'][year_selected][month_selected]["Expenses"]

    # Input expenses data
    st.subheader("Input Monthly Expenses")
    for idx, row in df_expenses.iterrows():
        df_expenses.at[idx, "Amount"] = st.number_input(
            f"{row['Expense']}",
            min_value=0,
            value=row["Amount"],
            step=100,
            key=f"expense_{year_selected}_{month_selected}_{idx}"
        )

    # Display the expenses table with totals
    st.subheader("Expenses Data Table")
    df_display_expenses = df_expenses.copy()
    total_expenses = df_display_expenses["Amount"].sum()
    df_display_expenses.loc['Total'] = ["Total Expenses", total_expenses]
    st.dataframe(df_display_expenses)

### SUMMARY SECTION ###
with tab[2]:
    st.header(f"Financial Summary for {month_selected} {year_selected}")

    # Get current month's income and expenses
    df_income = st.session_state['data'][year_selected][month_selected]["Income"]
    df_expenses = st.session_state['data'][year_selected][month_selected]["Expenses"]

    # Calculate income and expense totals
    income_totals = calculate_income_totals(df_income)
    expenses_totals = df_expenses["Amount"].sum()

    # Display the income categories with details
    st.subheader("Detailed Income Categories")
    st.write(income_totals)

    # Display the CC, Sales Tax, Fuel Gallons as reference
    st.subheader("Reference Numbers (CC, Sales Tax, Fuel Gallons)")
    st.write(df_income[["CC", "Sales Tax", "Fuel Gallons"]].sum(axis=0))

    # Display the expense categories in detail
    st.subheader("Detailed Expenses")
    st.write(df_expenses)

    # Financial summary
    st.subheader("Financial Summary")
    st.write(f"**Total Income:** ${income_totals.sum():,.2f}")
    st.write(f"**Total Expenses:** ${expenses_totals:,.2f}")
    st.write(f"**Net Profit:** ${income_totals.sum() - expenses_totals:,.2f}")

### YEARLY SUMMARY SECTION ###
with tab[3]:
    st.header(f"Yearly Summary for {year_selected}")

    # Initialize totals for yearly summary
    yearly_income = pd.DataFrame({category: [] for category in income_for_total})
    yearly_expenses = 0
    reference_totals = pd.DataFrame({
        "CC": [],
        "Sales Tax": [],
        "Fuel Gallons": []
    })

    # Loop through all months in the selected year and sum the data
    for month in months:
        if month in st.session_state['data'][year_selected]:
            df_income = st.session_state['data'][year_selected][month]["Income"]
            df_expenses = st.session_state['data'][year_selected][month]["Expenses"]

            # Sum income for the month
            monthly_income = calculate_income_totals(df_income)
            yearly_income = pd.concat([yearly_income, pd.DataFrame([monthly_income])], axis=1)

            # Sum expenses for the month
            monthly_expenses = df_expenses["Amount"].sum()
            yearly_expenses += monthly_expenses

            # Add CC, Sales Tax, Fuel Gallons reference numbers
            monthly_reference = df_income[["CC", "Sales Tax", "Fuel Gallons"]].sum(axis=0)
            reference_totals = pd.concat([reference_totals, pd.DataFrame([monthly_reference])], axis=1)

    # Calculate yearly totals
    yearly_income_total = yearly_income.sum(axis=1)
    reference_totals_total = reference_totals.sum(axis=1)

    # Display yearly income totals
    st.subheader("Yearly Income Totals")
    st.write(yearly_income_total)

    # Display reference numbers (CC, Sales Tax, Fuel Gallons)
    st.subheader("Yearly Reference Numbers (CC, Sales Tax, Fuel Gallons)")
    st.write(reference_totals
