"""
WildGuard AI – Vision Service
Handles image analysis for species identification and habitat assessment.
"""
import base64
import logging
from typing import Optional

from core.gemini_client import gemini

logger = logging.getLogger(__name__)

SPECIES_ID_PROMPT = """
You are performing expert wildlife species identification from the provided image.

Please analyze this image and return a structured identification report in this exact format:

## 🔬 Species Identification Report

### 🏆 Primary Identification
| Field | Value |
|---|---|
| **Common Name** | [Name] |
| **Scientific Name** | *[Genus species]* |
| **Kingdom** | [Kingdom] |
| **Phylum** | [Phylum] |
| **Class** | [Class] |
| **Order** | [Order] |
| **Family** | [Family] |
| **Genus** | [Genus] |

### 📊 Confidence Analysis
- **Primary Match Confidence**: [X]%
- **Confidence Level**: [High / Medium / Low]
- **Reasoning**: [Explain key visual features that led to this identification]

### 🌍 Distribution & Habitat
- **Native Regions**: [List countries/regions]
- **Habitat**: [Describe typical habitat]
- **Geographic Range**: [Describe range]

### 🔴 Conservation Status
- **IUCN Status**: [Status with category, e.g., Endangered (EN)]
- **Population Trend**: [Increasing / Stable / Decreasing / Unknown]
- **Key Threats**: [List 2-3 main threats]

### 🔄 Alternative Predictions
| # | Species | Confidence |
|---|---|---|
| 1 | [Name] (*[Sci Name]*) | [X]% |
| 2 | [Name] (*[Sci Name]*) | [X]% |
| 3 | [Name] (*[Sci Name]*) | [X]% |

### 🌿 Ecological Role
[Brief description of this species' role in its ecosystem]

### 📚 Sources
[IUCN Red List / GBIF / other authoritative source]

---
*If you cannot confidently identify the species, state your uncertainty clearly and explain why.*
"""

HABITAT_ANALYSIS_PROMPT = """
You are a professional habitat ecologist analyzing this ecosystem image.

Provide a comprehensive habitat health assessment in this exact format:

## 🌿 Habitat Health Analysis Report

### 🗺️ Habitat Classification
- **Ecosystem Type**: [Forest / Grassland / Wetland / Desert / Marine / Freshwater / etc.]
- **Sub-type**: [Tropical rainforest / Temperate / Mangrove / etc.]
- **Approximate Location Type**: [Geographical context if visible]

### 📊 Health Metrics

| Metric | Score (0-100) | Assessment |
|---|---|---|
| **Vegetation Density** | [X]/100 | [Excellent/Good/Fair/Poor/Critical] |
| **Forest/Vegetation Cover** | [X]/100 | [Assessment] |
| **Water Availability** | [X]/100 | [Assessment] |
| **Biodiversity Signs** | [X]/100 | [Assessment] |
| **Pollution Indicators** | [X]/100 | [Assessment] |
| **Habitat Fragmentation** | [X]/100 | [Assessment] |

### 🏆 Overall Scores
- **🌿 Habitat Health Score**: [X]/100
- **⚠️ Ecological Risk Score**: [X]/100
- **🦋 Biodiversity Potential Score**: [X]/100

### 🔍 Key Observations
1. [Observation about vegetation]
2. [Observation about wildlife signs]
3. [Observation about disturbance or health]
4. [Observation about threats visible]

### ⚠️ Threats Detected
- [List visible threats: deforestation signs, invasive plants, water pollution, human encroachment, etc.]

### 🌱 Restoration Recommendations
1. **Immediate Actions**: [What should be done now]
2. **Short-term (1-3 years)**: [Actions]
3. **Long-term (5-10 years)**: [Actions]

### 🦜 Likely Wildlife
Species that would typically inhabit this ecosystem:
- [Species 1]
- [Species 2]
- [Species 3]

### 📚 Assessment Basis
[Scientific framework used: e.g., FAO Forest Assessment, Terrestrial Ecosystems Health Index]
"""


def identify_species_from_image(image_bytes: bytes, mime_type: str) -> str:
    """Identify species from an uploaded image."""
    return gemini.analyze_image(image_bytes, mime_type, SPECIES_ID_PROMPT)


def analyze_habitat_from_image(image_bytes: bytes, mime_type: str) -> str:
    """Perform habitat health analysis on an uploaded image."""
    return gemini.analyze_image(image_bytes, mime_type, HABITAT_ANALYSIS_PROMPT)


def analyze_sighting_image(
    image_bytes: bytes,
    mime_type: str,
    location: str,
    observer_notes: str = "",
) -> str:
    """Analyze an image in the context of a wildlife sighting report."""
    prompt = f"""
Analyze this wildlife sighting image.

Location provided: {location}
Observer notes: {observer_notes}

Please provide:
1. Species identification with confidence score
2. Rarity assessment for the region
3. Behavioral observations from the image
4. Conservation significance
5. Any red flags (out-of-range sighting, rare species, etc.)

Format as a structured sighting analysis report.
"""
    return gemini.analyze_image(image_bytes, mime_type, prompt)
