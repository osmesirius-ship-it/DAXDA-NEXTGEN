"""DAXDA V11.4 Treasure Encoder

Replaces the security-focused SemanticEncoder with a geographic feature extractor.
Maps verse text into Clifford Cl(2,0) multivector dimensions:

    s   = Geographic Certainty  (how many identifiable features are present)
    e1  = Latitude Signal       (north/south indicators, known city anchors)
    e2  = Longitude Signal      (east/west indicators, known city anchors)
    e12 = Temporal Anchor       (historical dates, named persons, eras)

The stronger and more specific the geographic signal in the text,
the further the initial multivector M_0 deviates from the identity state,
giving the 16-layer transport more differentiated structure to work with.
"""

import re
import math
from typing import Dict, Any, List, Optional
from cl20 import MV


# =============================================================
# GEOGRAPHIC FEATURE DICTIONARIES
# =============================================================

# Cardinal direction keywords → latitude/longitude nudges
CARDINAL = {
    # North pushes latitude positive
    "north": (0.15, 0.0), "northern": (0.12, 0.0), "arctic": (0.2, 0.0),
    # South pushes latitude negative
    "south": (-0.15, 0.0), "southern": (-0.12, 0.0),
    # East pushes longitude positive (toward 0° from negative US longitudes)
    "east": (0.0, 0.12), "eastern": (0.0, 0.10),
    # West pushes longitude negative
    "west": (0.0, -0.12), "western": (0.0, -0.10),
}

# Known city/location anchors with approximate lat/lon
CITY_ANCHORS = {
    "new york": (40.71, -74.01), "manhattan": (40.78, -73.97), "brooklyn": (40.65, -73.95),
    "broadway": (40.76, -73.98), "central park": (40.78, -73.97), "battery park": (40.70, -74.02),
    "new orleans": (29.95, -90.07), "french quarter": (29.96, -90.06),
    "montreal": (45.50, -73.57), "mount royal": (45.51, -73.59),
    "st. augustine": (29.89, -81.31), "saint augustine": (29.89, -81.31),
    "san francisco": (37.77, -122.42), "golden gate": (37.82, -122.47),
    "milwaukee": (43.04, -87.91), "lake park": (43.08, -87.87),
    "houston": (29.76, -95.37), "galveston": (29.30, -94.80),
    "roanoke": (35.87, -75.67), "roanoke island": (35.87, -75.67),
    "charleston": (32.78, -79.93), "battery charleston": (32.77, -79.93),
    "chicago": (41.88, -87.62), "grant park": (41.87, -87.62),
    "cleveland": (41.50, -81.69), "boston": (42.36, -71.06),
    "rocky mountains": (39.75, -105.50), "rockies": (39.75, -105.50),
    "appalachian": (37.00, -81.00), "vermont": (43.60, -72.58),
    "little rock pond": (43.36, -72.95),
    "indies": (40.71, -74.01),  # West Indies → Hamilton → NYC
    "liberty": (40.69, -74.04), "bedloe": (40.69, -74.04),
}

# Landmark feature keywords → certainty boost
LANDMARK_KEYWORDS = [
    "park", "bridge", "statue", "monument", "tower", "fountain", "gate",
    "garden", "plaza", "square", "church", "cemetery", "courthouse",
    "lighthouse", "pier", "dock", "harbor", "fort", "fortress", "citadel",
    "museum", "library", "school", "university", "college", "capitol",
    "island", "lake", "river", "creek", "pond", "mountain", "hill",
    "trail", "path", "road", "street", "avenue", "boulevard",
]

# Distance/pacing keywords → certainty boost (someone is giving directions)
DISTANCE_KEYWORDS = [
    "paces", "steps", "walk", "stride", "feet", "yards", "miles",
    "rows", "twelve", "hundred", "fifteen", "twenty", "thirteen",
]

# Historical/temporal keywords → e12 (temporal anchor)
TEMPORAL_KEYWORDS = [
    "century", "ancient", "old", "historic", "1913", "1982", "december",
    "january", "february", "march", "april", "may", "june", "july",
    "august", "september", "october", "november",
    "freedom", "revolution", "civil", "war", "colonial", "native",
]

# Named historical persons → certainty + temporal boost
NAMED_PERSONS = {
    "gershwin": (40.69, -73.98),    # Brooklyn
    "hamilton": (40.80, -73.96),     # Hamilton Grange, NYC
    "twain": (37.77, -122.42),      # Mark Twain → San Francisco
    "columbus": (29.95, -90.07),     # Christopher Columbus → New Orleans
    "webster": (40.71, -74.01),      # Noah Webster → NYC
    "edwin": (29.89, -81.31),        # Edwin → St. Augustine
    "oz": (35.87, -75.67),           # Man of Oz → Roanoke area
    "fenn": (39.75, -105.50),        # Forrest Fenn → Rocky Mountains
    "thucydides": (42.36, -71.06),   # Greek historian → Boston
    "xenophon": (42.36, -71.06),     # Greek historian → Boston
}

