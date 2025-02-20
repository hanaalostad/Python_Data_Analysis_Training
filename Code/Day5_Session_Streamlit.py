import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium


# **🔹 Load Dataset**
@st.cache_data
def load_data():
    df = pd.read_csv("Store_tran.csv")
    df["Date"]=pd.to_datetime(df["Date"])
    return df

df = load_data()

# **🔹 Data Cleaning Functions**
def clean_data(df):
    df.drop_duplicates(inplace=True)  # Remove duplicate rows
    df["Quantity"].fillna(df["Quantity"].median(), inplace=True)  # Fill missing Quantity with median
    df["Price"].fillna(df["Price"].median(), inplace=True)  # Fill missing Price with median
    df["TotalAmount"] = df["Quantity"] * df["Price"]  # Recalculate TotalAmount
    return df

df = clean_data(df)

# **🎯 Streamlit UI**
st.title("📊 Sales Data Analysis & Cleaning")

# **🔍 Data Overview**
st.subheader("📋 Raw & Cleaned Data")
view_option = st.radio("Select Data View:", ["Raw Data", "Cleaned Data"])
if view_option == "Raw Data":
    st.write(load_data())  # Show original data

else:
    st.write(df)  # Show cleaned data


# **📊 Data Filtering**
st.subheader("🔎 Filter Sales Data")
selected_category = st.selectbox("Filter by Category", ["All"] + list(df["Category"].unique()))
if selected_category != "All":
    df = df[df["Category"] == selected_category]

selected_city = st.multiselect("Select Cities", df["City"].unique(), default=df["City"].unique())
df = df[df["City"].isin(selected_city)]

st.write(df)  # Display filtered data

# **📊 Data Visualization**
st.subheader("📊 Visualizations")

# **1️⃣ Sales Distribution**
st.write("### Sales Distribution")
fig, ax = plt.subplots(figsize=(6, 4))
sns.histplot(df["TotalAmount"], bins=10)
plt.xlabel("Total Sales ($)")
plt.xticks(rotation=45)
plt.ylabel("Frequency")
st.pyplot(fig)

# **2️⃣ Sales by Category**
st.write("### Total Sales by Category")
category_sales = df.groupby("Category")["TotalAmount"].sum().reset_index()
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x="Category", y="TotalAmount", data=category_sales)
plt.xlabel("Category")
plt.ylabel("Total Sales ($)")
st.pyplot(fig)

# **3️⃣ Outlier Detection (Boxplot)**
st.write("### Boxplot for Outlier Detection")
fig, ax = plt.subplots(figsize=(6, 4))
sns.boxplot(x=df["TotalAmount"], color="red")
plt.xlabel("Total Sales ($)")
st.pyplot(fig)

# **🗺️ Map Visualization**
st.subheader("🗺️ Sales Locations")

# Sample Latitude & Longitude for Cities
city_coords = {
    "New York": [40.7128, -74.0060],
    "Chicago": [41.8781, -87.6298],
    "Los Angeles": [34.0522, -118.2437],
    "Miami": [25.7617, -80.1918],
    "San Francisco": [37.7749, -122.4194],
    "Boston": [42.3601, -71.0589]
}

# Create a Folium Map

m = folium.Map(location=[39.8283, -98.5795], zoom_start=3)
for _, row in df.iterrows():
    if row["City"] in city_coords:
        folium.Marker(
            location=city_coords[row["City"]],
            popup=f"{row['Customer']} - ${row['TotalAmount']}",
            tooltip=row["City"],
            icon=folium.Icon(color="blue", icon="shopping-cart", prefix="fa")
        ).add_to(m)

st_folium(m,width=700,height=400)
