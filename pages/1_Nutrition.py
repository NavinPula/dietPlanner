import streamlit as st
import plotly.graph_objects as go
import pandas as pd
from pathlib import Path
import base64
import json

st.set_page_config(page_title="Nutrition", page_icon="📊", layout="wide")

# ✅ Load CSS if available
try:
    st.markdown(f"<style>{open('assets/styles.css').read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# --- HEADER ---
st.markdown("<h1 style='color:#3b3b98;'>🥗 Nutrition Overview</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#444;'>Weekly summary and nutraceutical recommendations</p>", unsafe_allow_html=True)

# --- WEEKLY CALORIES CHART ---
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
calories = [1800, 1700, 1900, 1600, 1750, 2000, 1800]
df = pd.DataFrame({"day": days, "calories": calories})

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<h3 style="color:#3b3b98;">Calories — Weekly Trend</h3>', unsafe_allow_html=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['day'], y=df['calories'], marker_color='#5e60ce'
    ))

    # <-- UPDATED: make x and y axis labels/ticks black -->
    fig.update_layout(
        yaxis_title='Calories (kcal)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='black', size=14),
        xaxis=dict(showgrid=False, tickfont=dict(color='black'), title_font=dict(color='black')),
        yaxis=dict(showgrid=True, gridcolor='#E9ECEF', tickfont=dict(color='black'), title_font=dict(color='black'))
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown('<h3 style="color:#3b3b98;">Summary</h3>', unsafe_allow_html=True)

    avg = int(df['calories'].mean())
    highest = max(df['calories'])
    lowest = min(df['calories'])

    # Custom styled metrics
    st.markdown(f"""
        <div style="color:#3b3b98; font-weight:bold; font-size:18px;">Average Calories</div>
        <div style="color:#000; font-size:22px; margin-bottom:10px;">{avg} kcal</div>

        <div style="color:#3b3b98; font-weight:bold; font-size:18px;">Highest</div>
        <div style="color:#000; font-size:22px; margin-bottom:10px;">{highest} kcal</div>

        <div style="color:#3b3b98; font-weight:bold; font-size:18px;">Lowest</div>
        <div style="color:#000; font-size:22px; margin-bottom:15px;">{lowest} kcal</div>
    """, unsafe_allow_html=True)

    st.markdown(
        "<div style='background-color:#eaf2ff; color:#3b3b98; border-radius:10px; padding:10px;'>✅ "
        "Keep your weekly average within your target for best results.</div>",
        unsafe_allow_html=True
    )


# ✅ Image loader
def load_image(image_path):
    path = Path(image_path)
    if path.exists():
        with open(path, "rb") as f:
            data = f.read()
        encoded = base64.b64encode(data).decode()
        return f"data:image/webp;base64,{encoded}"
    else:
        return "https://via.placeholder.com/300x200?text=Image+Not+Found"

# --- NUTRACEUTICAL SECTION ---
st.markdown('<h2 style="margin-top:40px; color:#3b3b98;">💊 Nutraceutical Recommendations</h2>', unsafe_allow_html=True)

# ✅ Load JSON Data
data_path = Path("assets/data/nutrition_data.json")
if data_path.exists():
    with open(data_path, "r", encoding="utf-8") as f:
        benefits = json.load(f)
else:
    st.error("⚠️ Nutrition data file not found!")
    benefits = []

# ✅ Card Style - Uniform Height (UPDATED: full image + neat card + key benefits inside card)
st.markdown("""
<style>
.card {
    background: #fff;
    border-radius: 16px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.07);
    padding: 16px;
    margin-bottom: 20px;
    text-align: left;
    transition: all 0.22s ease-in-out;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    height: 400px;       
}
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 14px 40px rgba(0,0,0,0.12);
}
.card img {
    width: 100%;
    height: 260px;        
    object-fit: cover;    
    border-radius: 12px;
    margin-bottom: 12px;
}
.card-title {
    font-size: 18px;
    font-weight: 700;
    color: #2c2c54;
    margin-bottom: 8px;
    min-height: 48px;
    display: flex;
    align-items: center;
}
.card-desc {
    font-size: 14px;
    color: #444;
    line-height: 1.5;
    margin-bottom: 12px;
    /* equal lines for all cards */
    display: -webkit-box;
    -webkit-line-clamp: 4;
    -webkit-box-orient: vertical;
    overflow: hidden; /* ensure equal height area */
}
.key-benefits-box {
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid #eef2ff;
}
.key-benefits-list {
    margin: 8px 0 0 18px;
    color: #333;
}
.key-benefits-list li {
    margin-bottom: 8px;
    line-height: 1.45;
    font-size: 13.5px;
}
</style>
""", unsafe_allow_html=True)

# ✅ Display Cards (UPDATED: render keyBenefit as numbered list inside each card)
for i in range(0, len(benefits), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(benefits):
            item = benefits[i + j]
            img_src = load_image(item["image"])
            # build ordered list HTML for key benefits
            kb_html = ""
            if isinstance(item.get("keyBenefit"), list):
                kb_html = "<ol class='key-benefits-list'>"
                for b in item["keyBenefit"]:
                    kb_html += f"<li>{b}</li>"
                kb_html += "</ol>"
            else:
                # if stored as text, keep line breaks
                kb_html = f"<div class='key-benefits-list'>{item.get('keyBenefit','')}</div>"

            with cols[j]:
                st.markdown(f"""
                    <div class="card">
                        <img src="{img_src}" alt="{item['title']}">
                        <div class="card-title">{item['title']}</div>
                        <div class="card-desc">{item['description']}</div>
                    </div>
                """, unsafe_allow_html=True)

                with st.expander("✨ Key Benefits"):
                    for idx, b in enumerate(item["keyBenefit"], 1):
                        st.markdown(f"**{idx}.** {b}")
