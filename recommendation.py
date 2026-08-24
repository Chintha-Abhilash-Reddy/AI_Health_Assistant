"""
recommendation.py — Disease precautions, lifestyle, food, exercise, and tablet/medication recommendations
"""

# ── Master disease data dictionary with Tablets/Medications ──────────────
DISEASE_DATA = {
    "Common Cold": {
        "precautions": [
            "Rest as much as possible and avoid overexertion",
            "Drink warm fluids like herbal tea, warm water, and broths",
            "Stay well hydrated — aim for 8-10 glasses of water per day",
            "Maintain proper hand hygiene to prevent spreading the virus",
            "Use a humidifier or steam inhalation to ease congestion",
            "Avoid close contact with others to prevent transmission",
            "Gargle with warm salt water to soothe sore throat",
        ],
        "lifestyle": [
            "Get 8–9 hours of quality sleep to support recovery",
            "Eat nutritious, warm meals rich in vitamins C and zinc",
            "Avoid smoking and alcohol as they weaken the immune system",
            "Stay in a warm, comfortable room",
            "Take warm showers to ease nasal congestion",
            "Use saline nasal spray for relief",
        ],
        "foods_recommended": [
            "Warm chicken soup or vegetable broth",
            "Ginger and turmeric tea",
            "Honey and lemon in warm water",
            "Citrus fruits (oranges, kiwi) rich in Vitamin C",
            "Garlic and onions — natural antiviral properties",
            "Yoghurt with probiotics",
        ],
        "foods_to_avoid": [
            "Cold or iced beverages and ice cream",
            "Excess dairy products (can thicken mucus)",
            "Fried and oily foods",
            "Alcohol and caffeinated drinks",
            "Spicy foods that irritate the throat",
        ],
        "exercise": "Avoid intense workouts. Gentle stretching or light walking indoors is acceptable if fever-free.",
        "tablets": [
            {"name": "Paracetamol (500mg)", "type": "Antipyretic / Analgesic", "dosage": "1 tablet every 6-8 hours as needed for fever/headache (Max 4 tablets/day)", "note": "Take after food"},
            {"name": "Cetirizine (10mg)", "type": "Antihistamine", "dosage": "1 tablet once daily at bedtime", "note": "Helps relieve runny nose, sneezing & watery eyes; may cause drowsiness"},
            {"name": "Vitamin C + Zinc (500mg)", "type": "Immune Supplement", "dosage": "1 chewable tablet daily for 5 days", "note": "Boosts immune response"},
            {"name": "Saline Nasal Spray (0.9%)", "type": "Decongestant Spray", "dosage": "2 sprays in each nostril 2-3 times daily", "note": "Relieves nasal blockage safely"}
        ]
    },

    "Influenza": {
        "precautions": [
            "Take complete bed rest — your body needs energy to fight the virus",
            "Drink plenty of fluids to prevent dehydration",
            "Monitor body temperature regularly with a thermometer",
            "Avoid close contact with family members to prevent spreading",
            "Cover mouth and nose when coughing or sneezing",
            "Consult a physician if fever exceeds 102°F or lasts >3 days",
        ],
        "lifestyle": [
            "Stay isolated in a well-ventilated room",
            "Sleep at least 9–10 hours during acute phase",
            "Avoid physical exertion until 48 hours fever-free",
            "Use warm compresses for body aches",
        ],
        "foods_recommended": [
            "Warm soups, bone broths, and herbal teas",
            "Bananas, applesauce, and easily digestible carbs",
            "Electrolyte drinks / coconut water",
            "Vitamin C rich fruits and berries",
        ],
        "foods_to_avoid": [
            "Sugary energy drinks and sodas",
            "Alcohol and excess coffee",
            "Heavy, greasy, and processed foods",
            "Unpasteurized dairy products",
        ],
        "exercise": "Strict rest during fever. No cardiovascular or strength training until full recovery.",
        "tablets": [
            {"name": "Paracetamol (650mg)", "type": "Antipyretic / Analgesic", "dosage": "1 tablet every 6-8 hours if temperature > 100°F", "note": "Do not exceed 3000mg/day"},
            {"name": "Oseltamivir (75mg) (Tamiflu)", "type": "Antiviral (Prescription Only)", "dosage": "1 capsule twice daily for 5 days", "note": "Must be prescribed by a doctor within 48h of onset"},
            {"name": "Phenylephrine / Chlorpheniramine", "type": "Decongestant / Antihistamine", "dosage": "1 tablet every 8 hours as needed", "note": "For severe congestion and cough"},
            {"name": "Oral Electrolyte Powder (ORS)", "type": "Hydration Salts", "dosage": "1 sachet dissolved in 1L water throughout the day", "note": "Maintains electrolyte balance"}
        ]
    },

    "Hypertension": {
        "precautions": [
            "Monitor blood pressure daily at the same time and record readings",
            "Strictly limit dietary sodium / salt intake to < 1,500mg daily",
            "Never stop prescribed antihypertensive medications without doctor advice",
            "Avoid excessive stress, anger, and anxiety triggers",
            "Avoid caffeine, energy drinks, and tobacco completely",
        ],
        "lifestyle": [
            "Follow the DASH (Dietary Approaches to Stop Hypertension) diet",
            "Engage in 30 minutes of moderate aerobic exercise 5 days a week",
            "Practice relaxation techniques (deep breathing, meditation)",
            "Maintain a healthy body weight and target BMI < 25",
            "Get 7–8 hours of sound sleep every night",
        ],
        "foods_recommended": [
            "Leafy greens (spinach, kale) rich in potassium",
            "Berries (blueberries, strawberries) rich in antioxidants",
            "Beets, oats, and whole grains",
            "Garlic, bananas, and unsalted nuts",
            "Fatty fish rich in Omega-3 fatty acids",
        ],
        "foods_to_avoid": [
            "Table salt, pickles, and processed meats (bacon, sausages)",
            "Canned soups and instant noodles (high sodium)",
            "Full-fat dairy, butter, and trans fats",
            "Alcohol and sugary beverages",
        ],
        "exercise": "Brisk walking, swimming, light cycling, and yoga. Avoid heavy weightlifting without physician approval.",
        "tablets": [
            {"name": "Amlodipine (5mg)", "type": "Calcium Channel Blocker (Prescription)", "dosage": "1 tablet once daily in the morning", "note": "Doctor consultation mandatory; relaxes blood vessels"},
            {"name": "Telmisartan (40mg)", "type": "ARB Antihypertensive (Prescription)", "dosage": "1 tablet once daily", "note": "Lowers arterial blood pressure; monitor kidney function"},
            {"name": "Hydrochlorothiazide (12.5mg)", "type": "Diuretic (Prescription)", "dosage": "1 tablet morning with food", "note": "Helps kidneys remove excess fluid and sodium"}
        ]
    },

    "Diabetes": {
        "precautions": [
            "Check fasting and post-prandial blood glucose levels regularly",
            "Inspect feet daily for cuts, blisters, or numbness",
            "Take prescribed insulin or oral antidiabetic agents on time",
            "Always carry fast-acting glucose tablets or candy for hypoglycemia",
            "Maintain annual eye, kidney, and cardiovascular checkups",
        ],
        "lifestyle": [
            "Eat smaller, balanced meals at consistent times every day",
            "Stay physically active with daily moderate exercise",
            "Stay hydrated with pure water (avoid fruit juices and sodas)",
            "Manage stress levels to avoid cortisol-induced sugar spikes",
        ],
        "foods_recommended": [
            "Non-starchy vegetables (broccoli, spinach, cauliflower)",
            "High-fiber foods (beans, lentils, chia seeds, oats)",
            "Nuts, avocados, and healthy unsaturated fats",
            "Bitter gourd (karela), fenugreek seeds, and cinnamon",
            "Lean proteins (tofu, eggs, skinless chicken)",
        ],
        "foods_to_avoid": [
            "Refined sugar, sweets, cakes, and pastries",
            "White bread, white rice, and refined flour",
            "Sweetened beverages, sodas, and packed fruit juices",
            "Deep-fried snacks and trans fat products",
        ],
        "exercise": "30-45 minutes of brisk walking, swimming, or cycling 5 days a week. Pair with light resistance exercises.",
        "tablets": [
            {"name": "Metformin (500mg / 1000mg)", "type": "Biguanide (Prescription)", "dosage": "1 tablet with or after meals (as prescribed)", "note": "First-line medication for Type 2 Diabetes; improves insulin sensitivity"},
            {"name": "Glimepiride (1mg / 2mg)", "type": "Sulfonylurea (Prescription)", "dosage": "1 tablet before breakfast (as prescribed)", "note": "Stimulates insulin production; watch for low blood sugar"},
            {"name": "Empagliflozin (10mg)", "type": "SGLT2 Inhibitor (Prescription)", "dosage": "1 tablet once daily morning", "note": "Excretes excess sugar in urine; protects heart & kidneys"}
        ]
    },

    "Malaria": {
        "precautions": [
            "Malaria is a critical infection — seek immediate medical diagnosis via blood smear",
            "Use mosquito nets and repellents containing DEET",
            "Eliminate standing water around the home to prevent breeding",
            "Complete the entire course of prescribed antimalarial medications",
            "Monitor for high fever spikes and chills",
        ],
        "lifestyle": [
            "Strict bed rest during febrile episodes",
            "Drink plenty of fluids and electrolyte solutions",
            "Wear long-sleeved light-colored clothing outdoors",
        ],
        "foods_recommended": [
            "High-carbohydrate light meals (rice gruel, porridge)",
            "Fresh fruit juices (papaya, pomegranate, orange)",
            "Coconut water and herbal broths",
            "Boiled vegetables and protein-rich pulses",
        ],
        "foods_to_avoid": [
            "Oily, spicy, and heavily seasoned foods",
            "Caffeinated beverages and alcohol",
            "Raw or unwashed vegetables",
        ],
        "exercise": "No physical exercise during acute illness. Rest until parasitic clearance is confirmed.",
        "tablets": [
            {"name": "Artemether + Lumefantrine (Coartem)", "type": "ACT Antimalarial (Prescription)", "dosage": "Exact 3-day course as prescribed by doctor", "note": "Take with milk or fatty meal for optimal absorption"},
            {"name": "Paracetamol (650mg)", "type": "Antipyretic", "dosage": "1 tablet every 6 hours for high fever & body aches", "note": "Do not exceed maximum daily limit"},
            {"name": "Oral Rehydration Salts (ORS)", "type": "Electrolytes", "dosage": "Drink 1-2 liters daily", "note": "Prevents dehydration from sweating and chills"}
        ]
    },

    "Typhoid": {
        "precautions": [
            "Consult a physician immediately; antibiotics are mandatory for Salmonella typhi",
            "Drink only boiled, filtered, or sealed bottled water",
            "Wash hands thoroughly with soap before eating and after using the restroom",
            "Do not consume street food, raw salads, or cut fruits from vendors",
            "Complete full antibiotic cycle to prevent relapse or becoming a carrier",
        ],
        "lifestyle": [
            "Complete bed rest for at least 1-2 weeks",
            "Maintain strict personal hygiene and sanitize living areas",
            "Record daily temperature readings",
        ],
        "foods_recommended": [
            "Boiled rice, khichdi, soft custards, and porridge",
            "Boiled potatoes, carrots, and bottle gourd",
            "Coconut water, barley water, and clear vegetable broths",
            "Ripe bananas and stewed apples",
        ],
        "foods_to_avoid": [
            "High-fiber raw foods, unpeeled fruits, and raw vegetables",
            "Spicy, fried, and heavily seasoned dishes",
            "Dairy products if experiencing diarrhea",
            "Carbonated sodas and caffeine",
        ],
        "exercise": "Strict physical rest. No workouts until completely recovered and verified by blood tests.",
        "tablets": [
            {"name": "Azithromycin (500mg) / Cefixime (200mg)", "type": "Antibiotic (Prescription Only)", "dosage": "As prescribed by doctor for 7-14 days", "note": "Crucial: Complete entire course even if feeling better"},
            {"name": "Paracetamol (650mg)", "type": "Antipyretic", "dosage": "1 tablet for high 'step-ladder' fever spikes", "note": "Take with water after light food"},
            {"name": "Pantoprazole (40mg)", "type": "Proton Pump Inhibitor", "dosage": "1 tablet 30 minutes before breakfast", "note": "Protects stomach lining during antibiotic therapy"},
            {"name": "Probiotic Capsules (e.g. Sporlac / Darolac)", "type": "Gut Flora Restorer", "dosage": "1 capsule twice daily", "note": "Restores healthy gut bacteria"}
        ]
    },

    "Pneumonia": {
        "precautions": [
            "Pneumonia is serious — immediate medical consultation and chest X-ray are vital",
            "Take all prescribed antibiotics or antivirals exactly as instructed",
            "Monitor blood oxygen saturation (SpO2) with a pulse oximeter (seek ER if SpO2 < 92%)",
            "Avoid exposure to tobacco smoke, dust, and cold air",
            "Use deep breathing exercises to keep airways open",
        ],
        "lifestyle": [
            "Strict bed rest in an elevated (propped up) position to ease breathing",
            "Use a room humidifier or steam vaporizer",
            "Stay well hydrated to help thin mucus in lungs",
        ],
        "foods_recommended": [
            "Warm herbal broths, ginger tea, and honey water",
            "Protein-rich foods (eggs, soft fish, lentils) to aid tissue healing",
            "Citrus fruits and green leafy vegetables",
            "Turmeric milk (golden milk) for anti-inflammatory benefits",
        ],
        "foods_to_avoid": [
            "Cold drinks and ice-chilled foods",
            "Dairy products if they exacerbate phlegm sensation",
            "Salty and ultra-processed meals",
            "Smoking and alcohol",
        ],
        "exercise": "Strictly no exercise during acute phase. Practice incentive spirometry and gentle deep breathing.",
        "tablets": [
            {"name": "Amoxicillin + Clavulanic Acid (625mg)", "type": "Broad-Spectrum Antibiotic (Prescription)", "dosage": "1 tablet twice daily for 7-10 days", "note": "Take with food; prescription required"},
            {"name": "Levocetirizine + Montelukast", "type": "Bronchodilator / Antiallergic", "dosage": "1 tablet at bedtime", "note": "Reduces airway inflammation and coughing"},
            {"name": "N-Acetylcysteine (600mg) (NAC)", "type": "Mucolytic Agent", "dosage": "1 effervescent tablet dissolved in water once daily", "note": "Thins and loosens chest mucus"}
        ]
    },

    "Dengue": {
        "precautions": [
            "Dengue requires careful monitoring — get daily complete blood count (CBC) to track platelets",
            "NEVER take Aspirin, Ibuprofen, or NSAIDs as they increase internal bleeding risks",
            "Use ONLY Paracetamol for fever management",
            "Watch for warning signs: severe abdominal pain, persistent vomiting, bleeding gums, extreme lethargy",
            "Prevent mosquito bites using repellents and mosquito nets",
        ],
        "lifestyle": [
            "Total bed rest until platelet counts stabilize and fever subsides",
            "Drink continuous fluids: aim for 3-4 liters daily",
            "Stay in a cool, mosquito-free environment",
        ],
        "foods_recommended": [
            "Papaya leaf extract / juice (known to support platelet levels)",
            "Pomegranate and kiwi juice (boosts hemoglobin and immunity)",
            "Coconut water and electrolyte solutions (ORS)",
            "Easily digestible light soups and porridge",
        ],
        "foods_to_avoid": [
            "Dark colored foods/drinks that can mask internal gastrointestinal bleeding",
            "Oily, greasy, and spicy foods",
            "Caffeine, sodas, and energy drinks",
        ],
        "exercise": "Absolute rest. Avoid any physical exertion or contact sports that could cause bruising or bleeding.",
        "tablets": [
            {"name": "Paracetamol (500mg / 650mg)", "type": "Antipyretic (ONLY Safe Painkiller)", "dosage": "1 tablet every 6 hours as needed for fever", "note": "⚠️ NEVER take Ibuprofen, Diclofenac, or Aspirin with Dengue"},
            {"name": "Carica Papaya Leaf Extract (1100mg)", "type": "Platelet Support Supplement", "dosage": "1 tablet twice daily after meals", "note": "Clinically proven to help maintain healthy platelet counts"},
            {"name": "Electrolyte Replacement Salts (ORS)", "type": "Oral Rehydration", "dosage": "Consume 2 to 3 liters throughout the day", "note": "Essential to prevent plasma leakage and shock"}
        ]
    },

    "Asthma": {
        "precautions": [
            "Always carry your rescue inhaler (Salbutamol / Albuterol) wherever you go",
            "Identify and strictly avoid triggers (dust, pet dander, cold air, pollen, smoke)",
            "Use a peak flow meter to monitor lung function at home",
            "Rinse mouth with water after using steroid inhalers to prevent oral thrush",
            "Seek emergency medical attention if rescue inhaler does not relieve breathing difficulty within 15 minutes",
        ],
        "lifestyle": [
            "Keep home dust-free with HEPA air purifiers",
            "Cover mouth and nose with a warm scarf in cold weather",
            "Practice diaphragmatic breathing exercises and Pranayama",
            "Avoid active and passive cigarette smoke completely",
        ],
        "foods_recommended": [
            "Foods rich in Vitamin D (fortified milk, eggs, salmon)",
            "Foods rich in Vitamin C and beta-carotene (carrots, bell peppers)",
            "Magnesium-rich foods (spinach, pumpkin seeds, almonds)",
            "Ginger and turmeric with warm water",
        ],
        "foods_to_avoid": [
            "Sulfites found in dried fruits, wine, and pickled foods",
            "Very cold beverages and ice creams",
            "Heavy gas-producing foods that create abdominal pressure on diaphragm",
        ],
        "exercise": "Swimming, walking, and gentle yoga are excellent. Always keep your rescue inhaler nearby during exercise.",
        "tablets": [
            {"name": "Salbutamol / Albuterol Inhaler (100mcg)", "type": "Fast-Acting Rescue Bronchodilator", "dosage": "1-2 puffs as needed for sudden wheezing/breathlessness", "note": "Immediate relief; carry everywhere"},
            {"name": "Budesonide + Formoterol Inhaler (200/6mcg)", "type": "Maintenance Controller Inhaler", "dosage": "1 puff morning and night daily", "note": "Long-term airway inflammation control; rinse mouth after use"},
            {"name": "Montelukast (10mg)", "type": "Leukotriene Receptor Antagonist", "dosage": "1 tablet daily at bedtime", "note": "Prevents exercise-induced and nighttime asthma attacks"}
        ]
    },

    "Migraine": {
        "precautions": [
            "Maintain a headache diary to pinpoint triggers (bright lights, lack of sleep, stress, foods)",
            "Rest in a quiet, dark, and cool room at the onset of symptoms",
            "Apply a cold ice pack to forehead or temples",
            "Stay well-hydrated throughout the day",
            "Avoid skipping meals as hypoglycemia triggers migraine attacks",
        ],
        "lifestyle": [
            "Maintain consistent sleep and wake schedules (even on weekends)",
            "Limit screen time and use blue-light filter glasses",
            "Practice stress-relief techniques (mindfulness, progressive muscle relaxation)",
            "Avoid sudden changes in caffeine intake",
        ],
        "foods_recommended": [
            "Magnesium-rich foods (spinach, pumpkin seeds, almonds, dark chocolate in moderation)",
            "Omega-3 rich foods (chia seeds, flaxseeds, salmon)",
            "Hydrating fruits (watermelon, cucumbers)",
            "Ginger tea (natural anti-inflammatory for nausea and pain)",
        ],
        "foods_to_avoid": [
            "Aged cheeses (contain tyramine)",
            "Processed meats containing nitrates (hot dogs, sausages)",
            "Artificial sweeteners (Aspartame) and MSG",
            "Red wine and excessive caffeine",
        ],
        "exercise": "Regular low-impact exercise (walking, yoga, cycling) prevents attacks. Avoid sudden strenuous workouts without warming up.",
        "tablets": [
            {"name": "Naproxen (500mg) / Ibuprofen (400mg)", "type": "NSAID Pain Reliever", "dosage": "1 tablet at the earliest sign of aura/headache with food", "note": "Take with plenty of water"},
            {"name": "Sumatriptan (50mg)", "type": "Triptan (Migraine-Specific Prescription)", "dosage": "1 tablet at onset of migraine; repeat in 2h if needed (Max 200mg/day)", "note": "Constricts cranial vessels; prescription required"},
            {"name": "Domperidone (10mg) / Ondansetron (4mg)", "type": "Antiemetic", "dosage": "1 tablet 30 minutes before pain medication", "note": "Relieves nausea and helps body absorb pain medication"},
            {"name": "Magnesium Glycinate (400mg)", "type": "Preventive Supplement", "dosage": "1 tablet daily at night", "note": "Reduces frequency and severity of attacks"}
        ]
    },

    "Gastroenteritis": {
        "precautions": [
            "Focus primarily on hydration to replace fluids and electrolytes lost through vomiting and diarrhea",
            "Sip small amounts of liquids frequently rather than large gulps",
            "Wash hands thoroughly after using the bathroom and before handling food",
            "Avoid taking anti-motility drugs if fever or bloody stool is present",
            "Seek medical care if unable to keep fluids down for >24 hours",
        ],
        "lifestyle": [
            "Rest adequately and allow the digestive system time to recover",
            "Gradually reintroduce bland solid foods as tolerance improves",
            "Disinfect household bathroom surfaces with bleach-based cleaners",
        ],
        "foods_recommended": [
            "BRAT diet: Bananas, Rice (white), Applesauce, Toast (plain white)",
            "Oral Rehydration Salts (ORS) and electrolyte solutions",
            "Clear chicken or vegetable broths and coconut water",
            "Plain oatmeal and boiled potatoes",
        ],
        "foods_to_avoid": [
            "Dairy products (milk, cheese, butter) — temporary lactose intolerance is common",
            "High-fat, greasy, fried, and spicy foods",
            "High-sugar snacks and juices (can worsen diarrhea)",
            "Caffeinated beverages and alcohol",
        ],
        "exercise": "Rest completely. Avoid exercise until hydration and bowel movements return to normal.",
        "tablets": [
            {"name": "Oral Rehydration Salts (ORS)", "type": "Electrolyte Therapy (Essential)", "dosage": "Dissolve 1 packet in 1 liter clean water; sip constantly", "note": "Replaces vital sodium, potassium & glucose"},
            {"name": "Loperamide (2mg)", "type": "Antidiarrheal", "dosage": "2mg after each loose stool (Max 8mg/day)", "note": "⚠️ Do NOT take if fever or bloody stool is present"},
            {"name": "Ondansetron (4mg) / Domperidone (10mg)", "type": "Antiemetic", "dosage": "1 tablet 30 mins before drinking/eating", "note": "Controls severe vomiting"},
            {"name": "Probiotic (Saccharomyces boulardii 250mg)", "type": "Gut Flora Probiotic", "dosage": "1 capsule twice daily with water", "note": "Restores intestinal lining and shortens diarrhea duration"}
        ]
    },

    "UTI": {
        "precautions": [
            "Consult a doctor for a clean-catch urine analysis (culture & sensitivity)",
            "Drink plenty of water to flush bacteria out of the urinary tract",
            "Do not delay or hold urine; empty bladder completely and frequently",
            "Wipe from front to back to avoid spreading bacteria from the anal region",
            "Urinate shortly after sexual intercourse",
        ],
        "lifestyle": [
            "Wear loose, breathable cotton underwear",
            "Avoid holding urine for extended periods",
            "Avoid feminine hygiene sprays, douches, and scented bath products",
            "Take showers instead of tub baths",
        ],
        "foods_recommended": [
            "Pure unsweetened cranberry juice or cranberry extract",
            "High water-content fruits and vegetables (cucumbers, watermelons)",
            "Probiotic yoghurt and fermented foods",
            "Vitamin C rich foods to help acidify urine",
        ],
        "foods_to_avoid": [
            "Caffeine, coffee, and energy drinks (irritate bladder lining)",
            "Alcohol and carbonated soft drinks",
            "Spicy and highly acidic foods",
            "Artificial sweeteners",
        ],
        "exercise": "Gentle walking is fine. Avoid cycling and swimming until symptoms resolve.",
        "tablets": [
            {"name": "Nitrofurantoin (100mg) / Ciprofloxacin (500mg)", "type": "Antibiotic (Prescription Only)", "dosage": "1 tablet twice daily for 5-7 days", "note": "Mandatory to complete full course; doctor prescription required"},
            {"name": "Phenazopyridine (100mg / 200mg)", "type": "Urinary Analgesic", "dosage": "1 tablet 3 times daily with meals for 2 days", "note": "Relieves burning pain and urgency (turns urine bright orange)"},
            {"name": "Cranberry Extract + D-Mannose (500mg)", "type": "Urinary Health Supplement", "dosage": "1 tablet twice daily with large glass of water", "note": "Prevents E. coli from adhering to bladder walls"},
            {"name": "Alkalizing Agent (Disodium Hydrogen Citrate)", "type": "Urine Alkalizer Syrup", "dosage": "2 teaspoons in 1 glass of water twice daily", "note": "Reduces burning sensation during urination"}
        ]
    },

    "Anxiety Disorder": {
        "precautions": [
            "Practice slow, deep diaphragmatic breathing (4-7-8 breathing method)",
            "Avoid stimulants like excess caffeine, energy drinks, and nicotine",
            "Maintain a strong support network — talk to friends, family, or a counselor",
            "Seek professional mental health evaluation (cognitive behavioral therapy)",
            "Never stop prescribed psychiatric medications abruptly",
        ],
        "lifestyle": [
            "Establish a calm, screen-free evening wind-down routine",
            "Engage in daily mindfulness meditation for 10-15 minutes",
            "Spend time outdoors in nature and sunlight",
            "Keep a thought journal to reframe catastrophic thinking",
        ],
        "foods_recommended": [
            "Chamomile and lavender tea (natural calming herbs)",
            "Complex carbohydrates (whole grains, sweet potatoes, oats)",
            "Magnesium-rich foods (pumpkin seeds, spinach, dark chocolate)",
            "Omega-3 rich foods (walnuts, chia seeds, fatty fish)",
            "Fermented foods rich in probiotics for gut-brain axis",
        ],
        "foods_to_avoid": [
            "Excessive coffee, tea, and caffeinated energy drinks",
            "Refined sugars (causes rapid blood sugar spikes and crashes)",
            "Alcohol (can trigger rebound anxiety and panic attacks)",
            "Processed and deep-fried fast food",
        ],
        "exercise": "Daily brisk walking, jogging, cycling, yoga, and tai chi release endorphins and reduce cortisol naturally.",
        "tablets": [
            {"name": "Ashwagandha (KSM-66 500mg)", "type": "Natural Adaptogen Supplement", "dosage": "1 capsule twice daily with milk or water", "note": "Clinically proven to lower cortisol and anxiety levels"},
            {"name": "L-Theanine (200mg) + Magnesium Glycinate", "type": "Calming Amino Acid & Mineral", "dosage": "1 capsule in the evening", "note": "Promotes mental relaxation without causing drowsiness"},
            {"name": "Escitalopram / Sertraline (Prescription)", "type": "SSRI Antidepressant / Anxiolytic", "dosage": "Strictly as prescribed by a licensed psychiatrist", "note": "Requires psychiatric evaluation and gradual titration"}
        ]
    },

    "Anemia": {
        "precautions": [
            "Get a complete blood count (CBC) and serum ferritin test to identify anemia type",
            "Take iron supplements with Vitamin C (orange juice) for enhanced absorption",
            "Do NOT take iron supplements with tea, coffee, milk, or calcium (inhibits absorption)",
            "Identify the root cause (dietary deficiency, blood loss, malabsorption)",
            "Monitor for extreme fatigue, dizziness, pale skin, or shortness of breath",
        ],
        "lifestyle": [
            "Allow adequate rest between physical activities to prevent exhaustion",
            "Cook meals in cast-iron cookware to naturally boost iron content",
            "Ensure regular 8 hours of sleep per night",
        ],
        "foods_recommended": [
            "Iron-rich foods: Spinach, beetroot, lentils, chickpeas, and beans",
            "Animal proteins: Liver, lean red meat, poultry, and eggs",
            "Dried fruits: Raisins, dates, prunes, and dried figs",
            "Vitamin C rich foods to boost iron uptake (citrus, tomatoes, bell peppers)",
            "Pomegranate and black sesame seeds",
        ],
        "foods_to_avoid": [
            "Black tea and coffee within 2 hours of meals (tannins block iron absorption)",
            "Calcium supplements or high-calcium dairy taken at the same time as iron meals",
            "Processed and refined junk foods with low nutritional density",
        ],
        "exercise": "Light to moderate exercises like gentle walking, yoga, and stretching. Stop immediately if feeling dizzy or breathless.",
        "tablets": [
            {"name": "Ferrous Ascorbate + Folic Acid (100mg)", "type": "Iron Supplement (First-Line)", "dosage": "1 tablet daily after lunch with orange juice or water", "note": "Do NOT take with milk/tea; may cause dark stools (normal)"},
            {"name": "Vitamin B12 (Methylcobalamin 1500mcg)", "type": "Vitamin B12 Supplement", "dosage": "1 sublingual tablet daily", "note": "Essential for red blood cell synthesis, especially in vegetarians"},
            {"name": "Vitamin C (Ascorbic Acid 500mg)", "type": "Iron Absorption Enhancer", "dosage": "1 tablet along with iron supplement", "note": "Significantly boosts intestinal iron bioavailability"}
        ]
    },

    "COVID-19": {
        "precautions": [
            "Self-isolate immediately in a well-ventilated room to protect family members",
            "Monitor blood oxygen saturation (SpO2) every 4-6 hours with a pulse oximeter",
            "Seek emergency hospitalization immediately if SpO2 drops below 94% or breathing is difficult",
            "Wear a well-fitted N95 or KN95 mask if interacting with caregivers",
            "Stay well hydrated and take adequate rest",
        ],
        "lifestyle": [
            "Strict isolation and rest for at least 7 days",
            "Proning exercises (lying on belly) can help improve oxygenation if advised by doctor",
            "Keep the room well-ventilated with open windows or HEPA air filtration",
        ],
        "foods_recommended": [
            "Warm herbal teas with ginger, turmeric, tulsi, and honey",
            "High-protein meals (eggs, chicken soup, lentils, paneer) for tissue recovery",
            "Citrus fruits, berries, and kiwi for Vitamin C",
            "Coconut water and electrolyte drinks for hydration",
        ],
        "foods_to_avoid": [
            "Cold drinks, ice creams, and chilled foods",
            "Alcohol and smoking (severely aggravates respiratory tract)",
            "Ultra-processed and high-sodium junk foods",
        ],
        "exercise": "No physical workouts during active infection. Practice gentle breathing exercises and slow paced walking inside the room.",
        "tablets": [
            {"name": "Paracetamol (650mg)", "type": "Antipyretic / Analgesic", "dosage": "1 tablet every 6 hours as needed for fever and body ache", "note": "Keep body temperature below 100°F"},
            {"name": "Vitamin C (500mg) + Zinc (50mg)", "type": "Immune Optimization", "dosage": "1 tablet daily for 10 days", "note": "Supports cellular immune response"},
            {"name": "Vitamin D3 (60,000 IU)", "type": "Immune Modulator", "dosage": "1 sachet or tablet once weekly for 4 weeks", "note": "Improves respiratory immune defenses"},
            {"name": "Inhaled Budesonide / Inhaler", "type": "Respiratory Anti-inflammatory (Prescription)", "dosage": "As prescribed by doctor if persistent cough", "note": "Rinse mouth after inhalation"}
        ]
    },
}


