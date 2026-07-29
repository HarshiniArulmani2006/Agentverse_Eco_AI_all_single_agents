from flask import Blueprint, request, jsonify
from database import db_manager

carbon_bp = Blueprint('carbon', __name__)

def safe_float(val, default_val=0.0):
    try:
        if val is None or str(val).strip() == "":
            return float(default_val)
        return float(val)
    except (ValueError, TypeError):
        return float(default_val)

@carbon_bp.route('/api/carbon-calculator', methods=['POST'])
def calculate_carbon_footprint():
    data = request.get_json() or {}
    
    daily_travel_km = safe_float(data.get('dailyTravelKm'), 15.0)
    travel_mode = str(data.get('travelMode', 'car_petrol')).lower() # car_petrol, bike, bus, ev
    monthly_electricity_kwh = safe_float(data.get('monthlyElectricityKwh'), 200.0)
    weekly_plastic_items = safe_float(data.get('weeklyPlasticItems'), 10.0)
    diet_type = str(data.get('dietType', 'average')).lower() # meat_heavy, average, vegetarian, vegan
    flights_per_year = safe_float(data.get('flightsPerYear'), 0.0)

    # Emission factors (kg CO2e per unit)
    travel_factors = {
        'car_petrol': 0.19,  # kg CO2 per km
        'bike': 0.05,        # scooter/motorcycle
        'bus': 0.04,         # public bus / metro
        'ev': 0.03           # electric vehicle
    }
    tf = travel_factors.get(travel_mode, 0.15)

    diet_factors = {
        'meat_heavy': 2500.0,
        'average': 1700.0,
        'vegetarian': 1000.0,
        'vegan': 600.0
    }
    df = diet_factors.get(diet_type, 1700.0)

    annual_travel_co2 = daily_travel_km * 365.0 * tf
    annual_elec_co2 = monthly_electricity_kwh * 12.0 * 0.85 # grid factor
    annual_plastic_co2 = weekly_plastic_items * 52.0 * 0.06
    annual_diet_co2 = df
    annual_flight_co2 = flights_per_year * 450.0 # ~450kg CO2 per short/mid flight segment

    total_carbon_score = round(
        annual_travel_co2 + annual_elec_co2 + annual_plastic_co2 + annual_diet_co2 + annual_flight_co2, 2
    )

    # Impact rating
    if total_carbon_score < 2000:
        rating = "Low Impact (Eco Champion)"
        rating_color = "green"
    elif total_carbon_score < 4000:
        rating = "Moderate Impact (Room for Improvement)"
        rating_color = "yellow"
    elif total_carbon_score < 6000:
        rating = "High Impact (Action Needed)"
        rating_color = "orange"
    else:
        rating = "Severe Impact (Urgent Action Needed)"
        rating_color = "red"

    # Personalized Actionable suggestions
    suggestions = []
    if annual_travel_co2 > 1000:
        suggestions.append("Switch to public transit or carpooling 2 days per week to cut travel emissions by ~400kg CO2 yearly.")
    if annual_elec_co2 > 1500:
        suggestions.append("Upgrade to 5-star rated inverter appliances and install LED bulbs to trim electricity emissions.")
    if weekly_plastic_items > 5:
        suggestions.append("Replace single-use plastic bottles & bags with stainless steel flasks and jute carry bags.")
    if diet_type in ['meat_heavy', 'average']:
        suggestions.append("Adopting 'Meatless Mondays' or plant-forward meals cuts your diet emissions by 300+ kg CO2 yearly.")
    if flights_per_year > 0:
        suggestions.append("Offset flight travel emissions by supporting certified reforestation or renewable energy projects.")
    if not suggestions:
        suggestions.append("Outstanding work! Your carbon footprint meets the global 1.5°C Paris Accord benchmark target.")

    result = {
        "dailyTravelKm": daily_travel_km,
        "travelMode": travel_mode,
        "monthlyElectricityKwh": monthly_electricity_kwh,
        "weeklyPlasticItems": weekly_plastic_items,
        "dietType": diet_type,
        "flightsPerYear": flights_per_year,
        "totalCarbonScoreKg": total_carbon_score,
        "annualTravelCo2": round(annual_travel_co2, 2),
        "annualElecCo2": round(annual_elec_co2, 2),
        "annualPlasticCo2": round(annual_plastic_co2, 2),
        "annualDietCo2": round(annual_diet_co2, 2),
        "annualFlightCo2": round(annual_flight_co2, 2),
        "rating": rating,
        "ratingColor": rating_color,
        "suggestions": suggestions,
        "globalAverageKg": 4700,
        "targetGoalKg": 2000
    }

    db_manager.insert_record("carbon_calculations", result)

    return jsonify({
        "status": "success",
        "result": result
    })
