import pandas as pd

url = "https://en.wikipedia.org/wiki/Boston_University_Terriers_men%27s_ice_hockey"
tables = pd.read_html(url)  # Extracts all tables into a list

print(f"Number of tables found: {len(tables)}")  # Debugging check

for i, table in enumerate(tables):
    print(f"Table {i}")
    print(table.head())  # Preview the first few rows


import streamlit as st

st.title("BU Men's Hockey Data")

for i, table in enumerate(tables):
    st.subheader(f"Table {i}")
    st.dataframe(table)
