import base64
from sambanova import SambaNova

# -------------------- CONFIG --------------------
API_KEY = "0f4f01cc-990d-44e9-86b5-7c0cb7fc643f"

client = SambaNova(
    api_key=API_KEY,
    base_url="https://api.sambanova.ai/v1",
)

# Predefined guidance templates
career_guidance_prompts = {
    "intro": {
        "en": "Hello! I am your AI career assistant. Let's start by understanding your skills and preferences.",
        "hi": "नमस्ते! मैं आपका AI करियर असिस्टेंट हूँ। चलिए आपकी स्किल्स और प्राथमिकताओं को जानते हैं।",
        "ta": "வணக்கம்! நான் உங்கள் AI தொழில் உதவியாளர். உங்கள் திறன்களை மற்றும் விருப்பங்களை அறிந்துகொள்வோம்."
    },
    "ask_skills": {
        "en": "Please enter your skills (comma-separated): ",
        "hi": "कृपया अपनी स्किल्स दर्ज करें (कॉमा से अलग करें): ",
        "ta": "உங்கள் திறன்களை உள்ளிடவும் (கொமா கொண்டு பிரித்து): "
    },
    "ask_education": {
        "en": "What is your highest education? ",
        "hi": "आपकी उच्चतम शिक्षा क्या है? ",
        "ta": "உங்கள் மிக உயர்ந்த கல்வி என்ன?"
    },
    "ask_region": {
        "en": "Which region/state are you from? ",
        "hi": "आप किस राज्य/क्षेत्र से हैं? ",
        "ta": "நீங்கள் எந்த மாநிலம்/பிராந்தியத்திலிருந்து வருகிறீர்கள்?"
    },
    "ask_language": {
        "en": "Which language should we chat in? (English/Hindi/Tamil): ",
        "hi": "हमें किस भाषा में चैट करनी चाहिए? (English/Hindi/Tamil): ",
        "ta": "நாம் எந்த மொழியில் உரையாட வேண்டும்? (English/Hindi/Tamil): "
    }
}

# -------------------- FUNCTION TO CALL SAMBANOVA --------------------
def ai_chat(user_input):
    """
    Send input to SambaNova API and return AI response.
    """
    try:
        response = client.chat.completions.create(
            model="Llama-4-Maverick-17B-128E-Instruct",
            messages=[{"role": "user", "content": user_input}],
            temperature=0.1,
            top_p=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error contacting AI: {e}"

# -------------------- MAIN CHATBOT --------------------
def chatbot():
    # Step 1: Ask preferred language
    lang = input(career_guidance_prompts['ask_language']['en']).strip().lower()
    if lang.startswith("h"):
        lang_code = "hi"
    elif lang.startswith("t"):
        lang_code = "ta"
    else:
        lang_code = "en"

    print("\n" + career_guidance_prompts['intro'][lang_code])

    # Step 2: Ask user details
    skills = input(career_guidance_prompts['ask_skills'][lang_code])
    education = input(career_guidance_prompts['ask_education'][lang_code])
    region = input(career_guidance_prompts['ask_region'][lang_code])

    # Step 3: Prepare user query for AI
    user_query = (
    f"I am from {region}, with education {education}, and skills {skills}. "
    f"Please provide personalized job recommendations (minimum 7-8 jobs) with job title, company name, location, and salary in a clear table format. "
    f"Also provide 7-8 course recommendations with course name, provider, and link. "
    f"Present everything in a plain table format, without bold letters or extra formatting. "
    f"Give the output in {lang_code}."
    )


    # Step 4: Get AI response
    print("\nSkillBridge Job Recommender:\n")
    response = ai_chat(user_query)
    print(response)

# -------------------- ENTRY POINT --------------------
if __name__ == "__main__":
    chatbot()




# SkillBridge: Job Recommendation using Trained Model

import pickle
import pandas as pd

# Load pre-trained model (SkillBridge_JobRecommender.pkl)
with open('SkillBridge_JobRecommender.pkl', 'rb') as f:
    model = pickle.load(f)

# Sample user input
user_data = {
    'skills': ['electrical', 'maintenance', 'wiring'],
    'education': 'Diploma in Electrical',
    'region': 'Tamil Nadu'
}

# Convert user input to DataFrame
input_df = pd.DataFrame([user_data])

# Predict suitable jobs
recommendations = model.predict(input_df)

# Display results
print("Recommended Jobs for You:")
for job in recommendations:
    print("-", job)
