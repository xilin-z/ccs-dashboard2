import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Title and description
st.title("CCS Stakeholder Sustainability Simulator")
st.markdown("""
This interactive dashboard simulates CCS project outcomes by region and year,
based on customizable sustainability metrics.
""")

# Generate or load data
@st.cache_data
def load_data():
    years = list(range(2020, 2026))
    regions = ['SouthSea', 'NorthBay']
    data = []

    for year in years:
        for region in regions:
            capture_cost = np.random.randint(50, 100)
            transport_cost = np.random.randint(5, 15)
            storage_cost = np.random.randint(8, 20)
            co2_price = np.random.uniform(60, 100)
            co2_volume = np.random.randint(80000, 120000)

            total_cost = (capture_cost + transport_cost + storage_cost) * co2_volume / 1e6
            total_revenue = co2_price * co2_volume / 1e6
            net_benefit = total_revenue - total_cost

            data.append({
                "year": year,
                "region": region,
                "capture_cost": capture_cost,
                "transport_cost": transport_cost,
                "storage_cost": storage_cost,
                "co2_price": co2_price,
                "co2_volume": co2_volume,
                "total_cost_million": round(total_cost, 2),
                "total_revenue_million": round(total_revenue, 2),
                "net_benefit_million": round(net_benefit, 2),
                "production_rate": np.random.randint(80000, 120000),
                "reliability_score": np.random.uniform(0.6, 0.95),
                "profit_margin": np.random.uniform(0.1, 0.4),
                "eroi": np.random.uniform(2.0, 5.0),
                "carbon_neutrality_score": np.random.uniform(0.3, 0.9),
                "env_friendly_score": np.random.uniform(0.4, 0.9),
            })

    return pd.DataFrame(data)

df = load_data()

# Sidebar - set weights
st.sidebar.header("Set Sustainability Weights")
weight_profit = st.sidebar.slider("Profitability", 0.0, 1.0, 0.3)
weight_reliability = st.sidebar.slider("Reliability", 0.0, 1.0, 0.2)
weight_eroi = st.sidebar.slider("EROI", 0.0, 1.0, 0.15)
weight_neutrality = st.sidebar.slider("Carbon Neutrality", 0.0, 1.0, 0.15)
weight_env = st.sidebar.slider("Environmental Friendliness", 0.0, 1.0, 0.2)

# Normalize and calculate sustainability score
df['sustainability_score'] = (
    df['profit_margin'] * weight_profit +
    df['reliability_score'] * weight_reliability +
    (df['eroi'] / 10) * weight_eroi +
    df['carbon_neutrality_score'] * weight_neutrality +
    df['env_friendly_score'] * weight_env
) * 100

# Filters
year_filter = st.selectbox("Select Year", sorted(df['year'].unique()))
region_filter = st.selectbox("Select Region", sorted(df['region'].unique()))
filtered_df = df[(df['year'] == year_filter) & (df['region'] == region_filter)]

# Show key results
st.subheader(f"Results for {region_filter} in {year_filter}")
st.write(filtered_df[['total_cost_million', 'total_revenue_million', 'net_benefit_million',
                     'sustainability_score']])

# Charts
st.subheader("Net Benefit vs Sustainability Score")
fig, ax = plt.subplots()
for region in df['region'].unique():
    region_data = df[df['region'] == region]
    ax.plot(region_data['year'], region_data['net_benefit_million'], marker='o', label=f"{region} - Benefit")
    ax.plot(region_data['year'], region_data['sustainability_score'], marker='s', linestyle='--', label=f"{region} - Sustainability")

ax.set_xlabel("Year")
ax.set_ylabel("Value")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Data preview
st.subheader("Full Data Table")
st.dataframe(df.round(2))
