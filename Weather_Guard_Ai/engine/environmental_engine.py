"""
WeatherWise AI - Environmental Intelligence Engine
Analyzes weather impact on renewable energy generation, agricultural irrigation,
wildfire risk, and power grid energy demand.
"""

import logging
from models.schema import WeatherMetrics, EnvironmentalImpact

logger = logging.getLogger("WeatherWise.EnvironmentalEngine")


def generate_environmental_impact(metrics: WeatherMetrics) -> EnvironmentalImpact:
    """
    Evaluates weather parameters to determine environmental intelligence signals
    for downstream renewable energy, agriculture, and grid agents.
    
    Args:
        metrics: WeatherMetrics object
        
    Returns:
        EnvironmentalImpact object
    """
    cloud_cover = metrics.cloud_cover
    uv_index = metrics.uv_index
    wind_speed = metrics.wind_speed_kmh
    rain_prob = metrics.rain_probability
    wmo_code = metrics.wmo_code
    temp = metrics.temperature_c
    humidity = metrics.relative_humidity

    # --- 1. Solar Power Generation Potential ---
    if cloud_cover < 20 and uv_index >= 6.0:
        solar_potential = "EXCELLENT"
        solar_details = f"Clear sky (Cloud cover: {cloud_cover}%) and strong solar irradiance (UV Index: {uv_index}) provide maximum solar photovoltaic generation."
    elif cloud_cover < 50:
        solar_potential = "HIGH"
        solar_details = f"Moderate cloud cover ({cloud_cover}%) allows consistent solar energy harvesting."
    elif cloud_cover < 80:
        solar_potential = "MODERATE"
        solar_details = f"High cloudiness ({cloud_cover}%) reduces solar PV efficiency by ~40-60%."
    else:
        solar_potential = "LOW"
        solar_details = f"Overcast/Rainy skies ({cloud_cover}% cloud cover) restrict solar power output."

    # --- 2. Wind Energy Potential ---
    if wind_speed >= 35.0:
        wind_potential = "EXCELLENT"
        wind_details = f"High wind velocity ({wind_speed:.1f} km/h) delivers peak turbine energy production."
    elif wind_speed >= 20.0:
        wind_potential = "GOOD"
        wind_details = f"Moderate wind speed ({wind_speed:.1f} km/h) is suitable for effective wind energy generation."
    elif wind_speed >= 10.0:
        wind_potential = "MODERATE"
        wind_details = f"Light breeze ({wind_speed:.1f} km/h) produces baseline wind generation."
    else:
        wind_potential = "POOR"
        wind_details = f"Calm winds ({wind_speed:.1f} km/h) are insufficient for wind turbine operation."

    # --- 3. Agricultural Irrigation Need ---
    if rain_prob >= 60 or wmo_code in [61, 63, 65, 80, 81, 82, 95]:
        irrigation_need = "NONE (RAIN EXPECTED)"
        irrigation_details = f"Precipitation expected (Rain probability: {rain_prob}%). Natural rainfall will supply crops, reducing agricultural irrigation demand."
    elif humidity >= 85 or cloud_cover >= 80:
        irrigation_need = "LOW"
        irrigation_details = "High humidity reduces soil evapotranspiration losses."
    elif temp >= 33.0 or humidity <= 40:
        irrigation_need = "HIGH"
        irrigation_details = "High temperatures and dry air accelerate soil moisture loss. Crop irrigation recommended."
    else:
        irrigation_need = "MODERATE"
        irrigation_details = "Normal evapotranspiration rates. Standard crop watering schedules apply."

    # --- 4. Electricity Demand & Grid Load Impact ---
    if temp >= 36.0:
        electricity_demand = "CRITICAL (PEAK COOLING LOAD)"
    elif temp >= 32.0:
        electricity_demand = "ELEVATED (COOLING LOAD)"
    elif temp <= 10.0:
        electricity_demand = "ELEVATED (HEATING LOAD)"
    else:
        electricity_demand = "NORMAL"

    # --- 5. Wildfire Risk Assessment ---
    if temp >= 35.0 and humidity <= 30 and wind_speed >= 25.0 and rain_prob < 10:
        wildfire_risk = "EXTREME"
    elif temp >= 30.0 and humidity <= 45 and wind_speed >= 18.0:
        wildfire_risk = "HIGH"
    elif temp >= 25.0 and humidity <= 55:
        wildfire_risk = "MODERATE"
    else:
        wildfire_risk = "LOW"

    # --- Synthesis Summary ---
    env_summary = (
        f"Solar: {solar_potential} | Wind: {wind_potential} | Irrigation: {irrigation_need} | "
        f"Grid Load: {electricity_demand} | Wildfire Risk: {wildfire_risk}"
    )

    return EnvironmentalImpact(
        solar_power_potential=solar_potential,
        solar_details=solar_details,
        wind_energy_potential=wind_potential,
        wind_details=wind_details,
        irrigation_need=irrigation_need,
        irrigation_details=irrigation_details,
        electricity_demand_impact=electricity_demand,
        wildfire_risk=wildfire_risk,
        environmental_summary=env_summary
    )
