import pandas as pd
import folium
from branca.element import Template, MacroElement

# ১. ডেটা লোড করা (নিশ্চিত করুন climate_data.csv ফাইলটি একই ফোল্ডারে আছে)
try:
    df = pd.read_csv("climate_data.csv")
except:
    print("CSV ফাইলটি পাওয়া যায়নি! দয়া করে ফাইলটি তৈরি করুন।")

# ২. ম্যাপ সেটআপ (বাংলাদেশ সেন্টার)
m = folium.Map(location=[23.6850, 90.3563], zoom_start=7, tiles='CartoDB positron')

# ৩. সার্কেল মার্কার যোগ করা
for index, row in df.iterrows():
    risk = row['climate_risk']
    
    # রিস্ক অনুযায়ী রঙ (High=Red, Medium=Orange, Low=Green)
    color = '#d63031' if risk >= 8 else '#e17055' if risk >= 5 else '#00b894'
    
    # সুন্দর পপআপ ডিজাইন
    popup_content = f"""
    <div style="font-family: sans-serif; width: 160px;">
        <h4 style="margin-bottom:5px;">{row['district']}</h4>
        <hr style="margin:5px 0;">
        <b>Risk Score:</b> {risk}/10<br>
        <b>Schools:</b> {row['number_of_schools']}<br>
        <b>Access:</b> {row['school_access_index']}%
    </div>
    """
    
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=risk * 2.5, # রিস্ক অনুযায়ী সার্কেলের সাইজ
        popup=folium.Popup(popup_content, max_width=200),
        tooltip=f"{row['district']} (Risk: {risk})",
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        weight=1.5
    ).add_to(m)

# ৪. লেজেন্ড (Legend) যোগ করার জন্য HTML কোড
legend_html = '''
{% macro html(this, kwargs) %}
<div style="
    position: fixed; bottom: 30px; left: 30px; width: 150px; height: 100px; 
    background-color: white; border:2px solid grey; z-index:9999; font-size:12px;
    padding: 10px; border-radius: 8px; font-family: Arial; opacity: 0.9;
    ">
    <b>Risk Indicators</b><br>
    <p><i style="background:#d63031; width:10px; height:10px; display:inline-block; border-radius:50%"></i> High Risk (8+)</p>
    <p><i style="background:#e17055; width:10px; height:10px; display:inline-block; border-radius:50%"></i> Medium Risk (5-7)</p>
    <p><i style="background:#00b894; width:10px; height:10px; display:inline-block; border-radius:50%"></i> Low Risk (1-4)</p>
</div>
{% endmacro %}
'''

# লেজেন্ড ম্যাপে যুক্ত করা
macro = MacroElement()
macro._template = Template(legend_html)
m.get_root().add_child(macro)

# ৫. ম্যাপ সেভ করা
m.save("final_bangladesh_risk_map.html")
print("অভিনন্দন! আপনার ম্যাপটি 'final_bangladesh_risk_map.html' নামে সেভ হয়েছে।")
