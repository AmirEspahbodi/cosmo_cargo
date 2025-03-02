import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from model import Shipment, Base  # Import your model
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

