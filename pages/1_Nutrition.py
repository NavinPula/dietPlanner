import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title="Nutrition Plan", page_icon="🥗", layout="wide")

# 🌿 Hide the default sidebar nav
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
st.title("🍎 AI Diet Suggestions")
st.markdown("Here are your **AI-generated weekly diet plans** based on your BMI 👇")

if "bmi" not in st.session_state:
    st.warning("⚠️ Please calculate your BMI from the Home page first!")
    st.page_link("Home.py", label="⬅️ Go to Home Page")
    st.stop()

bmi = st.session_state.bmi
category = st.session_state.category

st.info(f"Your BMI: **{bmi}** | Category: **{category}**")

# Dynamic Nutrient Ratios based on category
if category == "Underweight":
    nutrients = [55, 30, 15]  # More carbs, moderate protein, moderate fat
    weekly_plan = {
        "Mon": "🥣 Oats with milk | 🍛 Paneer rice | 🍗 Chicken curry",
        "Tue": "🍳 Eggs | 🍚 Rice, dal | 🍵 Soup + nuts",
        "Wed": "🥛 Smoothie | 🥘 Pasta + veggies | 🥗 Paneer curry",
        "Thu": "🍌 Fruit bowl | 🍛 Rice + lentils | 🥗 Salad + soup",
        "Fri": "🥣 Muesli | 🥘 Potato curry | 🍲 Rice + dal",
        "Sat": "🥑 Avocado toast | 🍛 Chicken + rice | 🥗 Roti + veg",
        "Sun": "🍎 Fruits | 🥘 Paneer pulao | 🍵 Milk + nuts"
    }

elif category == "Normal":
    nutrients = [50, 30, 20]
    weekly_plan = {
        "Mon": "🥣 Oats + Banana | 🍛 Brown rice + dal | 🍎 Soup & salad",
        "Tue": "🍳 Eggs & toast | 🍚 Quinoa + veggies | 🍵 Soup",
        "Wed": "🥛 Smoothie | 🥘 Grilled chicken | 🥬 Veg salad",
        "Thu": "🍌 Fruit bowl | 🍛 Rice + lentils | 🥗 Salad & soup",
        "Fri": "🥣 Muesli | 🥘 Grilled paneer | 🍲 Veg soup",
        "Sat": "🥑 Avocado toast | 🍛 Chicken curry | 🥗 Steamed veggies",
        "Sun": "🍎 Fruit bowl | 🥘 Brown rice + dal | 🍵 Soup & salad"
    }

elif category == "Overweight":
    nutrients = [45, 35, 20]  # Balanced protein, moderate fat
    weekly_plan = {
        "Mon": "🥣 Oats + berries | 🍛 Grilled tofu | 🥗 Soup + salad",
        "Tue": "🍳 Egg whites | 🍚 Quinoa + veggies | 🍵 Soup",
        "Wed": "🥛 Protein shake | 🥘 Grilled fish | 🥬 Veg salad",
        "Thu": "🍌 Fruit bowl | 🍛 Lentil soup | 🥗 Salad + soup",
        "Fri": "🥣 Muesli | 🥘 Paneer salad | 🍲 Veg soup",
        "Sat": "🥑 Avocado toast | 🍛 Chicken breast | 🥗 Steamed veggies",
        "Sun": "🍎 Fruit bowl | 🥘 Brown rice + dal | 🍵 Soup & salad"
    }

else:  # Obese
    nutrients = [35, 40, 25]  # Lower carbs, higher protein
    weekly_plan = {
        "Mon": "🥣 Oats + berries | 🍛 Grilled tofu | 🥗 Soup + salad",
        "Tue": "🍳 Egg whites | 🍚 Quinoa + veggies | 🍵 Soup",
        "Wed": "🥛 Protein shake | 🥘 Grilled fish | 🥬 Veg salad",
        "Thu": "🍌 Fruit bowl | 🍛 Lentil soup | 🥗 Salad + soup",
        "Fri": "🥣 Muesli | 🥘 Paneer salad | 🍲 Veg soup",
        "Sat": "🥑 Avocado toast | 🍛 Chicken breast | 🥗 Steamed veggies",
        "Sun": "🍎 Fruit bowl | 🥘 Brown rice + dal | 🍵 Soup & salad"
    }

    nutrients = [40, 35, 25]  # higher protein, lower carbs
    weekly_plan = {
        "Mon": "🥣 Oats + berries | 🍛 Grilled tofu | 🥗 Dinner: Soup + salad",
        "Tue": "🍳 Eggs white | 🍚 Quinoa + veggies | 🍵 Dinner: Soup",
        "Wed": "🥛 Protein shake | 🥘 Grilled fish | 🥬 Dinner: Veg salad",
        "Thu": "🍌 Fruit bowl | 🍛 Lentil soup | 🥗 Dinner: Salad + soup",
        "Fri": "🥣 Muesli | 🥘 Paneer salad | 🍲 Dinner: Veg soup",
        "Sat": "🥑 Avocado toast | 🍛 Chicken breast | 🥗 Dinner: Steamed veggies",
        "Sun": "🍎 Fruit bowl | 🥘 Brown rice + dal | 🍵 Dinner: Soup & salad"
    }

# Nutrient Breakdown & Weekly Planner
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 🍽️ Daily Nutrient Breakdown")
    fig = go.Figure(data=[go.Pie(
        labels=['Carbs', 'Protein', 'Fats'],
        values=nutrients,
        hole=.6,
        marker=dict(colors=['#36a2eb', '#ff6384', '#ffce56'])
    )])
    fig.update_layout(
        showlegend=True,
        annotations=[dict(text=f"{category}", x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("### 📅 Weekly Planner")
    days = list(weekly_plan.keys())
    selected_day = st.radio("Select Day", days, horizontal=True)
    st.write(weekly_plan[selected_day])

st.divider()
st.page_link("Home.py", label="⬅️ Back to Home")
