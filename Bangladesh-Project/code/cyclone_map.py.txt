import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import io

# ১. পেজ কনফিগারেশন
st.set_page_config(page_title="BD Cyclone Risk Dashboard", layout="wide")
st.title("🌪️ Cyclone Risk & Population Density Dashboard")

# ২. আপনার দেওয়া ডেটা (সঠিক Lat/Lon সহ)
csv_data = """district,lat,lon,cyclone_risk,population_density,coastal_exposure_index
CoxsBazar,21.4272,92.0058,9,800,95
Bhola,22.6859,90.6455,8,720,92
Satkhira,22.7131,89.0723,8,650,90
Khulna,22.8456,89.5403,7,610,85
Barisal,22.7010,90.3535,7,590,84
Patuakhali,22.3524,90.3347,9,500,93
Chattogram,22.3569,91.7832,8,900,88
Noakhali,22.8695,91.0991,7,760,86
Barguna,22.1593,90.1118,9,430,94
Lakshmipur,22.9427,90.8415,6,700,82"""

df = pd.read_csv(io.StringIO(csv_data))

# ৩. সাইডবার ফিল্টার
st.sidebar.header("কন্ট্রোল প্যানেল")
selected_districts = st.sidebar.multiselect(
    "জেলা নির্বাচন করুন:",
    options=df["district"].unique(),
    default=df["district"].unique()
)
filtered_df = df[df["district"].isin(selected_districts)]

# ৪. লেআউট তৈরি (দুই কলাম)
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader("📍 Cyclone Risk Interactive Map")
    # ম্যাপ তৈরি
    m = folium.Map(location=[22.5, 90.5], zoom_start=7, tiles='CartoDB positron')
    
    for _, row in filtered_df.iterrows():
        # ঝুঁকি অনুযায়ী রঙ
        color = '#ff3f34' if row['cyclone_risk'] >= 9 else '#ff9f1a' if row['cyclone_risk'] >= 7 else '#32ff7e'
        
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=row['coastal_exposure_index'] / 5,
            popup=f"<b>{row['district']}</b><br>Risk: {row['cyclone_risk']}/10",
            tooltip=row['district'],
            color=color,
            fill=True,
            fill_opacity=0.7
        ).add_to(m)
    
    # ম্যাপ প্রদর্শন
    st_folium(m, width=700, height=500)

with col2:
    st.subheader("📊 Risk vs Exposure Analysis")
    # বার চার্ট
    st.bar_chart(filtered_df.set_index("district")[["cyclone_risk", "coastal_exposure_index"]])
    
    st.subheader("👥 Population Density")
    st.area_chart(filtered_df.set_index("district")["population_density"])

# ৫. ডেটা টেবিল
st.divider()
st.subheader("📋 Raw Data Table")
st.dataframe(filtered_df, use_container_width=True)
