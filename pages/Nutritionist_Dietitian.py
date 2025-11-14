import streamlit as st

# Page setup
st.set_page_config(page_title="Nutritionist / Dietitian", page_icon="👩‍⚕️", layout="wide")

# Load custom CSS
try:
    st.markdown(f"<style>{open('assets/styles.css').read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# Page Header
st.markdown('<h1 class="h1">👩‍⚕️ Nutritionist / Dietitian Experts</h1>', unsafe_allow_html=True)
st.markdown('<div class="text-muted" style="margin-bottom: 32px;">Find trusted dietitians and nutrition experts near you to support your health goals.</div>', unsafe_allow_html=True)

# Data for cards
doctors = [
    {
        "name": "Dr. Aniruddh Kurulkar",
        "specialization": "Sports & Exercise Nutrition",
        "mobile": "9975316075",
        "address": "Tale Hipparga Marbe Vasti, Padmavati Nagar, Solapur - 413002"
    },
    {
        "name": "Dr. Swapna Wale",
        "specialization": "Medical Nutrition",
        "mobile": "9834989407",
        "address": "Rohidas Nagar, Ghatsil Road, Tuljapur - 413601"
    },
    {
        "name": "Dr. Shweta Adakul",
        "specialization": "Pediatrics Dietitian",
        "mobile": "7385418325",
        "address": "Flat No. 502, 5th Floor, Hayaticon Apartment, Mohite Nagar, near Raghoji Hospital, Aasara, Solapur - 413003"
    }
]

# Create 3-column layout for cards
cols = st.columns(3)
for i, doc in enumerate(doctors):
    with cols[i % 3]:
        st.markdown(f"""
        <div style="
            background-color: #ffffff;
            border-radius: 12px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            padding: 20px;
            margin-bottom: 24px;
            height: 250px;
            transition: transform 0.2s ease-in-out;
        " onmouseover="this.style.transform='scale(1.03)';" onmouseout="this.style.transform='scale(1)';">
            <h3 style="color: #4A90E2; margin-bottom: 8px;">{doc['name']}</h3>
            <p style="font-size:16px; color:#0072BB; font-weight:500; margin:0 0 8px 0;">{doc['specialization']}</p>
            <hr style="border:0.5px solid #E0E0E0; margin:10px 0;">
            <p style="margin:6px 0; font-size:15px; color:#000000;"><b>📞 Mobile:</b> {doc['mobile']}</p>
            <p style="margin:6px 0; font-size:15px; color:#000000;"><b>📍 Address:</b> {doc['address']}</p>
        </div>
        """, unsafe_allow_html=True)

# Back to Home Button (Streamlit button instead of link)
st.markdown('<div style="margin-top:40px; text-align:center;">', unsafe_allow_html=True)
if st.button("🏠 Go to Home", use_container_width=False, key="go_home_btn"):
    st.switch_page("Home.py")
st.markdown('</div>', unsafe_allow_html=True)