# ── Public API ─────────────────────────────────────────────────────────────

def get_disease_info(disease: str) -> dict:
    """Return the full information dict for a disease."""
    return DISEASE_DATA.get(disease, {
        "precautions": ["Consult a healthcare professional for personalized medical advice."],
        "lifestyle": ["Maintain a balanced routine with sufficient rest and hydration."],
        "foods_recommended": ["Eat wholesome, nutrient-dense whole foods and stay hydrated."],
        "foods_to_avoid": ["Avoid processed junk foods, excess sugar, and alcohol."],
        "exercise": "Consult your physician regarding suitable physical activity.",
        "tablets": [
            {"name": "Consult Physician", "type": "Prescription", "dosage": "Follow clinical prescription", "note": "Always consult a registered physician before taking medications"}
        ]
    })


def get_all_recommendations(disease: str) -> dict:
    """Return the complete structured recommendations package for a disease."""
    info = dict(get_disease_info(disease))
    info["tablets"] = get_tablets(disease)
    return info


def is_emergency_condition(disease: str) -> bool:
    """Check if the condition warrants emergency red-flag warning."""
    emergency_diseases = {"Asthma", "Pneumonia", "COVID-19", "Dengue", "Malaria", "Hypertension"}
    return disease in emergency_diseases


def get_precautions(disease: str) -> list:
    return get_disease_info(disease)["precautions"]



