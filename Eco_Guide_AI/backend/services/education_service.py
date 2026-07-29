"""
WildGuard AI – Education Service
Generates quizzes, facts, species of the day, and conservation content.
"""
import random
import time
from typing import List, Dict
from core.gemini_client import gemini


# ─── Static Wildlife Facts ────────────────────────────────────────────────────
WILDLIFE_FACTS = [
    {"fact": "The Blue Whale's heart is so large that a human could crawl through its aorta. It beats only 2-10 times per minute when diving.", "category": "Marine Life", "species": "Blue Whale"},
    {"fact": "A group of flamingos is called a flamboyance. Their pink color comes entirely from the carotenoid pigments in their food.", "category": "Birds", "species": "Flamingo"},
    {"fact": "Elephants are the only animals that cannot jump, but they can run at 25 mph and their trunks contain over 40,000 muscles.", "category": "Mammals", "species": "Elephant"},
    {"fact": "The mantis shrimp has 16 types of colour receptors (humans have 3) and can punch with the force of a bullet at 23 m/s.", "category": "Marine Life", "species": "Mantis Shrimp"},
    {"fact": "A cheetah's spots are actually solid black, unlike a leopard's rosettes. No two cheetahs have the same spot pattern.", "category": "Big Cats", "species": "Cheetah"},
    {"fact": "Crows can recognise individual human faces and hold grudges for years, passing warnings about 'dangerous' people to their offspring.", "category": "Birds", "species": "Crow"},
    {"fact": "The immortal jellyfish (Turritopsis dohrnii) is biologically immortal – it can revert to its juvenile state after reaching maturity.", "category": "Marine Life", "species": "Immortal Jellyfish"},
    {"fact": "Monarch butterflies navigate using a time-compensated sun compass and Earth's magnetic field, migrating up to 4,800 km.", "category": "Insects", "species": "Monarch Butterfly"},
    {"fact": "A single Bengal Tiger's territory can span up to 1,000 km². Their roar can be heard up to 3 km away.", "category": "Big Cats", "species": "Bengal Tiger"},
    {"fact": "The pistol shrimp can generate a bubble cavitation with temperatures of 8,000°C – nearly as hot as the sun's surface.", "category": "Marine Life", "species": "Pistol Shrimp"},
    {"fact": "Wolves change entire river ecosystems through a 'trophic cascade' – their presence alters deer behavior, allowing vegetation to recover, stabilising riverbanks.", "category": "Mammals", "species": "Gray Wolf"},
    {"fact": "The Greenland Shark lives up to 400 years, is sexually mature at 150 years, and was alive when Shakespeare was writing his plays.", "category": "Marine Life", "species": "Greenland Shark"},
    {"fact": "Tardigrades (water bears) can survive in the vacuum of space, temperatures from -272°C to +150°C, and 1,000 times more radiation than any other animal.", "category": "Invertebrates", "species": "Tardigrade"},
    {"fact": "The Mimic Octopus can impersonate 15+ different species including lionfish, flatfish, and sea snakes, changing behavior and shape.", "category": "Marine Life", "species": "Mimic Octopus"},
    {"fact": "African elephants can detect water up to 12 miles away. They dig 'wells' in dry riverbeds that other animals also use for water.", "category": "Mammals", "species": "African Elephant"},
    {"fact": "The lyrebird of Australia can perfectly mimic chainsaws, camera shutters, car alarms, and other birds with exceptional accuracy.", "category": "Birds", "species": "Lyrebird"},
    {"fact": "Mountain gorillas share 98.3% of their DNA with humans. A dominant silverback can weigh 220 kg but is primarily vegetarian.", "category": "Primates", "species": "Mountain Gorilla"},
    {"fact": "The platypus is one of the only venomous mammals. Males have a spur on their hind leg delivering venom potent enough to incapacitate a human.", "category": "Mammals", "species": "Platypus"},
    {"fact": "Humpback whale songs evolve culturally – new 'hit songs' spread across ocean basins as other males learn and replicate innovative vocalisations.", "category": "Marine Life", "species": "Humpback Whale"},
    {"fact": "The baobab tree can store up to 120,000 litres of water in its trunk. Some living baobabs are over 3,000 years old.", "category": "Plants", "species": "Baobab"},
    {"fact": "Polar bear fur is actually transparent and hollow, not white. It appears white because of light scattering, similar to snow.", "category": "Mammals", "species": "Polar Bear"},
    {"fact": "The bombardier beetle sprays boiling hot chemical spray (up to 100°C) at predators from a precisely aimed nozzle at 500 pulses per second.", "category": "Insects", "species": "Bombardier Beetle"},
    {"fact": "Dolphins sleep with one eye open, one brain hemisphere at a time (unihemispheric sleep), allowing them to surface for air while resting.", "category": "Marine Life", "species": "Dolphin"},
    {"fact": "The Indian Peafowl's iridescent tail doesn't use pigment – the colors are created by nanostructures that diffract light, like a natural photonic crystal.", "category": "Birds", "species": "Indian Peafowl"},
    {"fact": "Vampire bats are the only mammals that exclusively feed on blood. They can detect the heat signature of blood vessels through special nose receptors.", "category": "Mammals", "species": "Vampire Bat"},
    {"fact": "The Bowhead Whale lives over 200 years – the oldest ever found had a 19th-century harpoon tip still embedded in its blubber.", "category": "Marine Life", "species": "Bowhead Whale"},
    {"fact": "Ants have been farming fungi for over 50 million years – long before humans invented agriculture. Leafcutter ants are among the world's most sophisticated farmers.", "category": "Insects", "species": "Leafcutter Ant"},
    {"fact": "The Venus Flytrap can count – it requires two touches within 20 seconds to trigger its trap, preventing false alarms from raindrops.", "category": "Plants", "species": "Venus Flytrap"},
    {"fact": "Ocelots are crepuscular hunters who can rotate their head almost 180° and whose paw prints are so similar to jaguars that scientists use DNA to distinguish them.", "category": "Big Cats", "species": "Ocelot"},
    {"fact": "The pangolin is the world's most trafficked mammal. Their scales (made of keratin, like fingernails) are falsely believed to have medicinal properties.", "category": "Mammals", "species": "Pangolin"},
]

