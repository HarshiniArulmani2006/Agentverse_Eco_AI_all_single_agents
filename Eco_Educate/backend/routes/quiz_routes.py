import random
from flask import Blueprint, request, jsonify
from database import db_manager

quiz_bp = Blueprint('quiz', __name__)

QUIZ_QUESTIONS_BANK = [
    {
        "id": 1,
        "question": "Which greenhouse gas accounts for the largest share of global human-made greenhouse emissions?",
        "options": ["Methane (CH4)", "Carbon Dioxide (CO2)", "Nitrous Oxide (N2O)", "Ozone (O3)"],
        "correctIndex": 1,
        "explanation": "Carbon Dioxide (CO2) makes up approximately 76% of total global greenhouse gas emissions."
    },
    {
        "id": 2,
        "question": "What is Jeevamrutham in natural farming?",
        "options": [
            "A synthetic chemical pesticide",
            "A bio-stimulant microbial tonic made from fermented cow dung, urine, jaggery, and pulse flour",
            "A hybrid genetically modified seed variety",
            "A synthetic plastic mulching sheet"
        ],
        "correctIndex": 1,
        "explanation": "Jeevamrutham multiplies beneficial soil microbes exponentially without chemical inputs."
    },
    {
        "id": 3,
        "question": "Which irrigation technique delivers water directly to root zones with up to 80% less evaporation?",
        "options": ["Flood Irrigation", "Drip Irrigation", "Canal Irrigation", "Overhead Sprinkler"],
        "correctIndex": 1,
        "explanation": "Drip irrigation delivers targeted water directly to plant root zones, conserving water dramatically."
    },
    {
        "id": 4,
        "question": "What primary driver causes Ocean Acidification?",
        "options": [
            "Excess absorption of atmospheric Carbon Dioxide (CO2) by seawater",
            "Plastic waste floating on ocean surfaces",
            "Solar radiation flares",
            "Underwater noise pollution from cargo ships"
        ],
        "correctIndex": 0,
        "explanation": "Oceans absorb nearly 30% of human CO2 emissions, forming carbonic acid and lowering ocean pH."
    },
    {
        "id": 5,
        "question": "What is the recommended ratio of Brown biomass (Carbon) to Green biomass (Nitrogen) in aerobic composting?",
        "options": ["1:10 ratio", "3:1 ratio (Carbon to Nitrogen)", "10:1 ratio", "5:5 ratio"],
        "correctIndex": 1,
        "explanation": "A 3:1 ratio of carbon-rich browns (dry leaves) to nitrogen-rich greens (peels) ensures rapid decomposition."
    },
    {
        "id": 6,
        "question": "What is the main function of Beejamrutham in natural farming?",
        "options": [
            "Weed suppression spray",
            "Organic seed coating to protect against fungal and seed-borne diseases",
            "Chemical nitrogen supply",
            "Fruit ripening agent"
        ],
        "correctIndex": 1,
        "explanation": "Beejamrutham treats seeds organically before sowing to shield against soil and seed-borne fungal spores."
    },
    {
        "id": 7,
        "question": "Which natural botanical preparation is widely used to control aphids, thrips, and spider mites naturally?",
        "options": ["Cold-Pressed Neem Oil Spray", "Synthetic Glyphosate", "Urea Solution", "Chlorpyrifos"],
        "correctIndex": 0,
        "explanation": "Neem oil spray disrupts insect hormone systems without harming beneficial pollinators like bees."
    },
    {
        "id": 8,
        "question": "Why is organic straw mulching crucial in natural farming?",
        "options": [
            "It makes soil completely sterile",
            "It retains soil moisture, regulates soil temperature, and feeds earthworms",
            "It increases chemical runoff",
            "It speeds up solar heat reflection"
        ],
        "correctIndex": 1,
        "explanation": "Mulching acts as a protective blanket, preserving soil moisture and encouraging earthworm activity."
    },
    {
        "id": 9,
        "question": "What percentage of modern prescription medicines originate from natural plant and fungal compounds?",
        "options": ["Over 50%", "Less than 5%", "Exactly 10%", "Around 90%"],
        "correctIndex": 0,
        "explanation": "Over 50% of prescription drugs are derived from natural compounds discovered in plants, fungi, and microbes."
    },
    {
        "id": 10,
        "question": "Which natural preparation uses cow urine, neem leaves, hot green chillies, and garlic to combat severe stem borers?",
        "options": ["Agniastra", "Panchagavya", "Urea", "NPK Spray"],
        "correctIndex": 0,
        "explanation": "Agniastra is a potent botanical formulation specifically fermented to manage aggressive crop borers."
    },
    {
        "id": 11,
        "question": "What simple action cut household washing machine energy consumption by nearly 90%?",
        "options": ["Washing in cold water instead of hot water", "Using extra detergent", "Running empty loads", "Washing at night"],
        "correctIndex": 0,
        "explanation": "Roughly 90% of energy used by washing machines goes into heating the water."
    },
    {
        "id": 12,
        "question": "How long do typical single-use plastic bags take to decompose in landfill environments?",
        "options": ["10 to 20 years", "500 to 1,000 years", "2 to 5 years", "They decompose in 6 months"],
        "correctIndex": 1,
        "explanation": "Synthetic plastics resist biological degradation, persisting in ecosystems for 500 to 1,000 years."
    },
    {
        "id": 13,
        "question": "What is companion planting in organic farming?",
        "options": [
            "Planting mutually beneficial crops together to deter pests and enhance nutrients",
            "Planting crops in isolated single-species monocultures",
            "Growing crops without sunlight",
            "Using artificial LED lights"
        ],
        "correctIndex": 0,
        "explanation": "Companion planting couples crops like basil with tomatoes or legumes with corn for natural pest defense and soil fertility."
    },
    {
        "id": 14,
        "question": "Which sour fermented household liquid can be sprayed on plants as a natural fungicide against powdery mildew?",
        "options": ["Sour Buttermilk (fermented 4 days)", "Concentrated Vinegar", "Salt Solution", "Kerosene"],
        "correctIndex": 0,
        "explanation": "Lactic acid bacteria in sour buttermilk outcompete fungal pathogens causing leaf mildew and spot diseases."
    },
    {
        "id": 15,
        "question": "Which gas has a global warming potential over 28 times higher than CO2 over a 100-year timeframe?",
        "options": ["Methane (CH4)", "Oxygen (O2)", "Nitrogen (N2)", "Argon (Ar)"],
        "correctIndex": 0,
        "explanation": "Methane traps significantly more infrared heat in the atmosphere than CO2 per molecule."
    },
    {
        "id": 16,
        "question": "What is Panchagavya in traditional organic agriculture?",
        "options": [
            "A growth promoter made from 5 cow products (dung, urine, milk, curd, ghee) plus coconut water & jaggery",
            "A synthetic weedkiller",
            "A plastic seedling tray",
            "A chemical nitrogen granule"
        ],
        "correctIndex": 0,
        "explanation": "Panchagavya boosts crop immunity, branching, leaf area, and flowering yield naturally."
    },
    {
        "id": 17,
        "question": "What benefit does intercropping legumes (like pulse crops or clover) offer in natural farming?",
        "options": [
            "Legumes naturally fix atmospheric nitrogen into the soil via Rhizobium root nodules",
            "Legumes increase soil acidity",
            "Legumes repel all earthworms",
            "Legumes stop water infiltration"
        ],
        "correctIndex": 0,
        "explanation": "Legumes harbor nitrogen-fixing bacteria in root nodules, replacing synthetic nitrogen fertilizers."
    },
    {
        "id": 18,
        "question": "What is phantom or standby energy consumption?",
        "options": [
            "Electricity drawn by plugged-in electronics even when switched off",
            "Energy generated by wind turbines",
            "Heat produced by solar panels",
            "Power generated by hydro dams"
        ],
        "correctIndex": 0,
        "explanation": "Unplugging idle chargers and appliances saves up to 10% on household electric bills."
    },
    {
        "id": 19,
        "question": "Which simple garden addition naturally controls flying thrips and whiteflies without chemicals?",
        "options": ["Yellow and Blue Sticky Traps", "Copper Sulphate", "Synthetic Insecticide", "Chlorinated Water"],
        "correctIndex": 0,
        "explanation": "Colored sticky traps attract flying insects visually, capturing them before they lay eggs on crops."
    },
    {
        "id": 20,
        "question": "What is the primary ecological hazard of single-use plastic breaking down in marine environments?",
        "options": [
            "Formation of microplastics absorbed by marine life and human seafood",
            "It turns seawater into freshwater",
            "It increases ocean oxygen levels",
            "It cools marine temperatures"
        ],
        "correctIndex": 0,
        "explanation": "Microplastics absorb toxic chemical compounds and enter marine food chains worldwide."
    }
]

