import pandas as pd
import folium
import altair as alt
import json
import os

# ১. ফোল্ডার তৈরি
if not os.path.exists('maps'):
    os.makedirs('maps')

# ২. ডাটা এবং কোঅর্ডিনেটস
data = {
    'district': ['Sunamganj', 'Kurigram', 'Gaibandha', 'Jamalpur', 'Sirajganj', 'Satkhira', 'Bhola', 'Barisal', 'Faridpur', 'Dhaka'],
    'lat': [25.0715, 25.8072, 25.3297, 24.9200, 24.4534, 22.7131, 22.6859, 22.7010, 23.6071, 23.8103],
    'lon': [91.3992, 89.6295, 89.5430, 89.9400, 89.7042, 89.0723, 90.6455, 90.3535, 89.8429, 90.4125],
    'flood_risk_level': [9, 8, 8, 7, 9, 6, 7, 6, 5, 3],
    'population_exposed': [850000, 720000, 680000, 600000, 910000, 540000, 620000, 580000, 470000, 1000000]
}
df = pd.DataFrame(data)

# ৩. ম্যাপ তৈরি
m = folium.Map(location=[23.6850, 90.3563], zoom_start=7, tiles='CartoDB positron')

# ৪. প্রতিটি জেলার জন্য চার্ট তৈরি ও মার্কার যোগ করা
for i, row in df.iterrows():
    # চার্টের জন্য ছোট ডাটাসেট
    chart_data = pd.DataFrame({
        'Category': ['Risk Level', 'Pop (x100k)'],
        'Value': [row['flood_risk_level'], row['population_exposed']/100000]
    })

    # Altair দিয়ে বার চার্ট তৈরি
    chart = alt.Chart(chart_data).mark_bar().encode(
        x='Category',
        y='Value',
        color=alt.value('#d63031' if row['flood_risk_level'] >= 8 else '#0984e3')
    ).properties(width=150, height=100, title=f"Stats: {row['district']}")

    # চার্টটিকে পপআপে রূপান্তর
    vega_chart = folium.features.VegaLite(chart, width='100%', height='100%')
    popup = folium.Popup(max_width=250)
    vega_chart.add_to(popup)

    # সার্কেল মার্কার যোগ
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=row['flood_risk_level'] * 2.5,
        popup=popup,
        tooltip=f"Click for {row['district']} Chart",
        color='#2d3436',
        fill=True,
        fill_color='#d63031' if row['flood_risk_level'] >= 8 else '#0984e3',
        fill_opacity=0.7
    ).add_to(m)

# ৫. ম্যাপ সেভ
m.save("maps/flood_chart_map.html")
print("ম্যাপ তৈরি হয়েছে! যেকোনো সার্কেলে ক্লিক করে চার্ট দেখুন।")
