import streamlit as st
import pandas as pd
import json

def get_log(dbname="logs.db", table="chat_completions"):
    import sqlite3

    con = sqlite3.connect(dbname)
    query = f"SELECT * from {table}"
    cursor = con.execute(query)
    rows = cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    data = [dict(zip(column_names, row)) for row in rows]
    con.close()
    return data

def str_to_dict(s):
    return json.loads(s)


log_data = get_log()
log_data_df = pd.DataFrame(log_data)

log_data_df["total_tokens"] = log_data_df.apply(
    lambda row: str_to_dict(row["response"])["usage"]["total_tokens"], axis=1
)

log_data_df["request"] = log_data_df.apply(lambda row: str_to_dict(row["request"])["messages"][0]["content"], axis=1)

# Streamlit app
st.title("Request and Response Log Viewer")

# Sidebar for filtering
st.sidebar.header("Filter Options")
min_tokens = st.sidebar.number_input("Minimum Total Tokens", min_value=0, value=0)
max_tokens = st.sidebar.number_input("Maximum Total Tokens", min_value=0, value=1000)

# Filtered DataFrame
filtered_df = log_data_df[
    (log_data_df["total_tokens"] >= min_tokens) & (log_data_df["total_tokens"] <= max_tokens)
]

# Display filtered DataFrame
st.write("Filtered Log Data:")
st.dataframe(filtered_df[["request", "response", "total_tokens"]])

# Detailed View
st.write("Detailed View:")
selected_row = st.selectbox("Select a Request:", filtered_df["request"])

if selected_row:
    response = filtered_df[filtered_df["request"] == selected_row]["response"].values[0]
    st.write(f"**Request:** {selected_row}")
    st.write(f"**Response:** {response}")
