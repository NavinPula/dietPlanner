import streamlit as st

st.set_page_config(page_title="AI Diet Planner", page_icon="🥗", layout="wide")

# 🌿 Hide the default sidebar navigation
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
        [data-testid="stSidebarNavItems"] {display: none;}
        [data-testid="stSidebarNavSeparator"] {display: none;}
        [data-testid="stSidebarHeader"] {display: none;}
        [data-testid="stSidebar"] {
            background-color: #0E1117;
            padding-top: 30px;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("""
        <h2 style='text-align:center; color:#4CAF50; margin-bottom:10px;'>
            🤖 AI Diet Planner
        </h2>
        <hr style='border: 1px solid #4CAF50; margin:10px 0;'>
    """, unsafe_allow_html=True)

    if st.button("🏠 Home", use_container_width=True):
        st.switch_page("Home.py")

    if st.button("🥗 Nutrition Plan", use_container_width=True):
        st.switch_page("pages/1_Nutrition.py")

# ---------------- MAIN CONTENT ----------------
st.title("🏠 Welcome to AI Diet Planner")
st.markdown("""
### Your Smart Nutrition Companion 🍎  
Get your personalized **BMI** and weekly **nutrition plan** instantly.  
Simply enter your details below to calculate your BMI and discover your diet plan.
""")

st.divider()

# BMI Calculator
st.subheader("🧮 BMI Calculator")
col1, col2 = st.columns(2)

with col1:
    height = st.number_input("Enter your height (in cm):", min_value=50.0, max_value=250.0, step=0.5)
with col2:
    weight = st.number_input("Enter your weight (in kg):", min_value=10.0, max_value=300.0, step=0.5)

if st.button("✨ Calculate BMI"):
    if height > 0:
        bmi = round(weight / ((height / 100) ** 2), 2)
        st.success(f"✅ Your BMI is **{bmi}**")

        if bmi < 18.5:
            category = "Underweight"
        elif 18.5 <= bmi < 24.9:
            category = "Normal"
        elif 25 <= bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"

        st.info(f"**BMI Category:** {category}")
        st.session_state.bmi = bmi
        st.session_state.category = category
        st.session_state.show_nutrition = True

        st.markdown("---")
        st.write("👉 Click below to view your weekly nutrition plan:")
        st.page_link("pages/1_Nutrition.py", label="➡️ View Nutrition Plan")
    else:
        st.warning("⚠️ Please enter valid height and weight.")