@quiz_bp.route('/api/quiz/questions', methods=['GET'])
def get_quiz_questions():
    # Return a randomized sample of 5 questions each time requested
    sample_size = min(len(QUIZ_QUESTIONS_BANK), 5)
    selected_questions = random.sample(QUIZ_QUESTIONS_BANK, sample_size)
    return jsonify({
        "status": "success",
        "questions": selected_questions
    })

@quiz_bp.route('/api/quiz/submit', methods=['POST'])
def submit_quiz():
    data = request.get_json() or {}
    user_answers = data.get('answers', {})
    user_name = data.get('userName', 'Eco Enthusiast')

    q_lookup = {str(q['id']): q for q in QUIZ_QUESTIONS_BANK}
    
    score = 0
    total = len(user_answers) if user_answers else 5
    results_detail = []

    for qid_str, selected in user_answers.items():
        q_item = q_lookup.get(str(qid_str))
        if not q_item:
            continue
        
        is_correct = (selected == q_item['correctIndex'])
        if is_correct:
            score += 1
        
        results_detail.append({
            "questionId": q_item['id'],
            "correct": is_correct,
            "correctIndex": q_item['correctIndex'],
            "userSelectedIndex": selected,
            "explanation": q_item['explanation']
        })

    pct = round((score / max(total, 1)) * 100)

    # Badge tiers
    if pct >= 90:
        badge = "Earth Protector"
    elif pct >= 70:
        badge = "Green Warrior"
    elif pct >= 40:
        badge = "Eco Learner"
    else:
        badge = "Eco Beginner"

    record = {
        "user_name": user_name,
        "score": score,
        "total": total,
        "percentage": pct,
        "badge": badge,
        "details": results_detail
    }
    db_manager.insert_record("quiz_results", dict(record))

    return jsonify({
        "status": "success",
        "score": score,
        "total": total,
        "percentage": pct,
        "badge": badge,
        "record": record
    })
