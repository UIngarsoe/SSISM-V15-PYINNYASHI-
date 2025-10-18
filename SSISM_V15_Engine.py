# V15 Upgrade: Add R_Delta Calculation
def calculate_resilience_delta(n_risk: float, v0_gravity: float = 1.5, w_p: float = 0.6) -> float:
    """V14 Core: R_Delta = [W_P * (4.0 - N_Risk) + 0.5 * E_Soc] / 3"""
    e_soc = 1.0  # Default for Mahā-Purisa like DJT
    return (w_p * (4.0 - n_risk) + 0.5 * e_soc) / 3.0

# Update V13_SSISM_Predict
def V15_SSISM_Predict(client_name: str, client_dob: str, query_time: str, location: str, v0_gravity: float = 1.5) -> dict:
    # ... (V13 logic: natal planet, hour map, current planet)
    n_risk = calculate_natal_risk_score(current_planet, natal_planet)
    r_delta = calculate_resilience_delta(n_risk, v0_gravity)
    mandate = "Amā" if r_delta <= 1.9 else "Mettā"

    if ZERO_COST_CONSTRAINT and r_delta < 1.0:
        solution_category = 'MENTAL_DUKKHA'
    # ... (rest of V13 logic)

    final_advice = {
        # ... (V13 fields)
        "R_Delta_Resilience": r_delta,
        "Mandate_Type": mandate,
        "Zero_Cost_Adherence": ZERO_COST_CONSTRAINT
    }
    return final_advice
