import streamlit as st
import pandas as pd

# Function to get tables from Wikipedia
def get_wikipedia_tables():
    url = "https://en.wikipedia.org/wiki/Boston_University_Terriers_men%27s_ice_hockey"
    try:
        tables = pd.read_html(url)
        return tables
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return []

# Streamlit UI
st.title("BU Men's Hockey Data")

tables = get_wikipedia_tables()

if not tables:
    st.warning("No tables found. Check the Wikipedia URL.")
else:
    for i, table in enumerate(tables):
        st.subheader(f"Table {i}")
        st.dataframe(table)  # Display table in Streamlit


st.title("BU Men's Hockey Data - By Sean")

search_term = st.text_input("Search for a keyword in tables:")

tables = get_wikipedia_tables()

if not tables:
    st.warning("No tables found.")
else:
    for i, table in enumerate(tables):
        if search_term.lower() in table.to_string().lower():
            st.subheader(f"Table {i} (Matches: {search_term})")
            st.dataframe(table)

import matplotlib.pyplot as plt

# Assuming a table has 'Season' and 'Wins' columns
if tables:
    for table in tables:
        if "Season" in table.columns and "Wins" in table.columns:
            st.subheader("BU Hockey Wins Per Season")

            # Convert Season to string for better visualization
            table["Season"] = table["Season"].astype(str)

            # Matplotlib Chart
            fig, ax = plt.subplots()
            ax.plot(table["Season"], table["Wins"], marker="o", linestyle="-")
            ax.set_xlabel("Season")
            ax.set_ylabel("Wins")
            ax.set_title("BU Hockey Wins Per Season")
            ax.tick_params(axis='x', rotation=45)

            st.pyplot(fig)


table_options = [f"Table {i}" for i in range(len(tables))]

selected_table = st.selectbox("Select a table:", table_options)

if tables:
    index = table_options.index(selected_table)
    st.dataframe(tables[index])