def get_lifestyle(disease: str) -> list:
    return get_disease_info(disease)["lifestyle"]


def get_food_recommendation(disease: str) -> list:
    return get_disease_info(disease)["foods_recommended"]


def get_foods_to_avoid(disease: str) -> list:
    return get_disease_info(disease)["foods_to_avoid"]


def get_exercise_recommendation(disease: str) -> str:
    return get_disease_info(disease)["exercise"]


def get_tablets(disease: str) -> list:
    raw_tablets = get_disease_info(disease).get("tablets", [])
    enhanced = []
    for t in raw_tablets:
        item = dict(t)
        if "how_to_take" not in item:
            item["how_to_take"] = (
                "Take 1 tablet orally with a full glass of normal/warm water after food. "
                "Do not crush or chew. Maintain a consistent gap between doses. Avoid alcohol."
            )
        if "timing" not in item:
            item["timing"] = "After Meals (Morning / Night)"
        if "duration" not in item:
            item["duration"] = "3 to 5 Days (or as directed by physician)"
        enhanced.append(item)
    return enhanced


DOCTOR_SPECIALTY_MAP = {
    "Common Cold": {"name": "Dr. Anil Kumar, MD", "specialty": "Senior General Physician", "reg_no": "MCI-48291", "hospital": "Apex City Multi-Specialty Hospital"},
    "Influenza": {"name": "Dr. Anil Kumar, MD", "specialty": "Senior General Physician", "reg_no": "MCI-48291", "hospital": "Apex City Multi-Specialty Hospital"},
    "Hypertension": {"name": "Dr. Priya Sharma, MBBS, MD", "specialty": "Consultant Cardiologist", "reg_no": "MCI-59102", "hospital": "Metro Heart & Vascular Institute"},
    "Diabetes": {"name": "Dr. Ramesh Verma, MD, DM", "specialty": "Endocrinologist & Diabetologist", "reg_no": "MCI-37190", "hospital": "Care Diabetes & Metabolic Center"},
    "Asthma": {"name": "Dr. Sneha Patel, MD (Pulmonology)", "specialty": "Chest & Pulmonary Specialist", "reg_no": "MCI-62819", "hospital": "National Respiratory Center"},
    "Pneumonia": {"name": "Dr. Sneha Patel, MD (Pulmonology)", "specialty": "Chest & Pulmonary Specialist", "reg_no": "MCI-62819", "hospital": "National Respiratory Center"},
    "Bronchitis": {"name": "Dr. Sneha Patel, MD (Pulmonology)", "specialty": "Chest & Pulmonary Specialist", "reg_no": "MCI-62819", "hospital": "National Respiratory Center"},
    "COVID-19": {"name": "Dr. Vikram Sethi, MD (Infectious Diseases)", "specialty": "Infectious Disease Specialist", "reg_no": "MCI-77312", "hospital": "State Epidemic Response Hospital"},
    "Malaria": {"name": "Dr. Vikram Sethi, MD (Infectious Diseases)", "specialty": "Tropical Medicine & Infections", "reg_no": "MCI-77312", "hospital": "City Fever Care Clinic"},
    "Dengue": {"name": "Dr. Vikram Sethi, MD (Infectious Diseases)", "specialty": "Tropical Medicine & Infections", "reg_no": "MCI-77312", "hospital": "City Fever Care Clinic"},
    "Typhoid": {"name": "Dr. Anil Kumar, MD", "specialty": "Senior General Physician", "reg_no": "MCI-48291", "hospital": "Apex City Multi-Specialty Hospital"},
    "Migraine": {"name": "Dr. Rajesh Kulkarni, MD, DM", "specialty": "Consultant Neurologist", "reg_no": "MCI-88129", "hospital": "Brain & Spine Neuro Institute"},
    "Gastritis": {"name": "Dr. Meena Iyer, MD, DM", "specialty": "Gastroenterologist & Hepatologist", "reg_no": "MCI-44918", "hospital": "Digestive Health Foundation"},
    "GERD": {"name": "Dr. Meena Iyer, MD, DM", "specialty": "Gastroenterologist & Hepatologist", "reg_no": "MCI-44918", "hospital": "Digestive Health Foundation"},
    "Arthritis": {"name": "Dr. Sanjay Gupta, MS (Ortho)", "specialty": "Orthopedic & Rheumatology Specialist", "reg_no": "MCI-52901", "hospital": "Joint & Bone Care Clinic"},
    "Allergy": {"name": "Dr. Kavita Nair, MD (Dermatology)", "specialty": "Allergist & Dermatologist", "reg_no": "MCI-63820", "hospital": "Skin & Allergy Specialty Clinic"}
}


def get_prescribing_doctor(disease: str) -> dict:
    return DOCTOR_SPECIALTY_MAP.get(disease, {
        "name": "Dr. Anil Kumar, MD",
        "specialty": "Senior General Physician & Medical Officer",
        "reg_no": "MCI-48291",
        "hospital": "Apex Health Multi-Specialty Hospital"
    })


def get_all_diseases() -> list:
    return list(DISEASE_DATA.keys())
