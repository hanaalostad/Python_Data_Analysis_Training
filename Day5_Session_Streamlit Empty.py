import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium


# ** Write a Function load_data to Load Dataset**


df = []
# ** Write Data Cleaning Function**
def clean_data(df):
     # Remove duplicate rows
     # Fill missing Quantity with median
    # Fill missing Price with median
    # Recalculate TotalAmount
    return df

df = clean_data(df)

# **Streamlit UI title**
st.title("📊 Sales Data Analysis & Cleaning")

# ** Data Overview**
# show subheader Raw & Cleaned Data

# show radio to select data view Raw data or Cleaned data

 
# Show cleaned data


# **Data Filtering**
# show subheader Filter Sales Data

# use select box to Filter by Category either all or list of category

# filter based on selection

# use multiselect to select citites
selected_city = []
# filter dataframe based on selected city
df = []

st.write(df)  # Display filtered data

# ** Data Visualization**
st.subheader("Visualizations")

# **1 Total Amount of Sales Distribution bins=10**
st.write("### Sales Distribution")
fig, ax = plt.subplots(figsize=(6, 4))
sns.histplot(df["TotalAmount"], bins=10)
plt.xlabel("Total Sales ($)")
plt.xticks(rotation=45)
plt.ylabel("Frequency")
st.pyplot(fig)

# **2️ Sales by Category**
st.write("### Total Sales by Category")
category_sales = df.groupby("Category")["TotalAmount"].sum().reset_index()
fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(x="Category", y="TotalAmount", data=category_sales)
plt.xlabel("Category")
plt.ylabel("Total Sales ($)")
st.pyplot(fig)

# **3️ Outlier Detection (Boxplot)**
st.write("### Boxplot for Outlier Detection")
fig, ax = plt.subplots(figsize=(6, 4))
sns.boxplot(x=df["TotalAmount"], color="red")
plt.xlabel("Total Sales ($)")
st.pyplot(fig)

# **4 Map Visualization**
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
