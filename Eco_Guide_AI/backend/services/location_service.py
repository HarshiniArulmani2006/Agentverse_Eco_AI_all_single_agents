"""
WildGuard AI – Location Intelligence Service
Provides wildlife and biodiversity information for specific locations.
"""
import logging
from core.gemini_client import gemini

logger = logging.getLogger(__name__)


def get_location_wildlife_report(location: str) -> str:
    """
    Generate a detailed wildlife intelligence report for a specific location.
    """
    prompt = f"""
Generate a comprehensive Wildlife and Biodiversity Intelligence Report for: **{location}**

## 🌍 Location Wildlife Report: {location}

Please provide a detailed, scientifically accurate report covering ALL of the following sections:

### 1. 🗺️ Geographic & Ecological Overview
- Geographic context (region, terrain, climate zone)
- Major ecosystems present
- Biodiversity significance (is it a hotspot, endemic region, etc.)

### 2. 🦁 Common Wildlife Species
List at least 8-10 species with:
- Common Name | Scientific Name | IUCN Status | Brief note

### 3. 🔴 Threatened & Endangered Species
Focus on Critically Endangered, Endangered, and Vulnerable species found here:
- Species name | IUCN Category | Population estimate | Key threats

### 4. 🌿 Flora & Vegetation
- Dominant plant communities
- Notable/endemic plant species
- Forest types present

### 5. 🏞️ Protected Areas & Conservation Zones
List National Parks, Wildlife Sanctuaries, Biosphere Reserves, Ramsar Sites, UNESCO sites nearby:
- Area name | Type | Area (km²) | Key species protected

### 6. 🏔️ Biodiversity Hotspots
- Is this area part of a globally recognized biodiversity hotspot?
- What makes it ecologically significant?

### 7. ⚠️ Environmental Threats
- Deforestation and land use change
- Pollution levels
- Human-wildlife conflict
- Climate change impacts
- Invasive species

### 8. 🌱 Active Conservation Projects
- Government programmes
- NGO initiatives
- Community conservation efforts
- Research stations

### 9. 🦋 Seasonal Wildlife Calendar
- Best seasons to observe different species
- Migration events
- Breeding seasons

### 10. 📊 Biodiversity Statistics
- Number of recorded species (birds, mammals, reptiles, plants)
- Endemism rate
- Forest cover percentage

### 📚 Sources
Cite IUCN, GBIF, WWF, Forest Survey of India, state wildlife departments, or relevant national databases.

Be specific to {location} – avoid generic responses. Use real species and real conservation data.
"""
    return gemini.generate_structured(prompt)


def get_nearby_protected_areas(location: str) -> str:
    """Get information about protected areas near a location."""
    prompt = f"""
List all Protected Areas (National Parks, Wildlife Sanctuaries, Biosphere Reserves, Ramsar Sites, Conservation Reserves) within or near {location}.

For each area provide:
- Name | Type | Established Year | Area | Key Species | UNESCO/Ramsar Status

Format as a structured table followed by brief descriptions of the top 3 most important areas.
"""
    return gemini.generate_structured(prompt)
