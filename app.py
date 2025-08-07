import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    excel_file = "property_data.xlsx"
    base_df = pd.read_excel(excel_file, sheet_name="Sheet3")
    owner_df = pd.read_excel(excel_file, sheet_name="Sheet1")
    tenant_df = pd.read_excel(excel_file, sheet_name="Sheet2")

    for df in [base_df, owner_df, tenant_df]:
        df.columns = df.columns.str.strip()
        df["Property Address"] = df["Property Address"].astype(str).str.strip()

    merged = pd.merge(base_df, owner_df, on="Property Address", how="left")
    merged = pd.merge(merged, tenant_df, on="Property Address", how="left")
    return merged

st.title("🏠 Hanna Dam-Nardelli Properties")

df = load_data()
property_list = df["Property Address"].dropna().unique()
search = st.text_input("🔍 Search Property Address")

filtered = [p for p in property_list if search.lower() in p.lower()]
selected_property = st.selectbox("Select Property", filtered)

if selected_property:
    record = df[df["Property Address"] == selected_property].iloc[0].to_dict()

    def section(title, fields):
        st.subheader(title)
        for f in fields:
            val = record.get(f, "N/A")
            val = "N/A" if pd.isna(val) or val == "" else val
            st.text(f"{f}: {val}")

    section("🏘 Property Details", [
        "Property Address", "Market Rent", "Sqft",
        "Management Flat Fee", "Management Fee Percent",
        "Waive Fees When Vacant", "Reserve"
    ])

    section("👤 Owner Information", [
        "Owner(s)", "Owner(s) - Phone Numbers"
    ])

    section("👥 Tenant Information", [
        "Tenant Name", "Status", "Tenant Phone", "Tenant Email",
        "Lease Start", "Lease End", "Rent Amount", "Deposit Amount"
    ])
