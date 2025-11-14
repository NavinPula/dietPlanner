import streamlit as st
import plotly.graph_objects as go
from math import isfinite

# ---------------------------------------------------------
# 🥗 Page Configuration
# ---------------------------------------------------------
st.set_page_config(page_title="Meal Plan", page_icon="🥗", layout="wide")

# Load CSS
try:
    st.markdown(f"<style>{open('assets/styles.css').read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# ---------------------------------------------------------
# 🧭 Page Header
# ---------------------------------------------------------
st.markdown('<h1 class="h1">Meal Plan</h1>', unsafe_allow_html=True)
st.markdown('<div class="text-muted" style="margin-bottom: 32px;">AI suggestions and your daily & weekly view</div>', unsafe_allow_html=True)

# --- Read values from Home (height, weight, age, category, bmi_percent) ---
height_cm = st.session_state.get("height_cm")   # expected in cm
weight_kg = st.session_state.get("weight_kg")   # expected in kg
age = st.session_state.get("age")
# user may have computed bmi & category on Home; prefer those if present
bmi_home = st.session_state.get("bmi")
category_home = st.session_state.get("category")
bmi_percent_home = st.session_state.get("bmi_percent")  # optional

# Compute BMI locally if Home didn't provide it and height/weight available
bmi = None
if bmi_home:
    bmi = float(bmi_home)
elif height_cm and weight_kg:
    try:
        h_m = float(height_cm) / 100.0
        bmi = float(weight_kg) / (h_m * h_m) if h_m > 0 else None
    except Exception:
        bmi = None

# Determine BMI category (fallback if not provided)
def bmi_category_from_value(bmi_val):
    if bmi_val is None or not isfinite(bmi_val):
        return "Unknown"
    if bmi_val < 18.5:
        return "Underweight"
    if 18.5 <= bmi_val < 25:
        return "Normal"
    if 25 <= bmi_val < 30:
        return "Overweight"
    return "Obese"

bmi_category = category_home or bmi_category_from_value(bmi)

# Compute BMI percentage (relative to ideal BMI 22)
bmi_percent = None
if bmi_percent_home:
    try:
        bmi_percent = float(bmi_percent_home)
    except Exception:
        bmi_percent = None
elif bmi:
    target = 22.0
    bmi_percent = round((bmi / target) * 100, 1)

# Guard: ensure BMI exists (previous behavior kept)
if "bmi" not in st.session_state and bmi is None:
    st.warning("⚠️ Please calculate BMI on the Home page first (height & weight required).")
    st.markdown('<div style="margin-top: 20px;"></div>', unsafe_allow_html=True)
    if st.button("🏠 Go to Home", use_container_width=False, key="go_home_btn"):
        try:
            st.switch_page("Home.py")
        except Exception:
            pass
    st.stop()

# ---------------------------------------------------------
# 🧾 Initialize weekly meals storage & selected day
# ---------------------------------------------------------
if 'weekly_meals' not in st.session_state:
    st.session_state['weekly_meals'] = {
        'Mon': {'breakfast': '', 'lunch': '', 'dinner': ''},
        'Tue': {'breakfast': '', 'lunch': '', 'dinner': ''},
        'Wed': {'breakfast': '', 'lunch': '', 'dinner': ''},
        'Thu': {'breakfast': '', 'lunch': '', 'dinner': ''},
        'Fri': {'breakfast': '', 'lunch': '', 'dinner': ''},
        'Sat': {'breakfast': '', 'lunch': '', 'dinner': ''},
        'Sun': {'breakfast': '', 'lunch': '', 'dinner': ''}
    }

if 'selected_day' not in st.session_state:
    st.session_state['selected_day'] = 'Mon'

# ---------------------------------------------------------
# 📋 Layout: Left (Suggestions, Chart) | Right (Weekly Planner)
# ---------------------------------------------------------
left, right = st.columns([2, 1])

# ==============================
# LEFT SIDE CONTENT
# ==============================
with left:
    # ---- AI Diet Suggestions ----
    st.markdown('<h2 class="h2">AI Diet Suggestions</h2>', unsafe_allow_html=True)
    st.markdown(f'<div class="text-muted" style="margin-bottom: 8px;">Detected BMI: <b>{bmi:.1f}</b> — Category: <b>{bmi_category}</b></div>', unsafe_allow_html=True)
    if bmi_percent is not None:
        pct = bmi_percent
        st.markdown(f'<div class="text-muted" style="margin-bottom: 12px;">BMI % (vs ideal 22): <b>{pct}%</b></div>', unsafe_allow_html=True)
        # show progress visually (clamped)
        prog = min(max(int(round(pct)), 0), 200)
        st.progress(min(prog, 100) / 100.0)

    # Suggestions and default meals adapt to BMI/category and age
    if bmi_category in ["Underweight"]:
        suggestions = [
            ("🥜", "Add nuts & seeds", "Calorie-dense healthy fats"),
            ("🥛", "Include milk & shakes", "Extra protein and calories"),
            ("🍚", "Add complex carbs", "Support weight gain")
        ]
        default_meals = {
            'Mon': {'breakfast': 'Oats + milk + nuts', 'lunch': 'Rice + dal + chicken', 'dinner': 'Paneer curry + rice'},
            'Tue': {'breakfast': 'Banana shake + oats', 'lunch': 'Chapati + dal + potato', 'dinner': 'Egg curry + rice'},
            'Wed': {'breakfast': 'Peanut butter toast', 'lunch': 'Paneer biryani', 'dinner': 'Chicken + rice'},
            'Thu': {'breakfast': 'Smoothie + oats', 'lunch': 'Rice + fish', 'dinner': 'Roti + dal + ghee'},
            'Fri': {'breakfast': 'Muesli + milk', 'lunch': 'Rice + chicken', 'dinner': 'Paneer + roti'},
            'Sat': {'breakfast': 'Boiled eggs + toast', 'lunch': 'Chicken breast + rice', 'dinner': 'Curd rice'},
            'Sun': {'breakfast': 'Pancakes + eggs', 'lunch': 'Rice + dal + ghee', 'dinner': 'Veg pulao'}
        }
    elif bmi_category in ["Overweight", "Obese"]:
        suggestions = [
            ("🥗", "Increase veggies", "Low-calorie, high-fiber foods"),
            ("🍗", "Prioritize lean protein", "Improves satiety"),
            ("🚶", "Add daily activity", "Boost energy expenditure")
        ]
        default_meals = {
            'Mon': {'breakfast': 'Greek yogurt + berries', 'lunch': 'Grilled chicken salad', 'dinner': 'Steamed veggies + soup'},
            'Tue': {'breakfast': 'Smoothie (green)', 'lunch': 'Quinoa bowl', 'dinner': 'Grilled fish + salad'},
            'Wed': {'breakfast': 'Oats + fruit', 'lunch': 'Lentil salad', 'dinner': 'Veg stir-fry'},
            'Thu': {'breakfast': 'Fruit bowl', 'lunch': 'Chicken + salad', 'dinner': 'Soup'},
            'Fri': {'breakfast': 'Egg white omelette', 'lunch': 'Paneer salad', 'dinner': 'Grilled veggies'},
            'Sat': {'breakfast': 'Protein smoothie', 'lunch': 'Fish + greens', 'dinner': 'Salad'},
            'Sun': {'breakfast': 'Muesli', 'lunch': 'Brown rice + dal + salad', 'dinner': 'Soup'}
        }
    elif bmi_category == "Normal":
        suggestions = [
            ("🍎", "Balanced macros", "Maintain mixture of carbs/protein/fats"),
            ("🏃", "Stay active", "Keep consistent exercise routine"),
            ("🍳", "Include protein", "Support muscle mass")
        ]
        default_meals = {
            'Mon': {'breakfast': 'Oats + fruits', 'lunch': 'Rice + dal + veg', 'dinner': 'Soup + salad'},
            'Tue': {'breakfast': 'Eggs & toast', 'lunch': 'Grilled chicken + rice', 'dinner': 'Veg curry'},
            'Wed': {'breakfast': 'Smoothie bowl', 'lunch': 'Paneer + chapati', 'dinner': 'Grilled fish + salad'},
            'Thu': {'breakfast': 'Muesli', 'lunch': 'Quinoa bowl', 'dinner': 'Stir-fry veggies'},
            'Fri': {'breakfast': 'Oats + milk', 'lunch': 'Dal + rice', 'dinner': 'Chicken soup'},
            'Sat': {'breakfast': 'Avocado toast', 'lunch': 'Brown rice + salad', 'dinner': 'Paneer + veggies'},
            'Sun': {'breakfast': 'Fruit bowl', 'lunch': 'Rice + dal', 'dinner': 'Soup & salad'}
        }
    else:
        suggestions = [
            ("🍽️", "Follow balanced plan", "Adjust to your preferences"),
            ("💧", "Hydrate", "Drink water regularly")
        ]
        default_meals = {d: {'breakfast': '', 'lunch': '', 'dinner': ''} for d in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']}

    # Display suggestion boxes
    st.markdown('<div class="card-grid">', unsafe_allow_html=True)
    for icon, title, sub in suggestions:
        st.markdown(
            f"""
            <div class="suggestion-box">
                <div class="suggestion-icon">{icon}</div>
                <div class="suggestion-title">{title}</div>
                <div class="suggestion-subtitle">{sub}</div>
            </div>
            """, unsafe_allow_html=True
        )
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom: 24px;"></div>', unsafe_allow_html=True)

    # ---- Daily Nutrient Breakdown ----
    st.markdown('<h2 class="h2">Daily Nutrient Breakdown</h2>', unsafe_allow_html=True)

    # Sample nutrition data (customize as needed)
    calories = 589
    carbs = 76
    protein = 27
    fats = 15

    # Calculate percentages
    total_macros = carbs + protein + fats
    carbs_pct = int((carbs / total_macros) * 100) if total_macros else 0
    protein_pct = int((protein / total_macros) * 100) if total_macros else 0
    fats_pct = int((fats / total_macros) * 100) if total_macros else 0

    fig = go.Figure(
        data=[go.Pie(
            labels=['Carbs', 'Protein', 'Fats'],
            values=[carbs_pct, protein_pct, fats_pct],
            hole=.6,
            marker=dict(colors=['#50C878', '#4A90E2', '#FFD700']),
            textinfo='label+percent',
            textposition='outside'
        )]
    )
    fig.update_layout(
        margin=dict(t=20, b=20, l=20, r=20),
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.1),
        annotations=[dict(text=f"{calories}<br>kcal", x=0.5, y=0.5, font=dict(size=24, color="#667eea"), showarrow=False)]
    )
    st.plotly_chart(fig, use_container_width=True)

    # Nutrition info below chart
    st.markdown(f"""
    <div style="display:flex; gap:24px; margin-top:20px; justify-content:center; flex-wrap: wrap;">
        <div style="text-align: center;">
            <div style="color: #FFD700; font-size: 20px; font-weight: 700;">Calories</div>
            <div style="color: #667eea; font-size: 18px; font-weight: 700; margin-top: 4px;">{calories} kcal</div>
        </div>
        <div style="text-align: center;">
            <div style="color: #4A90E2; font-size: 20px; font-weight: 700;">Protein</div>
            <div style="color: #667eea; font-size: 18px; font-weight: 700; margin-top: 4px;">{protein}g</div>
        </div>
        <div style="text-align: center;">
            <div style="color: #50C878; font-size: 20px; font-weight: 700;">Carbs</div>
            <div style="color: #667eea; font-size: 18px; font-weight: 700; margin-top: 4px;">{carbs}g</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# RIGHT SIDE CONTENT
# ==============================
with right:
    st.markdown('<h2 class="h2">Weekly Planner</h2>', unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom:16px;"></div>', unsafe_allow_html=True)

    # Use default_meals chosen above if user hasn't added meals
    user_has_added_meals = st.session_state.get('meals_added', False)
    if not user_has_added_meals:
        for day in st.session_state['weekly_meals']:
            for meal_type in ['breakfast', 'lunch', 'dinner']:
                if not st.session_state['weekly_meals'][day].get(meal_type):
                    st.session_state['weekly_meals'][day][meal_type] = default_meals.get(day, {}).get(meal_type, '')

    # Day selection
    days_full = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    current_index = days_full.index(st.session_state.get('selected_day','Mon'))
    selected_day = st.radio("Select Day", days_full, horizontal=True, index=current_index, key="day_selector")
    st.session_state['selected_day'] = selected_day

    # Show BMI & Category at top of planner
    st.markdown(f"<div style='margin-top:8px; font-size:14px; color:#333;'>BMI: <b>{bmi:.1f}</b> &nbsp; | &nbsp; Category: <b>{bmi_category}</b></div>", unsafe_allow_html=True)
    if bmi_percent is not None:
        st.markdown(f"<div style='font-size:13px; color:#666;'>BMI % vs ideal: <b>{bmi_percent}%</b></div>", unsafe_allow_html=True)

    # Display meals for selected day
    day_meals = st.session_state['weekly_meals'].get(selected_day, {'breakfast':'','lunch':'','dinner':''})
    st.markdown('<div style="margin-top: 12px;"></div>', unsafe_allow_html=True)

    if day_meals.get('breakfast'):
        st.markdown(f"""
        <div style="margin-bottom: 12px;">
            <div style="font-weight: 600; color: #667eea; margin-bottom: 6px;">🍳 Breakfast</div>
            <div class="hint">{day_meals['breakfast']}</div>
        </div>
        """, unsafe_allow_html=True)

    if day_meals.get('lunch'):
        st.markdown(f"""
        <div style="margin-bottom: 12px;">
            <div style="font-weight: 600; color: #667eea; margin-bottom: 6px;">🍽️ Lunch</div>
            <div class="hint">{day_meals['lunch']}</div>
        </div>
        """, unsafe_allow_html=True)

    if day_meals.get('dinner'):
        st.markdown(f"""
        <div style="margin-bottom: 12px;">
            <div style="font-weight: 600; color: #667eea; margin-bottom: 6px;">🌙 Dinner</div>
            <div class="hint">{day_meals['dinner']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Quick Tips based on selected day (same as earlier mapping)
    st.markdown('<div style="margin-top: 16px;">', unsafe_allow_html=True)
    st.markdown(f'<h3 class="h3">💡 {selected_day}\'s Quick Tips</h3>', unsafe_allow_html=True)

    tips_by_day = {
        'Mon': ["Start your week with a protein-rich breakfast", "Include whole grains for sustained energy", "Drink plenty of water throughout the day"],
        'Tue': ["Add 1 boiled egg to increase protein", "Include 50g spinach for iron", "Opt for lean protein sources"],
        'Wed': ["Include colorful vegetables in every meal", "Choose complex carbs over simple sugars", "Stay hydrated with 8-10 glasses of water"],
        'Thu': ["Focus on fiber-rich foods", "Include healthy fats like avocado or nuts", "Plan your meals ahead for better choices"],
        'Fri': ["Balance your macros throughout the day", "Include omega-3 rich foods", "Don't skip meals - maintain regular eating"],
        'Sat': ["Enjoy a variety of fruits and vegetables", "Include probiotic foods for gut health", "Stay active and maintain portion control"],
        'Sun': ["Prepare healthy meals for the week ahead", "Include antioxidant-rich foods", "Reflect on your weekly nutrition goals"]
    }

    tips = tips_by_day.get(selected_day, tips_by_day['Mon'])
    tips_html = "".join([f'<li>{t}</li>' for t in tips])
    st.markdown(f"""
        <ul style="color: #7F8C8D; font-size: 14px; line-height: 1.8; padding-left: 20px;">
            {tips_html}
        </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
