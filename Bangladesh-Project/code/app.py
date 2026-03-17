import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import io

# ১. পেজ সেটআপ (Wide Layout)
st.set_page_config(page_title="Bangladesh Climate & Education Dashboard", layout="wide")

# সিএসএস দিয়ে ড্যাশবোর্ডকে আরও সুন্দর করা
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌍 Bangladesh Climate & Education Dashboard")
st.markdown("Interactive Data Analysis • Climate Risk • Educational Metrics")

# ২. ডেটা লোড (সবগুলো প্যারামিটার এক সাথে)
csv_data = """district,lat,lon,climate_risk,literacy_rate,school_access_index,population_at_risk
Dhaka,23.8103,90.4125,3,85,92,1.2
Chattogram,22.3569,91.7832,7,79,88,0.8
Rajshahi,24.3636,88.6241,4,78,85,0.5
Khulna,22.8456,89.5403,6,80,80,0.6
Barisal,22.7010,90.3535,8,75,76,0.9
Sylhet,24.8949,91.8687,6,72,79,0.4
Rangpur,25.7439,89.2752,5,74,82,0.5
Mymensingh,24.7471,90.4203,5,73,81,0.6
Bhola,22.6859,90.6455,9,68,65,1.5
Satkhira,22.7131,89.0723,10,70,63,1.1
"""
df = pd.read_csv(io.StringIO(csv_data))

# ৩. ফিল্টার সেকশন
st.sidebar.header("🔍 Filters")
selected_districts = st.sidebar.multiselect("Select Districts", options=df['district'].unique(), default=df['district'].unique())
filtered_df = df[df['district'].isin(selected_districts)]

# ৪. ওভারভিউ মেট্রিক্স (Overview Metrics)
st.subheader("📊 Overview")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Districts", len(filtered_df))
m2.metric("Avg Literacy Rate", f"{filtered_df['literacy_rate'].mean():.1f}%")
m3.metric("Population at Risk", f"{filtered_df['population_at_risk'].sum():.1f}M")
m4.metric("High Risk Districts", len(filtered_df[filtered_df['climate_risk'] >= 8]))

# ৫. ম্যাপ এবং এডুকেশনাল অ্যানালাইসিস
col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.subheader("📍 Climate Risk Map")
    m = folium.Map(location=[23.6850, 90.3563], zoom_start=7, tiles='CartoDB positron')
    for _, row in filtered_df.iterrows():
        color = '#d63031' if row['climate_risk'] >= 8 else '#fdcb6e' if row['climate_risk'] >= 5 else '#00b894'
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=row['climate_risk'] * 2,
            popup=f"District: {row['district']}<br>Risk: {row['climate_risk']}/10",
            color=color, fill=True, fill_opacity=0.7
        ).add_to(m)
    st_folium(m, width=700, height=450)

with col_right:
    st.subheader("📚 Educational Analysis")
    st.bar_chart(filtered_df.set_index("district")["literacy_rate"])
    st.markdown("**School Access Index**")
    st.bar_chart(filtered_df.set_index("district")["school_access_index"])

# ৬. ডেটা টেবিল
st.divider()
st.subheader("📋 Dataset")
st.dataframe(filtered_df, use_container_width=True)
