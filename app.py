import pandas as pd
import plotly.express as px
import streamlit as st

# Configuration
st.set_page_config(page_title="Car sales", layout="wide")

# Load data
car_data = pd.read_csv('vehicles_us.csv')
data = car_data.copy()

# Title and description
st.title('Car sales')
st.write('Explore data from car sale listings here.')


# Laterakl sidebar for filters
st.sidebar.header("Filters")

if st.sidebar.checkbox('Price'):
    price = st.sidebar.slider("Price ($)", float(car_data['price'].min()),
                              float(car_data['price'].max()),
                              float(car_data['price'].median()))
    data = data[data['price'] <= price]

if st.sidebar.checkbox('Year'):
    year = st.sidebar.selectbox("Year", sorted(
        car_data['model_year'].dropna().astype(int).unique()))
    data = data[data['model_year'] == year]

if st.sidebar.checkbox('Condition'):
    condition = st.sidebar.selectbox(
        "Condition", car_data['condition'].dropna().unique())
    data = data[data['condition'] == condition]


# Statistics
col1, col2, col3, col4 = st.columns([1.5, 1.5, 2, 2])
with col1:
    st.metric("📊 Average price", f"${data['price'].mean():,.0f}")
with col2:
    st.metric("💰 Lowest price", f"${data['price'].min():,.0f}")
with col3:
    st.metric("💸 Highest price", f"${data['price'].max():,.0f}")
with col4:
    st.metric("🚙 Average mileage", f"{data['odometer'].mean():,.0f} km")


# Show dataset
column_names = {
    'price': 'Price',
    'model_year': 'Year',
    'odometer': 'Mileage (Km)',
    'condition': 'Condition',
    'fuel': 'Fuel',
    'paint_color': 'Color',
    'cylinders': 'Cylinders',
    'type': 'Type',
    'is_4wd': '4WD',
    'model': 'Model',
    'transmission': 'Transmission',
    'date_posted': 'Posted date',
    'days_listed': 'Days listed',
}
st.write("### Filtered dataset", data.rename(columns=column_names))


# Charts
st.write("### Analysis charts")
st.write('Click on the boxes to view the charts.')

# Average price by car type
with st.expander("Average price by car type"):
    if not data.empty:
        avg_price_by_type = data.groupby('type')['price'].mean(
        ).reset_index().sort_values(by='price', ascending=False)
        fig1 = px.bar(avg_price_by_type, x='type', y='price', labels={'type': 'Car type', 'price': 'Price ($)'},
                      color='price', color_continuous_scale='Blues')
        fig1.update_traces(texttemplate='%{y:.2s}', textposition='outside')
        st.plotly_chart(fig1, use_container_width=True, key="graf_tipo")

# Relationship between year and price
with st.expander("Relationship between year and price"):
    fig2 = px.scatter(data, x='model_year', y='price', labels={'model_year': 'Year', 'price': 'Price ($)'},
                      color='condition', trendline='ols')
    st.plotly_chart(fig2, use_container_width=True, key="graf_year")

col1, col2 = st.columns(2)
# Mileage distribution
with col1:
    with st.expander("Mileage distribution"):
        fig3 = px.histogram(data, x='odometer', nbins=40, labels={'odometer': 'Mileage (Km)'},
                            color_discrete_sequence=['indianred'])
        fig3.update_traces(opacity=0.7)
        st.plotly_chart(fig3, use_container_width=True, key="graf_odom")

# Percentage of 4WD vehicles
with col2:
    with st.expander("Percentage of 4WD vehicles"):
        if 'is_4wd' in data.columns:
            is_4wd_counts = data['is_4wd'].fillna(
                0).replace({0: 'No', 1: 'Yes'}).value_counts()
            fig4 = px.pie(names=is_4wd_counts.index,
                          values=is_4wd_counts.values)
            st.plotly_chart(fig4, use_container_width=True, key="graf_4wd")

# Average price by condition
with st.expander("Average price by condition"):
    avg_price_by_condition = data.groupby('condition')['price'].mean(
    ).reset_index().sort_values(by='price', ascending=False)
    fig5 = px.bar(avg_price_by_condition, x='condition', y='price', labels={'condition': 'Condition', 'price': 'Price ($)'},
                  color='price', color_continuous_scale='Greens')
    fig5.update_traces(texttemplate='%{y:.2s}', textposition='outside')
    st.plotly_chart(fig5, use_container_width=True, key="graf_cond")

# Distribution by cylinder count
with st.expander("Distribution by cylinder count"):
    cyl_counts = data['cylinders'].dropna().astype(
        str).value_counts().reset_index()
    cyl_counts.columns = ['cylinders', 'count']
    fig6 = px.bar(cyl_counts, x='cylinders', y='count', labels={'cylinders': 'Cylinders'},
                  color='count', color_continuous_scale='viridis')
    fig6.update_traces(texttemplate='%{y}', textposition='outside')
    st.plotly_chart(fig6, use_container_width=True, key="graf_cyl")

col1, col2 = st.columns(2)
# Fuel distribution
with col1:
    with st.expander("Fuel distribution"):
        fuel_counts = data['fuel'].dropna().value_counts()
        fig7 = px.pie(names=fuel_counts.index, values=fuel_counts.values)
        st.plotly_chart(fig7, use_container_width=True, key="graf_fuel")

# Color distribution
with col2:
    with st.expander("Color distribution"):
        color_counts = data['paint_color'].dropna().value_counts()
        fig8 = px.pie(names=color_counts.index,
                      values=color_counts.values)
        st.plotly_chart(fig8, use_container_width=True, key="graf_color")
