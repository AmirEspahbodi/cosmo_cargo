import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from model import Shipment, Base
from core.connection.postgres import DATABASE_URL

# Page configuration
st.set_page_config(
    page_title="Shipment Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Create a header
st.title("Shipment Tracking Dashboard")
st.write("Interactive visualization and management of interplanetary shipments")

# Database connection function - cache it to improve performance
@st.cache_resource
def get_engine():
    connection_string = DATABASE_URL
    return create_engine(connection_string)

# Data loading function
@st.cache_data
def load_shipment_data():
    engine = get_engine()
    with Session(engine) as session:
        # Query only non-deleted shipments
        query = select(Shipment).where(Shipment.is_deleted == False)
        result = session.execute(query).scalars().all()
        
        # Convert SQLAlchemy objects to dictionaries
        shipments = []
        for shipment in result:
            shipment_dict = {
                "id": shipment.id,
                "time": shipment.time,
                "weight_kg": shipment.weight_kg,
                "volume_m3": shipment.volume_m3,
                "eta_min": shipment.eta_min,
                "status": shipment.status,
                "forecast_origin_wind_velocity_mph": shipment.forecast_origin_wind_velocity_mph,
                "forecast_origin_wind_direction": shipment.forecast_origin_wind_direction,
                "forecast_origin_precipitation_chance": shipment.forecast_origin_precipitation_chance,
                "forecast_origin_precipitation_kind": shipment.forecast_origin_precipitation_kind,
                "origin_solar_system": shipment.origin_solar_system,
                "origin_planet": shipment.origin_planet,
                "origin_country": shipment.origin_country,
                "origin_address": shipment.origin_address,
                "destination_solar_system": shipment.destination_solar_system,
                "destination_planet": shipment.destination_planet,
                "destination_country": shipment.destination_country,
                "destination_address": shipment.destination_address,
                "created_at": shipment.created_at,
                "is_restored": shipment.is_restored,
                "restored_at": shipment.restored_at
            }
            shipments.append(shipment_dict)
        
        return pd.DataFrame(shipments)

# Load the data
try:
    df = load_shipment_data()
    st.success(f"Successfully loaded {len(df)} shipment records")
except Exception as e:
    st.error(f"Error connecting to database: {e}")
    st.stop()

# Display sample data
st.subheader("Sample Data")
st.dataframe(df.head(5), use_container_width=True)


# Create sidebar for search and filters
st.sidebar.title("Shipment Search & Filters")

# Global search across all text fields
search_term = st.sidebar.text_input("Search all fields:")

# Apply the search filter
if search_term:
    # Convert all columns to string for searching across different data types
    filtered_df = df[df.astype(str).apply(lambda row: row.str.contains(search_term, case=False).any(), axis=1)]
else:
    filtered_df = df.copy()

# Add specific filters in collapsible sections
with st.sidebar.expander("Status Filter"):
    status_options = sorted(df['status'].unique().tolist())
    selected_statuses = st.multiselect("Select status:", status_options, default=status_options)
    if selected_statuses:
        filtered_df = filtered_df[filtered_df['status'].isin(selected_statuses)]

with st.sidebar.expander("Origin Location Filter"):
    # Solar System Filter
    origin_systems = sorted(df['origin_solar_system'].unique().tolist())
    selected_origin_systems = st.multiselect("Origin Solar System:", origin_systems, default=[])
    
    # Planet Filter - dynamically updated based on selected solar systems
    if selected_origin_systems:
        filtered_df = filtered_df[filtered_df['origin_solar_system'].isin(selected_origin_systems)]
        origin_planets = sorted(filtered_df['origin_planet'].unique().tolist())
    else:
        origin_planets = sorted(df['origin_planet'].unique().tolist())
        
    selected_origin_planets = st.multiselect("Origin Planet:", origin_planets, default=[])
    if selected_origin_planets:
        filtered_df = filtered_df[filtered_df['origin_planet'].isin(selected_origin_planets)]

with st.sidebar.expander("Destination Location Filter"):
    # Solar System Filter
    dest_systems = sorted(df['destination_solar_system'].unique().tolist())
    selected_dest_systems = st.multiselect("Destination Solar System:", dest_systems, default=[])
    
    # Planet Filter - dynamically updated
    if selected_dest_systems:
        filtered_df = filtered_df[filtered_df['destination_solar_system'].isin(selected_dest_systems)]
        dest_planets = sorted(filtered_df['destination_planet'].unique().tolist())
    else:
        dest_planets = sorted(df['destination_planet'].unique().tolist())
        
    selected_dest_planets = st.multiselect("Destination Planet:", dest_planets, default=[])
    if selected_dest_planets:
        filtered_df = filtered_df[filtered_df['destination_planet'].isin(selected_dest_planets)]

with st.sidebar.expander("Shipment Metrics Filter"):
    # Weight range slider
    min_weight = float(df['weight_kg'].min())
    max_weight = float(df['weight_kg'].max())
    weight_range = st.slider(
        "Weight Range (kg):",
        min_weight, max_weight, (min_weight, max_weight)
    )
    filtered_df = filtered_df[
        (filtered_df['weight_kg'] >= weight_range[0]) & 
        (filtered_df['weight_kg'] <= weight_range[1])
    ]
    
    # Volume range slider
    min_volume = float(df['volume_m3'].min())
    max_volume = float(df['volume_m3'].max())
    volume_range = st.slider(
        "Volume Range (m³):",
        min_volume, max_volume, (min_volume, max_volume)
    )
    filtered_df = filtered_df[
        (filtered_df['volume_m3'] >= volume_range[0]) & 
        (filtered_df['volume_m3'] <= volume_range[1])
    ]
    
    # ETA range slider
    min_eta = int(df['eta_min'].min())
    max_eta = int(df['eta_min'].max())
    eta_range = st.slider(
        "ETA Range (minutes):",
        min_eta, max_eta, (min_eta, max_eta)
    )
    filtered_df = filtered_df[
        (filtered_df['eta_min'] >= eta_range[0]) & 
        (filtered_df['eta_min'] <= eta_range[1])
    ]

# Display the filtered data with pagination
st.subheader("Filtered Shipment Data")
st.write(f"Showing {len(filtered_df)} of {len(df)} shipments")

# Add pagination for large datasets
page_size = st.selectbox("Rows per page:", [10, 25, 50, 100])
total_pages = (len(filtered_df) - 1) // page_size + 1
if total_pages > 1:
    page_number = st.number_input("Page:", min_value=1, max_value=total_pages, step=1)
    start_idx = (page_number - 1) * page_size
    end_idx = min(start_idx + page_size, len(filtered_df))
    page_df = filtered_df.iloc[start_idx:end_idx]
else:
    page_df = filtered_df.head(page_size)

# Display the data table
st.dataframe(page_df, use_container_width=True)

# Add download functionality
st.download_button(
    label="Download filtered data as CSV",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='shipment_data.csv',
    mime='text/csv',
)
