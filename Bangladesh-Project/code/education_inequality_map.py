import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import io

# ১. পেজ সেটআপ
st.set_page_config(page_title="BD Education Dashboard", layout="wide")
st.title("🎓 Education & Inequality Dashboard - Bangladesh")

# ২. ডেটা লোড (আপনার দেওয়া CSV ডেটা)
csv_data = """district,lat,lon,literacy_rate,enrollment_rate,dropout_rate,average_school_years
Dhaka,23.8103,90.4125,85,92,5,10
Rajshahi,24.3636,88.6241,78,88,8,9
Khulna,22.8456,89.5403,80,89,7,9
Barisal,22.7010,90.3535,75,85,10,8
Sylhet,24.8949,91.8687,72,82,12,8
Rangpur,25.7439,89.2752,74,84,11,8
Chattogram,22.3569,91.7832,79,87,9,9
Mymensingh,24.7471,90.4203,73,83,11,8
Bhola,22.6859,90.6455,68,80,14,7
Satkhira,22.7131,89.0723,70,81,13,7"""

df = pd.read_csv(io.StringIO(csv_data))

# ৩. সাইডবার ফিল্টার
st.sidebar.header("Filter Options")
districts = st.sidebar.multiselect("Select Districts", options=df['district'].unique(), default=df['district'].unique())
filtered_df = df[df['district'].isin(districts)]

# ৪. ড্যাশবোর্ডের উপরের অংশ (Metrics)
col1, col2, col3 = st.columns(3)
col1.metric("Avg Literacy", f"{filtered_df['literacy_rate'].mean():.1f}%")
col2.metric("Avg Enrollment", f"{filtered_df['enrollment_rate'].mean():.1f}%")
col3.metric("Avg Dropout", f"{filtered_df['dropout_rate'].mean():.1f}%", delta_color="inverse")

# ৫. ম্যাপ এবং চার্ট পাশাপাশি (Layout)
left_col, right_col = st.columns([1.2, 1])

with left_col:
    st.subheader("📍 Interactive Education Map")
    # Folium ম্যাপ তৈরি
    m = folium.Map(location=[23.6850, 90.3563], zoom_start=7, tiles='CartoDB positron')
    
    for _, row in filtered_df.iterrows():
        # ড্রপআউট বেশি হলে লাল রঙ
        color = '#d63031' if row['dropout_rate'] >= 11 else '#20bf6b'
        
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=row['literacy_rate'] / 4,
            popup=f"District: {row['district']}<br>Dropout: {row['dropout_rate']}%",
            tooltip=row['district'],
            color=color,
            fill=True,
            fill_opacity=0.7
        ).add_to(m)
    
    # Streamlit-এ ম্যাপ প্রদর্শন
    st_folium(m, width=700, height=500)

with right_col:
    st.subheader("📊 Literacy vs Dropout")
    st.bar_chart(filtered_df.set_index("district")[["literacy_rate", "dropout_rate"]])
    
    st.subheader("📝 Data Table")
    st.dataframe(filtered_df[['district', 'literacy_rate', 'dropout_rate']], use_container_width=True)

# ৬. রান করার নিয়ম
# টার্মিনালে লিখুন: streamlit run your_file_name.py
