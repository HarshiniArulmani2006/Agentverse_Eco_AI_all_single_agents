import json
import logging
import requests
from config import Config
from rag_engine import rag_engine

logger = logging.getLogger(__name__)

# Fallback knowledge bank structured by topic & subtopic for offline or API-unavailable mode
FALLBACK_KNOWLEDGE_BANK = {
    "fertilizer": {
        "answer": "Natural fertilizers and bio-tonics nourish soil microorganisms instead of feeding chemical salts directly to plants. 'Jeevamrutham' (fermented cow dung, urine, jaggery, pulse flour) multiplies beneficial soil microbes from thousands to millions in 48 hours. 'Beejamrutham' is used for organic seed treatment, while vermicompost provides slow-release humic matter.",
        "tip": "Apply liquid Jeevamrutham (diluted 1:10 with water) near root zones every 14 days during active crop growth.",
        "action": "Mix 1kg fresh cow dung, 1L cow urine, 100g jaggery, and 100g pulse flour in 10L water; ferment for 48 hours to create a high-potency soil microbe tonic."
    },
    "pest_control": {
        "answer": "Natural pest control relies on botanical bio-repellents and biological predators rather than toxic synthetic chemicals. Cold-pressed Neem Oil Spray (5ml oil + 2ml liquid soap per liter of warm water) disrupts pest feeding and reproduction without harming bees. For severe chewing caterpillars or borers, 'Agniastra' (boiled cow urine, neem, green chili, garlic) acts as a powerful botanical insecticide.",
        "tip": "Install yellow and blue sticky traps at canopy level to trap thrips, whiteflies, and aphids naturally before infestations spread.",
        "action": "Prepare Neem Bio-Spray: Mix 5ml pure cold-pressed neem oil with 2ml organic liquid soap in 1L warm water. Spray thoroughly on leaf undersides in the evening."
    },
    "composting": {
        "answer": "Aerobic composting converts kitchen scraps and biomass into nutrient-rich humus. Maintaining a ratio of 3 parts Brown biomass (dry leaves, straw, cardboard for Carbon) to 1 part Green biomass (vegetable peels, fruit scraps for Nitrogen) ensures fast, odorless decomposition.",
        "tip": "Keep the compost pile moist like a wrung-out sponge and turn it every 7-10 days to supply oxygen to aerobic microbes.",
        "action": "Start a 3:1 brown-to-green compost bin today using dry yard leaves and raw kitchen vegetable trimmings."
    },
    "soil_health": {
        "answer": "Soil health is maintained through organic mulching (covering soil with dry leaves or straw), zero chemical tillage, and intercropping with nitrogen-fixing legumes. Mulching conserves 50%+ soil moisture, prevents weed germination, and nurtures earthworms.",
        "tip": "Never leave agricultural soil bare; exposed soil bakes under UV light, killing beneficial soil microbes.",
        "action": "Spread a 2-to-3 inch mulch layer of dry leaves or straw around plant bases to retain moisture and foster soil ecology."
    },
    "crops_tomatoes": {
        "answer": "Growing tomatoes naturally requires well-drained loamy soil (pH 6.0-6.8) and 6-8 hours of direct sunlight. Water deeply twice a week at root level (avoid soaking foliage to prevent leaf blight). Plant basil or marigolds as companion plants to repel tomato hornworms and nematodes naturally.",
        "tip": "Prune lower sucker shoots and support vines with wooden stakes or trellises for optimal air circulation.",
        "action": "Plant marigold flowers near your tomato plants as a natural root nematode deterrent."
    },
    "fungicide_disease": {
        "answer": "Fungal crop diseases like powdery mildew, rust, and leaf spot can be controlled naturally using sour fermented buttermilk spray. Dilute 100ml of 4-day fermented sour buttermilk in 1L water. The lactic acid bacteria outcompete fungal pathogens on leaf surfaces.",
        "tip": "Spray sour buttermilk or copper-infused buttermilk in early morning hours to prevent leaf mildew during humid monsoon weather.",
        "action": "Ferment 100ml buttermilk for 4 days in shade, dilute in 1L fresh water, and spray over foliage exhibiting white powdery spots."
    },
    "farming": {
        "answer": "Natural farming (Zero Budget Natural Farming / Rishi Krishi) eliminates synthetic chemical inputs and artificial fertilizers. It relies on Jeevamrutham bio-stimulants, organic straw mulching, intercropping, and minimum tillage to restore living soil ecology.",
        "tip": "Intercrop legumes (beans, pulses) with main cereal or vegetable crops to naturally fix atmospheric nitrogen into the soil.",
        "action": "Replace chemical fertilizers with Jeevamrutham soil tonic and straw mulch for your garden or farm."
    },
    "climate": {
        "answer": "Climate change refers to long-term global warming caused primarily by heat-trapping greenhouse gases (CO2, CH4, N2O) from fossil fuel burning, industrial emissions, and deforestation.",
        "tip": "Switching to renewable power, eating plant-forward meals, and reducing energy waste dramatically lowers personal carbon footprints.",
        "action": "Unplug idle phantom electronics and switch household lighting to high-efficiency LED bulbs."
    },
    "pollution": {
        "answer": "Plastic and industrial pollution degrades terrestrial and marine ecosystems. Single-use plastics take 500-1000 years to breakdown into harmful microplastics entering the human food chain.",
        "tip": "Eliminate single-use shopping bags, disposable plastic water bottles, and plastic cutlery.",
        "action": "Carry a stainless steel water bottle and reusable canvas tote bag whenever leaving home."
    },
    "water": {
        "answer": "Freshwater conservation requires efficient irrigation (drip and micro-sprinklers) and rainwater harvesting. Drip irrigation reduces water evaporation and weed growth by up to 80%.",
        "tip": "Fixing a single dripping faucet saves over 3,000 liters of potable water per year.",
        "action": "Install low-flow aerators on kitchen taps and collect vegetable rinsing water to irrigate potted plants."
    },
    "biodiversity": {
        "answer": "Biodiversity encompasses the variety of living species (plants, pollinators, fungi, micro-organisms) sustaining life-support systems on Earth.",
        "tip": "Planting native flowering plants provides essential nectar and habitat for local honeybees and butterflies.",
        "action": "Plant a small pollinator garden with native flowering plants on your balcony or yard."
    },
    "energy": {
        "answer": "Renewable energy from solar photovoltaics, wind turbines, and micro-hydro supplies clean energy without greenhouse gas emissions.",
        "tip": "Rooftop solar water heaters cut domestic electricity demands significantly.",
        "action": "Upgrade to 5-star energy efficient inverter appliances and consider rooftop solar panels."
    }
}