# Environmental features → differentiation signal
ENVIRONMENT_KEYWORDS = {
    "water": 0.08, "ocean": 0.10, "sea": 0.10, "river": 0.08,
    "sand": 0.06, "stone": 0.05, "granite": 0.07, "limestone": 0.06,
    "tree": 0.05, "forest": 0.07, "wood": 0.05, "palm": 0.08,
    "wind": 0.04, "grass": 0.04, "bird": 0.05, "shell": 0.06,
    "salt": 0.05, "silver": 0.04, "jewel": 0.08, "gem": 0.08,
    "star": 0.05, "moon": 0.04, "night": 0.04, "shadow": 0.05,
    "iron": 0.05, "metal": 0.05, "brick": 0.04, "fence": 0.05,
}


# =============================================================
# ENCODING FUNCTIONS
# =============================================================

def f_certainty(landmark_count: float, distance_count: float, person_count: float) -> float:
    """s = Geographic Certainty. More identifiable features → higher certainty."""
    base = 1.0
    return base + 0.10 * landmark_count + 0.15 * distance_count + 0.20 * person_count

def f_latitude(lat_signals: List[float]) -> float:
    """e1 = Latitude Signal. Average of all latitude nudges."""
    if not lat_signals:
        return 0.0
    return sum(lat_signals) / len(lat_signals)

def f_longitude(lon_signals: List[float]) -> float:
    """e2 = Longitude Signal. Average of all longitude nudges."""
    if not lon_signals:
        return 0.0
    return sum(lon_signals) / len(lon_signals)

def f_temporal(temporal_count: float, env_signal: float) -> float:
    """e12 = Temporal/Historical Anchor. More dates and historical refs → stronger."""
    return 0.10 * temporal_count + env_signal


class TreasureEncoder:
    """Extracts geographic features from verse text and encodes into Cl(2,0) multivector."""

    def encode(self, verse_text: str, context: str = "", sources: Optional[List[Dict]] = None) -> Dict[str, Any]:
        text = (verse_text + " " + context).lower()
        
        lat_signals = []
        lon_signals = []
        landmark_count = 0
        distance_count = 0
        temporal_count = 0
        person_count = 0
        env_signal = 0.0
        city_lat_anchors = []
        city_lon_anchors = []
        
        # 1. Cardinal directions
        for word, (lat_nudge, lon_nudge) in CARDINAL.items():
            matches = len(re.findall(r'\b' + word + r'\b', text))
            if matches > 0:
                lat_signals.extend([lat_nudge] * matches)
                lon_signals.extend([lon_nudge] * matches)
        
        # 2. City/location anchors
        for city, (lat, lon) in CITY_ANCHORS.items():
            if city in text:
                # Normalize lat/lon to a signal range roughly [-1, 1]
                city_lat_anchors.append(lat / 45.0)  # normalize to ~[-1, 1]
                city_lon_anchors.append(lon / 120.0)  # normalize to ~[-1, 1]
                landmark_count += 2  # cities are strong landmarks
        
        # 3. Named persons
        for person, (lat, lon) in NAMED_PERSONS.items():
            if person in text:
                city_lat_anchors.append(lat / 45.0)
                city_lon_anchors.append(lon / 120.0)
                person_count += 1
        
        # 4. Landmark keywords
        for kw in LANDMARK_KEYWORDS:
            matches = len(re.findall(r'\b' + kw + r'\b', text))
            landmark_count += matches
        
        # 5. Distance keywords
        for kw in DISTANCE_KEYWORDS:
            matches = len(re.findall(r'\b' + kw + r'\b', text))
            distance_count += matches
        
        # 6. Temporal keywords
        for kw in TEMPORAL_KEYWORDS:
            matches = len(re.findall(r'\b' + kw + r'\b', text))
            temporal_count += matches
        
        # 7. Environmental features
        for kw, weight in ENVIRONMENT_KEYWORDS.items():
            if re.search(r'\b' + kw + r'\b', text):
                env_signal += weight
        
        # Combine city anchors with cardinal signals
        lat_signals.extend(city_lat_anchors)
        lon_signals.extend(city_lon_anchors)
        
        # Build the multivector
        s_val = f_certainty(landmark_count, distance_count, person_count)
        e1_val = f_latitude(lat_signals)
        e2_val = f_longitude(lon_signals)
        e12_val = f_temporal(temporal_count, env_signal)
        
        M_0 = MV(s=s_val, e1=e1_val, e2=e2_val, e12=e12_val)
        
        # Build parameters for the transport layer
        parameters = {
            "severe": 0.0,  # No security risk in treasure verses
            "caution": env_signal,
            "provenance": 0.0,
            "contradiction": 0.0,
            "evidence": min(landmark_count + person_count, 10) / 10.0,
            # Treasure-specific parameters
            "landmark_count": landmark_count,
            "distance_count": distance_count,
            "temporal_count": temporal_count,
            "person_count": person_count,
            "env_signal": env_signal,
            "lat_signal_count": len(lat_signals),
            "lon_signal_count": len(lon_signals),
        }
        
        return {
            "initial_encoded": M_0,
            "parameters": parameters,
            "feature_summary": {
                "landmarks": landmark_count,
                "distances": distance_count,
                "temporal_refs": temporal_count,
                "named_persons": person_count,
                "env_signal": round(env_signal, 4),
                "lat_signals": len(lat_signals),
                "lon_signals": len(lon_signals),
                "city_anchors_found": len(city_lat_anchors),
            }
        }
