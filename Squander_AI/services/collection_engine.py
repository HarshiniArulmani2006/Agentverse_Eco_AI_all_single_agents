"""
Smart Bin Monitoring & Collection Optimization Engine
- Simulates real-time smart bin status (fill level, temperature, health)
- Predicts overflow before it occurs
- Generates optimized collection schedules and routes
- Estimates fuel savings, time savings, and carbon reduction
"""
import math
import random
from typing import Dict, Any, List
from config import BIN_THRESHOLDS, DAILY_BASELINE


SMART_BINS = [
    {"id": "BIN-001", "location": "Main Street & Oak Ave",       "type": "plastic",  "lat": 12.9716, "lon": 77.5946},
    {"id": "BIN-002", "location": "City Park North Gate",        "type": "organic",  "lat": 12.9722, "lon": 77.5960},
    {"id": "BIN-003", "location": "Market Square Central",       "type": "paper",    "lat": 12.9708, "lon": 77.5935},
    {"id": "BIN-004", "location": "Riverside Commercial Zone",   "type": "metal",    "lat": 12.9730, "lon": 77.5975},
    {"id": "BIN-005", "location": "Tech Hub East Entrance",      "type": "ewaste",   "lat": 12.9700, "lon": 77.5920},
    {"id": "BIN-006", "location": "Hospital District Gate 2",    "type": "biomedical","lat": 12.9745, "lon": 77.5990},
    {"id": "BIN-007", "location": "Industrial Zone Gate A",      "type": "hazardous","lat": 12.9688, "lon": 77.5910},
    {"id": "BIN-008", "location": "Residential Block D",         "type": "glass",    "lat": 12.9760, "lon": 77.6000},
]

COLLECTION_ROUTES = [
    {"route_id": "R-01", "name": "North-East Circuit",   "bins": ["BIN-001", "BIN-002", "BIN-003"], "distance_km": 8.4},
    {"route_id": "R-02", "name": "Commercial Corridor",  "bins": ["BIN-004", "BIN-005"],             "distance_km": 5.1},
    {"route_id": "R-03", "name": "Special Waste Route",  "bins": ["BIN-006", "BIN-007"],             "distance_km": 6.2},
    {"route_id": "R-04", "name": "Residential Loop",     "bins": ["BIN-008"],                        "distance_km": 3.8},
]

CATEGORY_COLORS = {
    "plastic":   "#3b82f6",
    "organic":   "#22c55e",
    "paper":     "#f59e0b",
    "metal":     "#6366f1",
    "ewaste":    "#8b5cf6",
    "biomedical":"#f43f5e",
    "hazardous": "#ef4444",
    "glass":     "#06b6d4",
    "mixed":     "#94a3b8",
}

# Simulated fill levels (deterministic seeded by bin id for consistency)
def _seed_fill(bin_id: str) -> float:
    seed = sum(ord(c) for c in bin_id)
    random.seed(seed + 42)
    return round(random.uniform(12, 98), 1)

def _get_bin_status(fill_pct: float) -> Dict[str, str]:
    for key, (lo, hi, color) in BIN_THRESHOLDS.items():
        if lo <= fill_pct < hi or (key == "overflow" and fill_pct >= 85):
            return {"status": key.title(), "color": color}
    return {"status": "Empty", "color": "#22c55e"}

def _predict_overflow(fill_pct: float, bin_type: str) -> Dict[str, Any]:
    """Predict hours until overflow based on fill rate."""
    daily_rate = {"organic": 18, "plastic": 8, "paper": 10, "metal": 5,
                  "ewaste": 3, "biomedical": 12, "hazardous": 4, "glass": 6}.get(bin_type, 8)
    remaining = max(0, 100 - fill_pct)
    hours_to_full = round((remaining / daily_rate) * 24, 1) if daily_rate > 0 else 999
    urgent = hours_to_full < 8
    return {
        "hours_until_overflow": hours_to_full,
        "urgent_collection":    urgent,
        "fill_rate_per_day":    daily_rate,
        "prediction_confidence": 85 if fill_pct > 60 else 70,
    }