class EcoGuideAgent:
    def __init__(self):
        self.groq_api_key = Config.GROQ_API_KEY

    def generate_response(self, user_query, language="en"):
        # 1. Retrieve RAG context
        rag_results = rag_engine.search(user_query, top_k=2)
        context_str = "\n---\n".join([r["content"] for r in rag_results]) if rag_results else "No explicit context match."

        # 2. Try Groq API if key is present
        if self.groq_api_key and len(self.groq_api_key) > 5:
            try:
                system_prompt = (
                    "You are EcoGuide AI, a warm, highly knowledgeable, beginner-friendly environmental mentor and natural farming expert. "
                    "Provide a specific, accurate, and detailed response tailored strictly to the user's exact query. "
                    "Whether the user asks about organic fertilizers, pest control, crop management, soil health, composting, water conservation, or climate change, analyze their exact question and generate a specific answer. "
                    "Your output MUST be a strict JSON object with exactly three keys:\n"
                    '{\n  "answer": "<detailed specific educational explanation>",\n  "tip": "<actionable environmental or farming tip>",\n  "action": "<practical concrete action step the user can take>"\n}\n'
                    f"Language requested: {language}. If language is 'ta', translate the response to clear Tamil language."
                )

                user_prompt_full = f"User Query: {user_query}\n\nRetrieved Knowledge Base Context:\n{context_str}"

                headers = {
                    "Authorization": f"Bearer {self.groq_api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt_full}
                    ],
                    "temperature": 0.5,
                    "max_tokens": 800,
                    "response_format": {"type": "json_object"}
                }

                res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=10)
                if res.status_code == 200:
                    data = res.json()
                    content = data["choices"][0]["message"]["content"]
                    parsed = json.loads(content)
                    return {
                        "answer": parsed.get("answer", "Here is your detailed environmental explanation."),
                        "tip": parsed.get("tip", "Remember to practice sustainable eco-friendly habits!"),
                        "action": parsed.get("action", "Start by implementing this organic step today."),
                        "source": "groq_rag"
                    }
            except Exception as e:
                logger.error(f"Groq API call error: {e}")

        # 3. Intelligent dynamic topic matcher (Offline / Fallback engine)
        q_lower = user_query.lower()

        matched_category = "farming"
        if any(w in q_lower for w in ["fertiliz", "jeevamrutham", "beejamrutham", "panchagavya", "vermicompost", "bio-char", "tonic", "nutrient", "dung", "jaggery"]):
            matched_category = "fertilizer"
        elif any(w in q_lower for w in ["pest", "aphid", "borer", "caterpillar", "bug", "insect", "neem", "agniastra", "brahmastra", "trap", "spray", "fly", "thrip", "worm"]):
            matched_category = "pest_control"
        elif any(w in q_lower for w in ["fung", "blight", "mildew", "rust", "curling", "disease", "rot", "buttermilk", "wilt"]):
            matched_category = "fungicide_disease"
        elif any(w in q_lower for w in ["compost", "kitchen waste", "scraps", "browns", "greens", "layering", "humus"]):
            matched_category = "composting"
        elif any(w in q_lower for w in ["soil", "mulch", "tillage", "earthworm", "microbe", "cover crop", "erosi"]):
            matched_category = "soil_health"
        elif any(w in q_lower for w in ["tomato", "eggplant", "brinjal", "chili", "chilli", "crop", "vegetable", "plant", "stake", "prun"]):
            matched_category = "crops_tomatoes"
        elif any(w in q_lower for w in ["pollut", "plastic", "waste", "garbage", "smog", "ocean"]):
            matched_category = "pollution"
        elif any(w in q_lower for w in ["water", "rain", "drip", "river", "irrigat", "faucet"]):
            matched_category = "water"
        elif any(w in q_lower for w in ["bio", "species", "animal", "forest", "tree", "bee", "pollinator"]):
            matched_category = "biodiversity"
        elif any(w in q_lower for w in ["sol", "wind", "energy", "power", "renew", "electricity"]):
            matched_category = "energy"
        elif any(w in q_lower for w in ["climat", "warming", "carbon", "co2", "emiss", "fossil"]):
            matched_category = "climate"

        base_res = dict(FALLBACK_KNOWLEDGE_BANK[matched_category])

        if rag_results:
            # Enrich answer with top context snippet if available
            snippet = rag_results[0]["content"].split("\n")[0].replace("=", "").strip()
            base_res["answer"] = f"{base_res['answer']} RAG Knowledge: {snippet}"

        # Tamil translation fallback handling
        if language == "ta":
            base_res = {
                "answer": f"தமிழ் விளக்கம்: {base_res['answer']}",
                "tip": f"சுற்றுச்சூழல் / விவசாய குறிப்பு: {base_res['tip']}",
                "action": f"நடவடிக்கை: {base_res['action']}",
                "source": "rag_fallback_ta"
            }
        else:
            base_res["source"] = "rag_fallback"

        return base_res

eco_agent = EcoGuideAgent()
