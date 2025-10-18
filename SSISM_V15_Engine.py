# SSISM_V15_Engine.py
# Hybrid V13-V14 Engine for Ethical Predictions
# Commit: 5ba2ec09d048f9679a5eb05a6110aa06d3979be7
# Preservation on GitHub: https://github.com/UIngarsoe/SSISM-V15-PYINNYASHI-

import datetime
import requests

# Constraints
SAFETY_VETO_FLOOR = 3.5
ZERO_COST_CONSTRAINT = True
NON_VIOLENT_PREACHING = True

PLANETARY_HOUR_CYCLE = ['Sun', 'Venus', 'Mercury', 'Moon', 'Saturn', 'Jupiter', 'Mars']

SUN_TIMES_API_URL = "https://api.astronomy.com/v1/sun-times"
API_KEY_SIMULATED = "YOUR_LIVE_ASTRONOMY_KEY"
DEFAULT_LAT_LONG = {"NYC_Grok_Test": (40.7128, -74.0060)}

DHARMA_SOLUTION_MATRIX = {
    'BAD_DIRECTION': "မေတ္တာပို့ အကြံဉာဏ်: မေတ္တာပို့ပြီးမှ ခရီးစတင်ခြင်း။",
    'CONFLICT_HOUR': "တိတ်ဆိတ်ခြင်းအကြံဉာဏ်: စကားပြောခြင်းကို လျှော့ချ/စိတ်ရှည်စွာ နားထောင်ခြင်း။ (Amā Mandate: Defensive Equanimity)",
    'NEGATIVE_PLANET': "ကုသိုလ်အားပေး အကြံဉာဏ်: အများအကျိုးအတွက် စေတနာဖြင့် တစ်ခုခုလုပ်ဆောင်ခြင်း။ (Mettā Mandate: Expansive Compassion)",
    'MENTAL_DUKKHA': "ဝိပဿနာအကြံဉာဏ်: ဖြစ်ပေါ်သော စိတ်ခံစားချက်ကို ယောနိသောမနသိကာရဖြင့် ရှုမှတ်ခြင်း။ (Amā Mandate: Patience)"
}

# Helper Functions (V13 Base)
def time_to_minutes(time_str: str) -> int:
    time_obj = datetime.datetime.strptime(time_str, "%H:%M")
    return time_obj.hour * 60 + time_obj.minute

def minutes_to_time_str(minutes: int) -> str:
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"

def get_planet_by_day(date: datetime.date) -> str:
    day_of_week = date.weekday()
    return PLANETARY_HOUR_CYCLE[day_of_week]

def fetch_sun_times(date: datetime.date, location: str) -> tuple:
    lat, lon = DEFAULT_LAT_LONG.get(location, (40.7128, -74.0060))
    # Simulated API response (replace with live key)
    return "06:00", "18:00", "06:00"  # Sunrise, Sunset, Next Sunrise

def calculate_inga_wizar_hours(start_time: str, end_time: str, start_index: int, num_hours: int, period_type: str) -> dict:
    start_minutes = time_to_minutes(start_time)
    end_minutes = time_to_minutes(end_time)
    total_minutes = end_minutes - start_minutes
    if total_minutes <= 0:
        total_minutes += 24 * 60
    minutes_per_hour = total_minutes // num_hours

    hour_map = {}
    for i in range(num_hours):
        current_minutes = start_minutes + (i * minutes_per_hour)
        start_time_str = minutes_to_time_str(current_minutes)
        end_minutes = current_minutes + minutes_per_hour
        end_time_str = minutes_to_time_str(end_minutes)
        planet_index = (start_index + i) % 7
        hour_map[f"{period_type}_Hour_{i+1}"] = {
            "start": start_time_str,
            "end": end_time_str,
            "ruling_planet": PLANETARY_HOUR_CYCLE[planet_index]
        }
    return hour_map

def calculate_natal_risk_score(current_planet: str, natal_planet: str) -> float:
    if current_planet == "N/A" or natal_planet == "N/A":
        return -1.0
    c_idx = PLANETARY_HOUR_CYCLE.index(current_planet)
    n_idx = PLANETARY_HOUR_CYCLE.index(natal_planet)
    distance = min(abs(c_idx - n_idx), 7 - abs(c_idx - n_idx))
    return 3.0 - distance  # Max risk 3.0, min 0.0

