"""
insights_engine.py
==================
Generates dynamic, natural-language intelligence insights based on filtered DataFrame analytics.
Each insight returns a structured dictionary (text, icon, theme badge).
"""

import pandas as pd
import numpy as np
from analysis.trend_analysis import detect_peak_months, find_fastest_growing_category

def generate_dashboard_insights(df: pd.DataFrame) -> list:
    """
    Synthesizes natural-language business intelligence statements based on Pandas aggregates.
    Returns 5 structured insights cards with custom icons and neon glow class mappings.
    """
    insights = []
    
    if len(df) == 0:
        return [
            {
                "id": "empty",
                "title": "No Crime Data Isolated",
                "text": "Filter query constraints yielded zero active records. Analytical insights are currently suspended.",
                "icon": "fa-solid fa-triangle-exclamation",
                "badge": "rose"
            }
        ]
        
    # ── 1. Geolocation Hotspot Epicenter ────────────────────────────────────────
    if "City" in df.columns:
        city_counts = df["City"].value_counts()
        if len(city_counts) > 0:
            top_city = city_counts.index[0]
            top_count = city_counts.values[0]
            city_pct = (top_count / len(df)) * 100
            insights.append({
                "id": "hotspot_epicenter",
                "title": " हॉटस्पॉट / HOTSPOT EPICENTER",
                "text": f"{top_city.upper()} isolated the highest crime concentration with {top_count:,} recorded incidents, representing {city_pct:.1f}% of overall filtered caseloads.",
                "icon": "fa-solid fa-map-location-dot",
                "badge": "rose"
            })
            
    # ── 2. Primary Offense Dominance ────────────────────────────────────────────
    if "Crime Description" in df.columns:
        crime_counts = df["Crime Description"].value_counts()
        if len(crime_counts) > 0:
            top_crime = crime_counts.index[0]
            top_count = crime_counts.values[0]
            crime_pct = (top_count / len(df)) * 100
            insights.append({
                "id": "primary_offense",
                "title": "अपराध विश्लेषण / OFFENSE ANALYSIS",
                "text": f"{top_crime.upper()} remains the dominant category in current logs, accounting for {crime_pct:.1f}% ({top_count:,} cases) of isolated security profiles.",
                "icon": "fa-solid fa-shapes",
                "badge": "purple"
            })
            
    # ── 3. Peak Seasonal Density ────────────────────────────────────────────────
    peak_months = detect_peak_months(df)
    if peak_months:
        months_str = " and ".join(peak_months).upper()
        insights.append({
            "id": "peak_season",
            "title": "मौसमी प्रवृत्ति / SEASONAL DENSITY",
            "text": f"Incident frequency peaks significantly during {months_str}, suggesting recurring seasonal spikes that warrant adjusted operational deployment.",
            "icon": "fa-regular fa-calendar-days",
            "badge": "yellow"
        })
        
    # ── 4. Fastest Growing Caseloads (YoY) ──────────────────────────────────────
    growth_info = find_fastest_growing_category(df)
    if growth_info and growth_info["category"] != "N/A":
        cat = growth_info["category"].upper()
        rate = growth_info["growth"]
        if rate > 0:
            msg = f"{cat} cases isolated the fastest YoY acceleration, climbing sharply by {rate}% over the last active interval."
        elif growth_info.get("is_fallback", False):
            msg = f"{cat} cases represent the main high-growth baseline threat vector in current active intervals."
        else:
            msg = f"{cat} cases remain stabilized as a persistent analytical threat with steady caseload counts."
            
        insights.append({
            "id": "growing_threat",
            "title": "विकास विश्लेषण / THREAT ACCELERATION",
            "text": msg,
            "icon": "fa-solid fa-arrow-trend-up",
            "badge": "cyan"
        })
        
    # ── 5. Weapon Tactics Index ─────────────────────────────────────────────────
    if "Weapon Used" in df.columns:
        weapon_counts = df["Weapon Used"].value_counts()
        if len(weapon_counts) > 0:
            top_weapon = weapon_counts.index[0]
            top_count = weapon_counts.values[0]
            # Map weapon names to strings
            weapon_name = top_weapon.upper()
            if weapon_name == "None" or weapon_name == "Unknown":
                weapon_name = "UNARMED / PHYSICAL FORCE"
            insights.append({
                "id": "tactical_means",
                "title": "हथियार प्रवृत्ति / TACTICAL THREAT INDEX",
                "text": f"{weapon_name} dominates tactical offense execution logs, suggesting immediate patrol security and containment adjustments.",
                "icon": "fa-solid fa-gun",
                "badge": "emerald"
            })
            
    return insights
