
"""
Traceability & Responsible Sourcing GIS Dashboard
"""

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from src.config import BASE_DIR, COMPLIANCE_COLORS
from src.data_loader import load_traceability_data, validate_and_enrich_data

# PAGE CONFIG 
st.set_page_config(
    page_title="Traceability & Responsible Sourcing Map",
    page_icon="🌍",
    layout="wide"
)

st.title("Ethiopian Specialty Coffee Traceability & Responsible Sourcing")
st.markdown("**Interactive GIS Dashboard • EUDR Compliant • Real Locations**")

# LOAD DATA 
@st.cache_data
def get_data():
    df = load_traceability_data()
    return validate_and_enrich_data(df)

df = get_data()

# SIDEBAR 
st.sidebar.header("Filters")

selected_regions = st.sidebar.multiselect(
    "Region", 
    options=sorted(df['region'].unique()),
    default=sorted(df['region'].unique())
)

selected_traceability = st.sidebar.multiselect(
    "Traceability Level",
    options=df['traceability_level'].unique(),
    default=df['traceability_level'].unique()
)

compliance_filter = st.sidebar.selectbox(
    "EUDR Status",
    ["All Lots", "Compliant Only", "At Risk"]
)

# FILTER DATA 
filtered_df = df[
    (df['region'].isin(selected_regions)) &
    (df['traceability_level'].isin(selected_traceability))
]

if compliance_filter == "Compliant Only":
    filtered_df = filtered_df[filtered_df['eudr_compliant'] == True]
elif compliance_filter == "At Risk":
    filtered_df = filtered_df[filtered_df['compliance_status'] == "At Risk"]

#  METRICS 
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Lots on Map", len(filtered_df))
with c2:
    st.metric("EUDR Compliant", f"{filtered_df['eudr_compliant'].sum()} ({filtered_df['eudr_compliant'].mean()*100:.1f}%)")
with c3:
    st.metric("Avg SCA Score", f"{filtered_df['sca_score'].mean():.2f}")
with c4:
    st.metric("Low Deforestation Risk", (filtered_df['deforestation_risk'] == 'Low').sum())

st.divider()

# FOLIUM MAP
st.subheader("Interactive Traceability Map")

# Better center for Ethiopia
m = folium.Map(location=[7.8, 38.0], zoom_start=7, tiles="Cartodb Positron")

for _, row in filtered_df.iterrows():
    color = COMPLIANCE_COLORS.get(row['compliance_status'], "blue")

    popup_html = f"""
        <b>Lot:</b> {row['lot_id']}<br>
        <b>Supplier:</b> {row['supplier_name']}<br>
        <b>Region:</b> {row['region']}<br>
        <b>District:</b> {row['district']}<br>
        <b>Altitude:</b> {row['altitude_m']}m<br><br>
        <b>Score:</b> {row['sca_score']} | <b>Grade:</b> {row['grade_ecx']}<br>
        <b>Traceability:</b> {row['traceability_level']}<br>
        <b>Certification:</b> {row['sustainability_cert']}<br>
        <b>EUDR:</b> {' Compliant' if row['eudr_compliant'] else ' Not Compliant'}<br>
        <b>Risk:</b> {row['deforestation_risk']}
    """

    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=8,
        popup=folium.Popup(popup_html, max_width=350),
        color=color,
        fill=True,
        fillOpacity=0.85,
        tooltip=f"{row['lot_id']} - {row['region']}"
    ).add_to(m)

folium.LayerControl().add_to(m)

st_folium(m, width=1400, height=700)

# FOOTER 
st.divider()
st.caption("**Aklilu Abera** | **Specialty Coffee Analyst** ")
st.caption("**Traceability & Responsible Sourcing GIS Dashboard** | **Aligned with EUDR & Responsible Sourcing Standards**")