# ─── Quiz Questions ───────────────────────────────────────────────────────────
QUIZ_QUESTIONS = {
    "beginner": [
        {"q": "What is the national animal of India?", "options": ["Lion", "Bengal Tiger", "Elephant", "Peacock"], "answer": "Bengal Tiger", "explanation": "The Bengal Tiger (Panthera tigris tigris) has been India's national animal since 1973 when Project Tiger was launched."},
        {"q": "Which is the largest land animal on Earth?", "options": ["Asian Elephant", "Giraffe", "African Bush Elephant", "Hippopotamus"], "answer": "African Bush Elephant", "explanation": "The African Bush Elephant (Loxodonta africana) is the largest land animal, weighing up to 6,350 kg."},
        {"q": "What does 'IUCN' stand for?", "options": ["International Union for Conservation of Nature", "Indian Union for Conservation Network", "International Union for Conservation Networks", "International United Conservation Nations"], "answer": "International Union for Conservation of Nature", "explanation": "The IUCN was founded in 1948 and maintains the Red List of Threatened Species."},
        {"q": "Which bird is the national bird of India?", "options": ["Great Indian Bustard", "Indian Peafowl", "Sarus Crane", "Black Necked Stork"], "answer": "Indian Peafowl", "explanation": "The Indian Peafowl (Pavo cristatus) was declared India's national bird in 1963."},
        {"q": "What is the primary diet of the Giant Panda?", "options": ["Fruits", "Fish", "Bamboo", "Insects"], "answer": "Bamboo", "explanation": "Giant Pandas eat 12–38 kg of bamboo daily, making up 99% of their diet despite being members of the order Carnivora."},
        {"q": "Which animal is known as the 'fastest land animal'?", "options": ["Leopard", "Lion", "Cheetah", "African Wild Dog"], "answer": "Cheetah", "explanation": "The Cheetah (Acinonyx jubatus) reaches speeds of up to 112 km/h, making it the fastest land animal."},
        {"q": "What is the botanical name of the Neem tree?", "options": ["Ficus benghalensis", "Azadirachta indica", "Saraca asoca", "Santalum album"], "answer": "Azadirachta indica", "explanation": "Neem (Azadirachta indica) belongs to the family Meliaceae and is native to the Indian subcontinent."},
        {"q": "Which conservation category in the IUCN Red List indicates the highest risk of extinction?", "options": ["Endangered", "Vulnerable", "Critically Endangered", "Near Threatened"], "answer": "Critically Endangered", "explanation": "Critically Endangered (CR) is the highest risk category before Extinct in the Wild (EW) and Extinct (EX)."},
    ],
    "intermediate": [
        {"q": "Which Indian rhinoceros species is found in Kaziranga National Park?", "options": ["Black Rhinoceros", "White Rhinoceros", "Indian One-Horned Rhinoceros", "Javan Rhinoceros"], "answer": "Indian One-Horned Rhinoceros", "explanation": "The Indian One-Horned Rhinoceros (Rhinoceros unicornis) – Kaziranga is home to ~2400 individuals, about 70% of the world population."},
        {"q": "What is the primary cause of decline for the Monarch Butterfly?", "options": ["Predation by birds", "Milkweed habitat loss due to herbicide use", "Ocean pollution", "Disease outbreaks"], "answer": "Milkweed habitat loss due to herbicide use", "explanation": "Monarchs exclusively lay eggs on milkweed plants. Widespread herbicide use in agriculture has dramatically reduced milkweed, destroying breeding habitat."},
        {"q": "What ecological role makes the African Elephant an 'ecosystem engineer'?", "options": ["They build dams like beavers", "They dig waterholes used by other species and disperse seeds over vast distances", "They fertilize soil with urine", "They remove dead trees"], "answer": "They dig waterholes used by other species and disperse seeds over vast distances", "explanation": "Elephants create waterholes by digging in dry riverbeds and disperse large seeds across kilometres, making them critical architects of their ecosystem."},
        {"q": "The Snow Leopard is found at what typical elevation range?", "options": ["0-500 m", "500-1500 m", "3000-5500 m", "6000-8000 m"], "answer": "3000-5500 m", "explanation": "Snow Leopards inhabit alpine and subalpine zones between 3,000 and 5,500 m elevation across Central Asia and the Himalayas."},
        {"q": "What is the scientific name of the Mountain Gorilla?", "options": ["Gorilla gorilla gorilla", "Pan troglodytes", "Gorilla beringei beringei", "Pongo pygmaeus"], "answer": "Gorilla beringei beringei", "explanation": "The Mountain Gorilla is a subspecies of Eastern Gorilla. Fewer than 1,100 individuals remain in the Virunga volcanoes and Bwindi forest."},
        {"q": "The Gangetic River Dolphin is the national aquatic animal of which country?", "options": ["Bangladesh", "Nepal", "India", "Pakistan"], "answer": "India", "explanation": "The Ganges River Dolphin (Platanista gangetica) was declared India's National Aquatic Animal in 2009 and is the subject of Project Dolphin."},
        {"q": "What makes the Leatherback Sea Turtle unique among sea turtles?", "options": ["It breathes air", "It has a soft, leathery carapace instead of a hard shell", "It is the smallest sea turtle", "It only lives in freshwater"], "answer": "It has a soft, leathery carapace instead of a hard shell", "explanation": "The Leatherback (Dermochelys coriacea) is the only sea turtle without a hard shell. It is the largest, reaching 2 m and 900 kg."},
        {"q": "Which biodiversity hotspot includes the Western Ghats of India?", "options": ["Himalayan Mountains", "Indo-Burma", "Western Ghats and Sri Lanka", "Sundaland"], "answer": "Western Ghats and Sri Lanka", "explanation": "The Western Ghats and Sri Lanka are designated as one of 36 global biodiversity hotspots, with extremely high endemism in flora and fauna."},
    ],
    "expert": [
        {"q": "What is the trophic cascade phenomenon demonstrated by wolves reintroduced to Yellowstone in 1995?", "options": ["Wolves directly killed all predators", "Wolf predation changed elk behavior causing vegetation recovery, river stabilization, and species proliferation", "Wolves dammed rivers", "Wolves eliminated all diseases"], "answer": "Wolf predation changed elk behavior causing vegetation recovery, river stabilization, and species proliferation", "explanation": "This 'landscape of fear' effect caused elk to avoid valleys, allowing willows and aspens to recover, which stabilized riverbanks, changed river morphology, and increased biodiversity throughout the ecosystem."},
        {"q": "What is the ecological mechanism behind the 'Corpse Flower' (Rafflesia arnoldii)'s pollination strategy?", "options": ["Attracting hummingbirds with nectar", "Wind pollination via pollen release", "Mimicking carrion odour to attract blowflies as pollinators", "Self-pollination"], "answer": "Mimicking carrion odour to attract blowflies as pollinators", "explanation": "Rafflesia produces thermogenic heat and volatile compounds (dimethyl disulfide, dimethyl trisulfide) mimicking decomposing flesh, attracting carrion flies (Lucilia, Calliphora sp.) as pollinators."},
        {"q": "What is the EDGE of Existence metric (Evolutionary Distinctiveness + Global Endangerment) primarily used for?", "options": ["Measuring habitat size", "Prioritising conservation based on species evolutionary uniqueness combined with extinction risk", "Calculating population growth rate", "Determining prey availability"], "answer": "Prioritising conservation based on species evolutionary uniqueness combined with extinction risk", "explanation": "EDGE species have few close relatives on the tree of life and are at high extinction risk. Protecting them preserves unique evolutionary heritage that cannot be replaced if lost."},
        {"q": "The Nilgiri Tahr (Nilgiritragus hylocrius) is endemic to which specific ecosystem type in India?", "options": ["Mangrove forests of Kerala", "Shola-grassland mosaic of the Western Ghats", "Sundarbans tidal forests", "Himalayan alpine meadows"], "answer": "Shola-grassland mosaic of the Western Ghats", "explanation": "The Nilgiri Tahr is found exclusively in the high-altitude shola-grassland mosaic ecosystem of the Nilgiris, Anamalais and associated ranges. It is the state animal of Tamil Nadu."},
        {"q": "What is metapopulation theory and why is it critical for conservation biology?", "options": ["Theory about single large populations", "Framework describing interconnected subpopulations separated by unsuitable habitat, where recolonization balances local extinctions", "Theory about migratory routes", "Framework for calculating carrying capacity"], "answer": "Framework describing interconnected subpopulations separated by unsuitable habitat, where recolonization balances local extinctions", "explanation": "Metapopulation theory (Levins 1969) is vital for designing wildlife corridors, as even small subpopulations remain viable if connected. Isolation leads to inbreeding depression and local extinction."},
        {"q": "Which keystone concept explains why sea otters are critical to kelp forest biodiversity?", "options": ["Sea otters build kelp structures", "Sea otters control sea urchin populations which would otherwise overgraze kelp, creating urchin barrens", "Sea otters provide nitrogen fertilizer", "Sea otters shade competing algae"], "answer": "Sea otters control sea urchin populations which would otherwise overgraze kelp, creating urchin barrens", "explanation": "This classic Paine (1966) keystone species example shows how sea otters controlling sea urchins prevents overgrazing of kelp, maintaining structural habitat for hundreds of species."},
        {"q": "The Great Indian Bustard's primary survival threat today (2024) relates to which infrastructure?", "options": ["Road networks", "High-voltage overhead power lines causing collision mortality", "Wind turbines", "Railway lines"], "answer": "High-voltage overhead power lines causing collision mortality", "explanation": "The Supreme Court of India ordered power lines undergrounded in GIB habitats (2021). Power line collision is now the leading direct mortality cause, especially in Rajasthan's wind energy belt where overhead lines bisect GIB habitat."},
    ],
}