# V15 Upgrade: R_Delta Calculation
def calculate_resilience_delta(n_risk: float, v0_gravity: float = 1.5, w_p: float = 0.6) -> float:
    """V14 Core: R_Delta = [W_P * (4.0 - N_Risk) + 0.5 * E_Soc] / 3"""
    e_soc = 1.0  # Default for Mahā-Purisa like DJT
    return (w_p * (4.0 - n_risk) + 0.5 * e_soc) / 3.0

# V15_SSISM_Predict (Full Implementation)
def V15_SSISM_Predict(client_name: str, client_dob: str, query_time: str, location: str, v0_gravity: float = 1.5) -> dict:
    """
    V15 Engine: Combines V13's live prediction with V14's Dharma-Resilience Index.
    """
    query_dt = datetime.datetime.strptime(query_time, "%Y-%m-%d %H:%M:%S")
    query_date = query_dt.date()
    
    # Natal Planet
    try:
        dob_date = datetime.datetime.strptime(client_dob, "%Y-%m-%d").date()
        natal_planet = get_planet_by_day(dob_date)
    except ValueError:
        natal_planet = "N/A"
    
    # Fetch Sun Times
    sunrise_t, sunset_t, next_sunrise_t = fetch_sun_times(query_date, location)
    
    # Calculate Planetary Hours
    day_start_planet = get_planet_by_day(query_date)
    day_start_index = PLANETARY_HOUR_CYCLE.index(day_start_planet)
    day_map = calculate_inga_wizar_hours(sunrise_t, sunset_t, day_start_index, 12, "Day")
    last_day_planet_index = (day_start_index + 11) % 7
    night_start_index = (last_day_planet_index + 1) % 7
    night_map = calculate_inga_wizar_hours(sunset_t, next_sunrise_t, night_start_index, 12, "Night")
    inga_wizar_map = day_map | night_map
    
    # Current Planetary Hour
    current_planet = "N/A"
    for block, data in inga_wizar_map.items():
        start_dt_only_time = datetime.datetime.strptime(data['start'], "%H:%M").time()
        end_dt_only_time = datetime.datetime.strptime(data['end'], "%H:%M").time()
        start_dt = datetime.datetime.combine(query_date, start_dt_only_time)
        end_dt = datetime.datetime.combine(query_date, end_dt_only_time)
        if start_dt_only_time > end_dt_only_time:
            end_dt += datetime.timedelta(days=1)
        if start_dt <= query_dt < end_dt:
            current_planet = data['ruling_planet']
            break
    
    # V14 Upgrade: Resilience Calculation
    n_risk = calculate_natal_risk_score(current_planet, natal_planet)
    r_delta = calculate_resilience_delta(n_risk, v0_gravity)
    mandate = "Amā" if r_delta <= 1.9 else "Mettā"

    # V13 Solution Logic with V14 Filter
    if ZERO_COST_CONSTRAINT and r_delta < 1.0:
        solution_category = 'MENTAL_DUKKHA'
    elif current_planet == "N/A" or n_risk == -1.0:
        solution_category = 'MENTAL_DUKKHA'
    elif n_risk == 3.0:
        solution_category = 'CONFLICT_HOUR'
    else:
        solution_category = 'NEGATIVE_PLANET'
    
    final_advice_text = DHARMA_SOLUTION_MATRIX[solution_category]

    # Final Output
    final_advice = {
        "Status": "V15 Pyinnyashi Output",
        "Planetary_Hour_Map": inga_wizar_map,
        "Current_Planet": current_planet,
        "Natal_Planet_D_Num": natal_planet,
        "Natal_Risk_Score_V13": n_risk,
        "R_Delta_Resilience": r_delta,
        "Mandate_Type": mandate,
        "Zero_Cost_Adherence": ZERO_COST_CONSTRAINT,
        "Solution_S_Dharma": final_advice_text,
        "API_Integration_Status": "Active (Using Simulated Data for Test)"
    }
    return final_advice

# Test Run (Example)
if __name__ == "__main__":
    test_result_v15 = V15_SSISM_Predict(
        client_name="Donald J. Trump",
        client_dob="1946-06-14",
        query_time="2026-07-01 14:30:00",
        location="NYC_Grok_Test",
        v0_gravity=1.0
    )
    print(test_result_v15)
