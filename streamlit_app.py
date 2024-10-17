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

# Income categories
income_categories = ["Taxable", "Non-tax", "CC", "Sales Tax", "FS", "Lottery", "Lotto", "Fuel Sales", "Fuel Gallons", "Rebates", "ATM", "Other Income"]

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
        })
    }

# Function to calculate totals
def calculate_totals(df_income):
    return df_income.sum(axis=0, numeric_only=True)

# Display income table
st.header(f"Income Data for {month_selected} {year_selected}")
df_income = st.session_state['data'][year_selected][month_selected]["Income"]

# Add column headers (Income categories) and row labels (Day 1, Day 2, etc.)
st.subheader("Input Daily Data")

# Create the header with the income categories
st.write("### Income Categories:")
st.write(f"| {' | '.join(income_categories)} |")  # Show category headers as columns

# Input data for each day (Day as rows, Categories as columns)
for idx, day in enumerate(df_income["Day"]):
    st.write(f"### {day}")  # Display Day label for the row
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
df_display_income.loc['Total'] = calculate_totals(df_display_income)
st.dataframe(df_display_income)

# Option to save work and download CSV
st.sidebar.header("Save Work")
csv = df_display_income.to_csv(index=False)
st.sidebar.download_button(label="Download Income CSV", data=csv, mime="text/csv", file_name=f"Income_{month_selected}_{year_selected}.csv")

# Option to upload a CSV to restore data
uploaded_file = st.sidebar.file_uploader("Upload Income CSV", type="csv")
if uploaded_file is not None:
    df_income_uploaded = pd.read_csv(uploaded_file)
    st.session_state['data'][year_selected][month_selected]["Income"] = df_income_uploaded
    st.success("Income data uploaded successfully!")
