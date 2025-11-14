import streamlit as st
import plotly.graph_objects as go
from math import isfinite

# ---------------------------------------------------------
# 🥗 Page Configuration
# ---------------------------------------------------------
st.set_page_config(page_title="Meal Plan", page_icon="🥗", layout="wide")

# Load custom CSS (optional)
try:
    st.markdown(f"<style>{open('assets/styles.css').read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    pass

# ---------------------------------------------------------
# 🧭 Page Header
# ---------------------------------------------------------
st.markdown('<h1 class="h1">Meal Plan</h1>', unsafe_allow_html=True)
st.markdown('<div class="text-muted" style="margin-bottom: 18px;">AI suggestions and your daily & weekly view</div>', unsafe_allow_html=True)

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
    try:
        bmi = float(bmi_home)
    except Exception:
        bmi = None
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
# 🌱 Diet Preference Selection (Veg / Non-Veg / Vegan)
# ---------------------------------------------------------
st.markdown("<h3 class='h3'>Choose Diet Preference</h3>", unsafe_allow_html=True)
diet_type = st.radio(
    "Select diet type",
    ["Veg", "Non-Veg", "Vegan"],
    horizontal=True,
    index=["Veg","Non-Veg","Vegan"].index(st.session_state.get("diet_type","Veg")),
    key="diet_type_selector"
)
# store choice (useful elsewhere)
st.session_state["diet_type"] = diet_type

# ---------------------------
# BMI-based meal intent (keeps your original logic)
# ---------------------------
if bmi_category in ["Underweight"]:
    bmi_default_meals = {
        'Mon': {'breakfast': 'Oats + milk + nuts', 'lunch': 'Rice + dal + chicken', 'dinner': 'Paneer curry + rice'},
        'Tue': {'breakfast': 'Banana shake + oats', 'lunch': 'Chapati + dal + potato', 'dinner': 'Egg curry + rice'},
        'Wed': {'breakfast': 'Peanut butter toast', 'lunch': 'Paneer biryani', 'dinner': 'Chicken + rice'},
        'Thu': {'breakfast': 'Smoothie + oats', 'lunch': 'Rice + fish', 'dinner': 'Roti + dal + ghee'},
        'Fri': {'breakfast': 'Muesli + milk', 'lunch': 'Rice + chicken', 'dinner': 'Paneer + roti'},
        'Sat': {'breakfast': 'Boiled eggs + toast', 'lunch': 'Chicken breast + rice', 'dinner': 'Curd rice'},
        'Sun': {'breakfast': 'Pancakes + eggs', 'lunch': 'Rice + dal + ghee', 'dinner': 'Veg pulao'}
    }
    suggestions = [
        ("🥜", "Add nuts & seeds", "Calorie-dense healthy fats"),
        ("🥛", "Include milk & shakes", "Extra protein and calories"),
        ("🍚", "Add complex carbs", "Support weight gain")
    ]

elif bmi_category in ["Overweight", "Obese"]:
    bmi_default_meals = {
        'Mon': {'breakfast': 'Greek yogurt + berries', 'lunch': 'Grilled chicken salad', 'dinner': 'Steamed veggies + soup'},
        'Tue': {'breakfast': 'Smoothie (green)', 'lunch': 'Quinoa bowl', 'dinner': 'Grilled fish + salad'},
        'Wed': {'breakfast': 'Oats + fruit', 'lunch': 'Lentil salad', 'dinner': 'Veg stir-fry'},
        'Thu': {'breakfast': 'Fruit bowl', 'lunch': 'Chicken + salad', 'dinner': 'Soup'},
        'Fri': {'breakfast': 'Egg white omelette', 'lunch': 'Paneer salad', 'dinner': 'Grilled veggies'},
        'Sat': {'breakfast': 'Protein smoothie', 'lunch': 'Fish + greens', 'dinner': 'Salad'},
        'Sun': {'breakfast': 'Muesli', 'lunch': 'Brown rice + dal + salad', 'dinner': 'Soup'}
    }
    suggestions = [
        ("🥗", "Increase veggies", "Low-calorie, high-fiber foods"),
        ("🍗", "Prioritize lean protein", "Improves satiety"),
        ("🚶", "Add daily activity", "Boost energy expenditure")
    ]

elif bmi_category == "Normal":
    bmi_default_meals = {
        'Mon': {'breakfast': 'Oats + fruits', 'lunch': 'Rice + dal + veg', 'dinner': 'Soup + salad'},
        'Tue': {'breakfast': 'Eggs & toast', 'lunch': 'Grilled chicken + rice', 'dinner': 'Veg curry'},
        'Wed': {'breakfast': 'Smoothie bowl', 'lunch': 'Paneer + chapati', 'dinner': 'Grilled fish + salad'},
        'Thu': {'breakfast': 'Muesli', 'lunch': 'Quinoa bowl', 'dinner': 'Stir-fry veggies'},
        'Fri': {'breakfast': 'Oats + milk', 'lunch': 'Dal + rice', 'dinner': 'Chicken soup'},
        'Sat': {'breakfast': 'Avocado toast', 'lunch': 'Brown rice + salad', 'dinner': 'Paneer + veggies'},
        'Sun': {'breakfast': 'Fruit bowl', 'lunch': 'Rice + dal', 'dinner': 'Soup & salad'}
    }
    suggestions = [
        ("🍎", "Balanced macros", "Maintain mixture of carbs/protein/fats"),
        ("🏃", "Stay active", "Keep consistent exercise routine"),
        ("🍳", "Include protein", "Support muscle mass")
    ]
else:
    bmi_default_meals = {d: {'breakfast': '', 'lunch': '', 'dinner': ''} for d in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']}
    suggestions = [
        ("🍽️", "Follow balanced plan", "Adjust to your preferences"),
        ("💧", "Hydrate", "Drink water regularly")
    ]

# ---------------------------------------------------------
# Diet-specific weekly meal templates (to replace bmi intent)
# ---------------------------------------------------------
veg_meals = {
    'Mon': {'breakfast': 'Oats + fruits', 'lunch': 'Veg pulao', 'dinner': 'Paneer curry + roti'},
    'Tue': {'breakfast': 'Idli + chutney', 'lunch': 'Veg biryani', 'dinner': 'Dal + rice'},
    'Wed': {'breakfast': 'Upma + fruits', 'lunch': 'Paneer curry + rice', 'dinner': 'Veg soup'},
    'Thu': {'breakfast': 'Poha + nuts', 'lunch': 'Veg thali', 'dinner': 'Khichdi + curd'},
    'Fri': {'breakfast': 'Paratha + curd', 'lunch': 'Veg fried rice', 'dinner': 'Dal tadka + roti'},
    'Sat': {'breakfast': 'Smoothie bowl', 'lunch': 'Paneer rice bowl', 'dinner': 'Veg noodles'},
    'Sun': {'breakfast': 'Muesli + milk', 'lunch': 'Veg thali', 'dinner': 'Soup + salad'}
}

nonveg_meals = {
    'Mon': {'breakfast': 'Egg omelette', 'lunch': 'Chicken biryani', 'dinner': 'Grilled chicken + veggies'},
    'Tue': {'breakfast': 'Boiled eggs', 'lunch': 'Fish curry + rice', 'dinner': 'Chicken soup'},
    'Wed': {'breakfast': 'Egg sandwich', 'lunch': 'Chicken fried rice', 'dinner': 'Fish grill'},
    'Thu': {'breakfast': 'Protein shake', 'lunch': 'Chicken thali', 'dinner': 'Egg curry'},
    'Fri': {'breakfast': 'Scrambled eggs', 'lunch': 'Fish biryani', 'dinner': 'Chicken salad'},
    'Sat': {'breakfast': 'Egg dosa', 'lunch': 'Chicken rice bowl', 'dinner': 'Fish soup'},
    'Sun': {'breakfast': 'Omelette + toast', 'lunch': 'Chicken curry', 'dinner': 'Boiled eggs + veggies'}
}

vegan_meals = {
    'Mon': {'breakfast': 'Oats + almond milk', 'lunch': 'Veg quinoa bowl', 'dinner': 'Tofu stir-fry'},
    'Tue': {'breakfast': 'Fruit smoothie', 'lunch': 'Vegan thali', 'dinner': 'Veg salad + beans'},
    'Wed': {'breakfast': 'Peanut butter toast', 'lunch': 'Brown rice + lentils', 'dinner': 'Tofu curry'},
    'Thu': {'breakfast': 'Chia pudding', 'lunch': 'Steamed veggies + rice', 'dinner': 'Vegan soup'},
    'Fri': {'breakfast': 'Green smoothie', 'lunch': 'Veg wrap', 'dinner': 'Tofu grill'},
    'Sat': {'breakfast': 'Sprouts salad', 'lunch': 'Rice + veg curry', 'dinner': 'Vegan pasta'},
    'Sun': {'breakfast': 'Granola + soy milk', 'lunch': 'Veg fried rice', 'dinner': 'Tofu biryani'}
}

# ---------------------------------------------------------
# Compose default meals: merge BMI intent with diet-specific items
# ---------------------------------------------------------
def compose_default_meals(bmi_defaults, diet_choice):
    if diet_choice == "Veg":
        diet_map = veg_meals
    elif diet_choice == "Non-Veg":
        diet_map = nonveg_meals
    else:
        diet_map = vegan_meals

    composed = {}
    for day in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']:
        composed[day] = {
            'breakfast': diet_map.get(day, {}).get('breakfast') or bmi_defaults.get(day, {}).get('breakfast', ''),
            'lunch': diet_map.get(day, {}).get('lunch') or bmi_defaults.get(day, {}).get('lunch', ''),
            'dinner': diet_map.get(day, {}).get('dinner') or bmi_defaults.get(day, {}).get('dinner', '')
        }
    return composed

default_meals = compose_default_meals(bmi_default_meals, diet_type)

# ---------------------------------------------------------
# Option 2: BMI + Diet based macros (calories + macro% -> grams)
# - We compute a target total daily calories from BMI category,
#   then apply a macro percentage split depending on diet type + BMI intent.
# ---------------------------------------------------------
def compute_daily_calories(bmi_cat):
    """
    Rough calorie targets for an average adult (can be tuned).
    These are defaults — you may override per-user later using weight/age/activity.
    """
    if bmi_cat == "Underweight":
        return 2600  # calorie surplus to gain weight
    if bmi_cat == "Normal":
        return 2100
    if bmi_cat == "Overweight":
        return 1700
    if bmi_cat == "Obese":
        return 1500
    return 2000

# Macro % table by (diet_type, bmi_category)
# values are (carb%, protein%, fat%)
macro_pct_table = {
    "Veg": {
        "Underweight": (55, 20, 25),
        "Normal": (60, 18, 22),
        "Overweight": (50, 20, 30),
        "Obese": (45, 20, 35),
        "Unknown": (55, 18, 27)
    },
    "Non-Veg": {
        "Underweight": (50, 25, 25),
        "Normal": (50, 30, 20),
        "Overweight": (40, 35, 25),
        "Obese": (35, 40, 25),
        "Unknown": (50, 28, 22)
    },
    "Vegan": {
        "Underweight": (58, 18, 24),
        "Normal": (60, 18, 22),
        "Overweight": (55, 18, 27),
        "Obese": (50, 20, 30),
        "Unknown": (58, 18, 24)
    }
}

def compute_macros(bmi_cat, diet_choice):
    total_kcal = compute_daily_calories(bmi_cat)
    pct = macro_pct_table.get(diet_choice, {}).get(bmi_cat, macro_pct_table[diet_choice].get("Unknown"))
    carb_pct, prot_pct, fat_pct = pct

    carb_kcal = total_kcal * carb_pct / 100.0
    prot_kcal = total_kcal * prot_pct / 100.0
    fat_kcal = total_kcal * fat_pct / 100.0

    # grams: carbs & protein = 4 kcal/g, fats = 9 kcal/g
    carbs_g = round(carb_kcal / 4)
    protein_g = round(prot_kcal / 4)
    fats_g = round(fat_kcal / 9)

    # For chart we want percentages (by kcal)
    carbs_pct_kcal = round(carb_kcal / total_kcal * 100)
    protein_pct_kcal = round(prot_kcal / total_kcal * 100)
    fat_pct_kcal = 100 - carbs_pct_kcal - protein_pct_kcal  # ensure sums to ~100

    return {
        "calories": int(total_kcal),
        "carbs_g": int(carbs_g),
        "protein_g": int(protein_g),
        "fats_g": int(fats_g),
        "carbs_pct": int(carbs_pct_kcal),
        "protein_pct": int(protein_pct_kcal),
        "fats_pct": int(fat_pct_kcal)
    }

macros = compute_macros(bmi_category, diet_type)

# ---------------------------------------------------------
# Populate session_state weekly_meals with default_meals (no edit feature)
# ---------------------------------------------------------
for d in ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']:
    st.session_state['weekly_meals'][d] = default_meals.get(d, {'breakfast':'','lunch':'','dinner':''})

# ---------------------------------------------------------
# Layout: Left (Suggestions + Chart) | Right (Weekly Planner)
# ---------------------------------------------------------
left, right = st.columns([2, 1])

# ==============================
# LEFT SIDE CONTENT
# ==============================
with left:
    st.markdown('<h2 class="h2">AI Diet Suggestions</h2>', unsafe_allow_html=True)
    st.markdown(f'<div class="text-muted" style="margin-bottom: 8px;">Detected BMI: <b>{bmi:.1f}</b> — Category: <b>{bmi_category}</b></div>', unsafe_allow_html=True)
    if bmi_percent is not None:
        st.markdown(f'<div class="text-muted" style="margin-bottom: 10px;">BMI % (vs ideal 22): <b>{bmi_percent}%</b></div>', unsafe_allow_html=True)
        prog = min(max(int(round(bmi_percent)), 0), 200)
        st.progress(min(prog, 100) / 100.0)

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
    st.markdown('<div style="margin-bottom: 14px;"></div>', unsafe_allow_html=True)

    # ---- Daily Nutrient Breakdown (dynamic based on BMI + diet) ----
    st.markdown('<h2 class="h2">Daily Nutrient Breakdown</h2>', unsafe_allow_html=True)

    calories = macros["calories"]
    carbs_g = macros["carbs_g"]
    protein_g = macros["protein_g"]
    fats_g = macros["fats_g"]

    carbs_pct = macros["carbs_pct"]
    protein_pct = macros["protein_pct"]
    fats_pct = macros["fats_pct"]

    fig = go.Figure(
        data=[go.Pie(
            labels=['Carbs', 'Protein', 'Fats'],
            values=[carbs_pct, protein_pct, fats_pct],
            hole=.58,
            marker=dict(colors=['#50C878', '#4A90E2', '#FFD700']),
            textinfo='label+percent',
            textposition='outside'
        )]
    )
    fig.update_layout(
        margin=dict(t=8, b=8, l=8, r=8),
        showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05),
        annotations=[dict(text=f"{calories}<br>kcal", x=0.5, y=0.5, font=dict(size=20, color="#667eea"), showarrow=False)]
    )
    st.plotly_chart(fig, use_container_width=True)

    # Nutrition info below chart
    st.markdown(f"""
    <div style="display:flex; gap:16px; margin-top:12px; justify-content:center; flex-wrap: wrap;">
        <div style="text-align: center;">
            <div style="color: #FFD700; font-size: 15px; font-weight: 700;">Calories</div>
            <div style="color: #667eea; font-size: 15px; font-weight: 700; margin-top: 4px;">{calories} kcal</div>
        </div>
        <div style="text-align: center;">
            <div style="color: #4A90E2; font-size: 15px; font-weight: 700;">Protein</div>
            <div style="color: #667eea; font-size: 15px; font-weight: 700; margin-top: 4px;">{protein_g} g</div>
        </div>
        <div style="text-align: center;">
            <div style="color: #50C878; font-size: 15px; font-weight: 700;">Carbs</div>
            <div style="color: #667eea; font-size: 15px; font-weight: 700; margin-top: 4px;">{carbs_g} g</div>
        </div>
        <div style="text-align: center;">
            <div style="color: #9B59B6; font-size: 15px; font-weight: 700;">Fats</div>
            <div style="color: #667eea; font-size: 15px; font-weight: 700; margin-top: 4px;">{fats_g} g</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==============================
# RIGHT SIDE CONTENT (Weekly Planner)
# ==============================
with right:
    st.markdown('<h2 class="h2">Weekly Planner</h2>', unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom:10px;"></div>', unsafe_allow_html=True)

    days_full = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    try:
        current_index = days_full.index(st.session_state.get('selected_day','Mon'))
    except ValueError:
        current_index = 0
    selected_day = st.radio("Select Day", days_full, horizontal=True, index=current_index, key="day_selector")
    st.session_state['selected_day'] = selected_day

    # Show BMI & Category at top of planner
    st.markdown(f"<div style='margin-top:6px; font-size:14px; color:#333;'>BMI: <b>{bmi:.1f}</b> &nbsp; | &nbsp; Category: <b>{bmi_category}</b></div>", unsafe_allow_html=True)
    if bmi_percent is not None:
        st.markdown(f"<div style='font-size:13px; color:#666;'>BMI % vs ideal: <b>{bmi_percent}%</b></div>", unsafe_allow_html=True)

    # Display auto-generated meals for selected day (no editing)
    day_meals = st.session_state['weekly_meals'].get(selected_day, {'breakfast':'','lunch':'','dinner':''})
    st.markdown('<div style="margin-top: 10px;"></div>', unsafe_allow_html=True)

    if day_meals.get('breakfast'):
        st.markdown(f"""
        <div style="margin-bottom: 10px;">
            <div style="font-weight: 600; color: #667eea; margin-bottom: 6px;">🍳 Breakfast</div>
            <div class="hint">{day_meals['breakfast']}</div>
        </div>
        """, unsafe_allow_html=True)

    if day_meals.get('lunch'):
        st.markdown(f"""
        <div style="margin-bottom: 10px;">
            <div style="font-weight: 600; color: #667eea; margin-bottom: 6px;">🍽️ Lunch</div>
            <div class="hint">{day_meals['lunch']}</div>
        </div>
        """, unsafe_allow_html=True)

    if day_meals.get('dinner'):
        st.markdown(f"""
        <div style="margin-bottom: 10px;">
            <div style="font-weight: 600; color: #667eea; margin-bottom: 6px;">🌙 Dinner</div>
            <div class="hint">{day_meals['dinner']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Quick Tips based on selected day
    st.markdown('<div style="margin-top: 12px;">', unsafe_allow_html=True)
    st.markdown(f'<h3 class="h3">💡 {selected_day}\'s Quick Tips</h3>', unsafe_allow_html=True)

    tips_by_day = {
        'Mon': ["Start your week with a protein-rich breakfast", "Include whole grains for sustained energy", "Drink plenty of water throughout the day"],
        'Tue': ["Include leafy greens for iron", "Add a portion of lean protein", "Opt for whole grains"],
        'Wed': ["Include colorful vegetables in every meal", "Choose complex carbs over simple sugars", "Stay hydrated"],
        'Thu': ["Focus on fiber-rich foods", "Include healthy fats like avocado or nuts", "Plan your meals ahead"],
        'Fri': ["Balance your macros throughout the day", "Include omega-3 rich foods (fish or flaxseed)", "Don't skip meals"],
        'Sat': ["Enjoy a variety of fruits and vegetables", "Include probiotic foods for gut health", "Stay active"],
        'Sun': ["Prepare healthy meals for the week ahead", "Include antioxidant-rich foods", "Reflect on your weekly nutrition goals"]
    }

    tips = tips_by_day.get(selected_day, tips_by_day['Mon'])
    tips_html = "".join([f'<li>{t}</li>' for t in tips])
    st.markdown(f"""
        <ul style="color: #7F8C8D; font-size: 14px; line-height: 1.7; padding-left: 20px;">
            {tips_html}
        </ul>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
