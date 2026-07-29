from flask import Blueprint, jsonify

learn_bp = Blueprint('learn', __name__)

LEARN_TOPICS = [
    {
        "id": "climate-change",
        "title": "Climate Change",
        "category": "Atmosphere",
        "icon": "CloudSun",
        "definition": "Long-term shifts in global or regional climate patterns, driven by human activities increasing greenhouse gas concentrations in the atmosphere.",
        "causes": [
            "Combustion of coal, oil, and natural gas for energy",
            "Deforestation and destruction of natural carbon sinks",
            "Industrial farming and heavy methane emissions from livestock",
            "Uncontrolled landfill decomposition releasing greenhouse gases"
        ],
        "effects": [
            "Rising global surface temperatures and heatwaves",
            "Melting polar ice sheets leading to sea-level rise",
            "Extreme weather events like super-cyclones and mega-droughts",
            "Disruption of marine ecosystems and food security"
        ],
        "prevention": [
            "Transition to 100% renewable energy grids",
            "Large-scale reforestation and ecosystem restoration",
            "Enforcing carbon pricing and industrial emission caps",
            "Adopting circular economy and zero-waste lifestyles"
        ],
        "examples": [
            "Costa Rica generating over 98% of its electricity from renewable sources.",
            "The Great Green Wall initiative in Africa planting trees across the Sahel."
        ]
    },
    {
        "id": "global-warming",
        "title": "Global Warming",
        "category": "Atmosphere",
        "icon": "Thermometer",
        "definition": "The rapid increase in Earth's average surface temperature over the past century due to greenhouse gases trapping thermal radiation.",
        "causes": [
            "Excessive carbon dioxide accumulation in the atmosphere",
            "Release of potent fluorinated synthetic gases in cooling systems",
            "Widespread clearance of primary rainforests for cattle ranching"
        ],
        "effects": [
            "Glacial retreat in Himalayas, Alps, and Andes",
            "Unprecedented ocean warming causing coral reef bleaching",
            "Shift in animal migration and plant flowering times"
        ],
        "prevention": [
            "Phasing out coal-fired power plants worldwide",
            "Improving building insulation to cut heating/cooling loss",
            "Adopting electric transit powered by solar and wind energy"
        ],
        "examples": [
            "The Paris Agreement aiming to limit global temperature rise below 1.5°C.",
            "Deployment of offshore giant wind turbines in the North Sea."
        ]
    },
    {
        "id": "pollution",
        "title": "Environmental Pollution",
        "category": "Environment",
        "icon": "Wind",
        "definition": "The introduction of harmful contaminants into the natural environment, causing adverse changes to air, water, soil, and wildlife.",
        "causes": [
            "Untreated industrial effluent and sewage discharge into waterways",
            "Vehicle exhaust gases containing toxic PM2.5 particulates",
            "Single-use plastic accumulation in oceans and landfills",
            "Agricultural runoff loaded with synthetic pesticides"
        ],
        "effects": [
            "Respiratory diseases, lung damage, and premature death in humans",
            "Mass aquatic die-offs due to toxic algal blooms and microplastics",
            "Loss of fertile arable land and groundwater contamination"
        ],
        "prevention": [
            "Mandating Zero Liquid Discharge (ZLD) in factories",
            "Strict plastic packaging bans and zero-waste recycling",
            "Promoting electric vehicles and low-emission urban zones"
        ],
        "examples": [
            "The cleaning of Europe's Rhine River through strict anti-pollution laws.",
            "Rwanda's nationwide ban on single-use plastic bags since 2008."
        ]
    },
    {
        "id": "biodiversity",
        "title": "Biodiversity Conservation",
        "category": "Ecology",
        "icon": "Leaf",
        "definition": "The protection and restoration of the variety of life on Earth, including species diversity, genetic variation, and delicate ecosystem habitats.",
        "causes": [
            "Habitat fragmentation due to highways, cities, and monoculture farms",
            "Poaching and illegal international trade in endangered species",
            "Invasive species outcompeting native plants and animals"
        ],
        "effects": [
            "Collapse of key ecosystem services like pollination and water purification",
            "Irreversible species extinction and loss of natural medicinal compounds",
            "Increased vulnerability of crops to destructive blights"
        ],
        "prevention": [
            "Creating protected wildlife corridors and marine reserves",
            "Restoring wetlands, mangroves, and degraded native forests",
            "Enforcing CITES anti-poaching regulations strictly"
        ],
        "examples": [
            "Project Tiger in India successfully doubling wild tiger populations.",
            "Mangrove restoration along the coasts of Indonesia protecting shorelines."
        ]
    },
    {
        "id": "renewable-energy",
        "title": "Renewable Energy",
        "category": "Technology",
        "icon": "Sun",
        "definition": "Clean energy produced from natural sources that naturally replenish faster than they are consumed, emitting zero carbon during operation.",
        "causes": [
            "Depletion of finite fossil fuel reserves",
            "Urgent global demand to decarbonize power generation"
        ],
        "effects": [
            "Drastic reduction in global carbon emissions",
            "Lower long-term electricity costs and cleaner urban air quality",
            "Job creation in solar, wind, and battery technology"
        ],
        "prevention": [
            "Government subsidies for rooftop solar installations",
            "Building grid-scale battery storage capacity for intermittent power",
            "Investing in green hydrogen electrolyzers for heavy transport"
        ],
        "examples": [
            "Bhadla Solar Park in Rajasthan, one of the world's largest solar installations.",
            "Denmark producing over 50% of its power from offshore wind turbines."
        ]
    },
    {
        "id": "water-conservation",
        "title": "Water Conservation",
        "category": "Resources",
        "icon": "Droplet",
        "definition": "Strategies, policies, and activities to sustainably manage freshwater resources and prevent water scarcity.",
        "causes": [
            "Over-pumping of underground aquifers for flood irrigation",
            "Massive urban water leakage from outdated piping networks",
            "Pollution rendering natural river water unfit for consumption"
        ],
        "effects": [
            "Severe drought conditions in agricultural belts",
            "Depletion of groundwater tables threatening drinking supply",
            "Salinization of coastal soil due to seawater intrusion"
        ],
        "prevention": [
            "Mandatory rooftop rainwater harvesting systems in cities",
            "Replacing flood irrigation with precision drip irrigation",
            "Installing low-flow plumbing fixtures in all residential buildings"
        ],
        "examples": [
            "Cape Town's successful 'Day Zero' water management campaign.",
            "Traditional Johads (earthen check dams) restoring rivers in rural India."
        ]
    },
    {
        "id": "sustainable-living",
        "title": "Sustainable Living",
        "category": "Lifestyle",
        "icon": "Recycle",
        "definition": "A lifestyle that attempts to reduce an individual's or society's use of Earth's natural resources and personal carbon footprint.",
        "causes": [
            "Over-consumption and single-use throwaway culture",
            "High carbon footprint from meat-heavy diets and fast fashion"
        ],
        "effects": [
            "Massive landfill overflow and ocean microplastic pollution",
            "Excessive resource extraction degrading natural landscapes"
        ],
        "prevention": [
            "Practicing the 5 Rs: Refuse, Reduce, Reuse, Repurpose, Recycle",
            "Switching to locally sourced, seasonal plant-rich meals",
            "Composting organic kitchen waste at home"
        ],
        "examples": [
            "Zero-waste grocery stores allowing customers to fill reusable containers.",
            "Urban community gardens transforming vacant lots into food hubs."
        ]
    }
]

@learn_bp.route('/api/learn/topics', methods=['GET'])
def get_learn_topics():
    return jsonify({
        "status": "success",
        "topics": LEARN_TOPICS
    })

@learn_bp.route('/api/learn/topic/<topic_id>', methods=['GET'])
def get_learn_topic_by_id(topic_id):
    topic = next((t for t in LEARN_TOPICS if t['id'] == topic_id), None)
    if not topic:
        return jsonify({"error": "Topic not found"}), 404
    return jsonify({
        "status": "success",
        "topic": topic
    })
