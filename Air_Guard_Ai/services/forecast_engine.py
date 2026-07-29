"""
Pollution Trend Prediction, Anomaly Detection & Analytics Engine
"""
from typing import Dict, Any, List

class ForecastEngine:

    def predict_trends(self, hourly_data: Dict[str, Any], current_aqi: float) -> Dict[str, Dict[str, Any]]:
        us_aqi_list = hourly_data.get("us_aqi", []) or hourly_data.get("pm2_5", [])

        if not us_aqi_list or len(us_aqi_list) < 24:
            # Fallback if hourly data is insufficient
            return {
                "next_hour": {"direction": "Stable", "expected_aqi": current_aqi},
                "next_6_hours": {"direction": "Stable", "expected_aqi": current_aqi},
                "tomorrow": {"direction": "Stable", "expected_aqi": current_aqi},
                "next_3_days": {"direction": "Stable", "expected_aqi": current_aqi},
                "next_7_days": {"direction": "Stable", "expected_aqi": current_aqi}
            }

        curr = us_aqi_list[0] if us_aqi_list[0] is not None else current_aqi
        h1 = us_aqi_list[1] if len(us_aqi_list) > 1 and us_aqi_list[1] is not None else curr
        h6 = us_aqi_list[6] if len(us_aqi_list) > 6 and us_aqi_list[6] is not None else curr
        h24 = sum([x for x in us_aqi_list[24:48] if x is not None]) / max(1, len([x for x in us_aqi_list[24:48] if x is not None])) if len(us_aqi_list) >= 48 else curr
        d3 = sum([x for x in us_aqi_list[48:72] if x is not None]) / max(1, len([x for x in us_aqi_list[48:72] if x is not None])) if len(us_aqi_list) >= 72 else curr
        d7 = sum([x for x in us_aqi_list[72:] if x is not None]) / max(1, len([x for x in us_aqi_list[72:] if x is not None])) if len(us_aqi_list) >= 72 else curr

        def determine_direction(old_val, new_val):
            diff = new_val - old_val
            if diff < -5:
                return "Improving"
            elif diff > 5:
                return "Worsening"
            else:
                return "Stable"

        return {
            "next_hour": {"direction": determine_direction(curr, h1), "expected_aqi": round(h1, 1)},
            "next_6_hours": {"direction": determine_direction(curr, h6), "expected_aqi": round(h6, 1)},
            "tomorrow": {"direction": determine_direction(curr, h24), "expected_aqi": round(h24, 1)},
            "next_3_days": {"direction": determine_direction(curr, d3), "expected_aqi": round(d3, 1)},
            "next_7_days": {"direction": determine_direction(curr, d7), "expected_aqi": round(d7, 1)}
        }

    def detect_anomalies(self, hourly_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        anomalies = []
        pm2_5_series = hourly_data.get("pm2_5", [])
        times = hourly_data.get("time", [])

        if len(pm2_5_series) >= 24:
            clean_series = [x for x in pm2_5_series[:24] if x is not None]
            if clean_series:
                avg_pm25 = sum(clean_series) / len(clean_series)
                for idx, val in enumerate(clean_series):
                    if val is not None and val > avg_pm25 * 2.2 and val > 40:
                        timestamp = times[idx] if idx < len(times) else f"Hour {idx}"
                        anomalies.append({
                            "time": timestamp,
                            "pollutant": "PM2.5",
                            "spike_value": val,
                            "baseline_avg": round(avg_pm25, 1),
                            "ratio": round(val / avg_pm25, 1),
                            "description": f"Unusual PM2.5 spike detected at {timestamp}. Value {val} µg/m³ is {round(val/avg_pm25, 1)}x baseline daily average."
                        })
        return anomalies

    def generate_analytics(self, hourly_data: Dict[str, Any]) -> Dict[str, Any]:
        aqi_list = [x for x in hourly_data.get("us_aqi", []) if x is not None]
        times = hourly_data.get("time", [])

        if not aqi_list:
            return {
                "daily_aqi_avg": 0,
                "weekly_aqi_avg": 0,
                "peak_pollution_hour": "N/A",
                "lowest_pollution_hour": "N/A",
                "trend_summary": "Insufficient data"
            }

        daily_avg = round(sum(aqi_list[:24]) / max(1, len(aqi_list[:24])), 1)
        weekly_avg = round(sum(aqi_list) / max(1, len(aqi_list)), 1)

        # Peak and lowest times in 24h
        day_aqi = aqi_list[:24]
        max_idx = day_aqi.index(max(day_aqi)) if day_aqi else 0
        min_idx = day_aqi.index(min(day_aqi)) if day_aqi else 0

        peak_time = times[max_idx] if max_idx < len(times) else f"Hour {max_idx}"
        lowest_time = times[min_idx] if min_idx < len(times) else f"Hour {min_idx}"

        return {
            "daily_aqi_avg": daily_avg,
            "weekly_aqi_avg": weekly_avg,
            "peak_pollution_hour": peak_time,
            "peak_aqi_value": max(day_aqi) if day_aqi else 0,
            "lowest_pollution_hour": lowest_time,
            "lowest_aqi_value": min(day_aqi) if day_aqi else 0,
            "trend_summary": f"Daily mean AQI is {daily_avg}. Pollution peaks around {peak_time} and reaches lowest levels near {lowest_time}."
        }

forecast_engine = ForecastEngine()