def get_daily_fact() -> Dict:
    """Return a wildlife fact based on the current day."""
    day_index = int(time.time() / 86400) % len(WILDLIFE_FACTS)
    return WILDLIFE_FACTS[day_index]


def get_random_fact() -> Dict:
    """Return a random wildlife fact."""
    return random.choice(WILDLIFE_FACTS)


def get_quiz(difficulty: str = "beginner", count: int = 5) -> List[Dict]:
    """Return a quiz set for the given difficulty."""
    difficulty = difficulty.lower()
    if difficulty not in QUIZ_QUESTIONS:
        difficulty = "beginner"
    questions = QUIZ_QUESTIONS[difficulty].copy()
    random.shuffle(questions)
    return questions[:min(count, len(questions))]


def get_species_of_the_day() -> str:
    """Generate an educational species of the day profile."""
    species_pool = [
        "Snow Leopard (Panthera uncia)",
        "Pangolin (Manis crassicaudata)",
        "Axolotl (Ambystoma mexicanum)",
        "Narwhal (Monodon monoceros)",
        "Aye-aye (Daubentonia madagascariensis)",
        "Okapi (Okapia johnstoni)",
        "Saiga Antelope (Saiga tatarica)",
        "Irrawaddy Dolphin (Orcaella brevirostris)",
        "Philippine Eagle (Pithecophaga jefferyi)",
        "Numbat (Myrmecobius fasciatus)",
        "Proboscis Monkey (Nasalis larvatus)",
        "Fishing Cat (Prionailurus viverrinus)",
        "Nilgiri Tahr (Nilgiritragus hylocrius)",
        "Great Indian Bustard (Ardeotis nigriceps)",
        "Gangetic Dolphin (Platanista gangetica)",
    ]
    day_index = int(time.time() / 86400) % len(species_pool)
    species = species_pool[day_index]

    prompt = f"""
Generate an engaging, educational "Species of the Day" profile for: **{species}**

Format it with:
1. 🌟 A captivating opening hook (2 sentences)
2. 📋 Full taxonomy table (Kingdom to Species)
3. 🔴 Conservation status with IUCN category
4. 🌍 Where it lives (with specific locations)
5. 🍽️ What it eats and how it hunts/feeds
6. 🧬 3 mind-blowing scientific facts about this species
7. ⚠️ Top 3 threats to its survival
8. 🌱 What YOU can do to help conserve this species
9. 📚 Sources

Make it engaging for all ages – educational yet fascinating.
"""
    return gemini.generate_structured(prompt)


def generate_quiz_with_ai(topic: str, difficulty: str = "intermediate") -> str:
    """Generate a custom AI-powered quiz on a wildlife topic."""
    prompt = f"""
Create a wildlife quiz with 5 multiple-choice questions on the topic: **{topic}**
Difficulty level: **{difficulty}**

For each question provide:
- Question text
- 4 options (A, B, C, D)
- Correct answer
- Scientific explanation (2-3 sentences)

Format each question clearly numbered. Make questions scientifically accurate and cite sources.
"""
    return gemini.generate_structured(prompt)


def generate_conservation_report(topic: str) -> str:
    """Generate a conservation awareness report."""
    prompt = f"""
Write a comprehensive conservation awareness report on: **{topic}**

Include:
1. Current situation and statistics
2. Species/ecosystems affected
3. Root causes
4. Global conservation efforts
5. Success stories
6. What individuals can do
7. Organizations working on this issue
8. Scientific sources

Make it compelling, factual, and actionable. Target a general educated audience.
"""
    return gemini.generate_structured(prompt)