class CollectionEngine:

    def get_smart_bin_status(self) -> List[Dict[str, Any]]:
        """Return current status of all monitored smart bins."""
        bins = []
        for b in SMART_BINS:
            fill     = _seed_fill(b["id"])
            status   = _get_bin_status(fill)
            overflow = _predict_overflow(fill, b["type"])
            temp     = round(28 + (fill / 100) * 12, 1)   # higher temp when fuller

            bins.append({
                "bin_id":           b["id"],
                "location":         b["location"],
                "waste_type":       b["type"],
                "category_color":   CATEGORY_COLORS.get(b["type"], "#94a3b8"),
                "fill_level_pct":   fill,
                "status":           status["status"],
                "status_color":     status["color"],
                "temperature_c":    temp,
                "collection_status":"Scheduled" if fill > 70 else "Normal",
                "bin_health":       "Good" if fill < 85 and temp < 38 else ("Warning" if fill < 95 else "Critical"),
                "overflow_prediction": overflow,
                "coordinates":      {"lat": b["lat"], "lon": b["lon"]},
            })

        # Sort: urgent bins first
        bins.sort(key=lambda x: x["fill_level_pct"], reverse=True)
        return bins

    def optimize_collection_routes(self, bins: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate optimized collection schedule and route assignments.
        Prioritize urgent bins (fill > 80%) for immediate dispatch.
        """
        urgent_bin_ids = {b["bin_id"] for b in bins if b["fill_level_pct"] >= 80}

        routes_output = []
        total_distance   = 0.0
        total_bins       = 0
        skipped_distance = 0.0

        for route in COLLECTION_ROUTES:
            urgent_in_route   = [bid for bid in route["bins"] if bid in urgent_bin_ids]
            priority          = "URGENT" if urgent_in_route else "ROUTINE"
            schedule          = "Today — Immediate" if urgent_in_route else "Next Scheduled Day"
            effective_dist    = route["distance_km"] if urgent_in_route else route["distance_km"] * 0.0
            total_distance   += route["distance_km"]
            total_bins       += len(route["bins"])
            skipped_distance += route["distance_km"] * (0 if urgent_in_route else 1)

            routes_output.append({
                "route_id":         route["route_id"],
                "route_name":       route["name"],
                "bins_assigned":    route["bins"],
                "urgent_bins":      urgent_in_route,
                "priority":         priority,
                "distance_km":      route["distance_km"],
                "collection_schedule": schedule,
                "estimated_time_min": round(route["distance_km"] * 5),   # ~12 km/h average
            })

        fuel_per_km   = 0.35     # L/km diesel
        co2_per_litre = 2.68     # kg CO2/L
        fuel_saved    = round(skipped_distance * fuel_per_km, 2)
        co2_saved     = round(fuel_saved * co2_per_litre, 2)
        time_saved_min= round(skipped_distance / 12 * 60, 0)

        return {
            "routes":              routes_output,
            "total_bins_monitored":total_bins,
            "total_route_distance_km": total_distance,
            "urgent_collections":  len(urgent_bin_ids),
            "optimization_savings":{
                "fuel_saved_litres": fuel_saved,
                "co2_saved_kg":      co2_saved,
                "time_saved_minutes":time_saved_min,
            },
            "xai_reason": (
                f"{len(urgent_bin_ids)} bins require urgent collection (fill > 80%). "
                f"Skipping non-urgent routes today saves {fuel_saved} L fuel and "
                f"{co2_saved} kg CO2 emissions."
            ),
        }

    def get_collection_summary(self) -> Dict[str, Any]:
        bins   = self.get_smart_bin_status()
        routes = self.optimize_collection_routes(bins)
        return {
            "smart_bins":     bins,
            "route_optimization": routes,
        }


collection_engine = CollectionEngine()
