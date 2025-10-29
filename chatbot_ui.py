import streamlit as st
from sambanova import SambaNova

# -------------------- CONFIG --------------------
API_KEY = "27c9b911-0a48-4a28-b6d2-4119e6ac8863"

client = SambaNova(
    api_key=API_KEY,
    base_url="https://api.sambanova.ai/v1",
)

career_guidance_prompts = {
    "intro": {
        "en": "Hello! I am your AI career assistant. Let's start by understanding your skills and preferences.",
        "hi": "नमस्ते! मैं आपका AI करियर असिस्टेंट हूँ। चलिए आपकी स्किल्स और प्राथमिकताओं को जानते हैं।",
    },
    "ask_skills": {
        "en": "Please enter your skills (comma-separated): ",
        "hi": "कृपया अपनी स्किल्स दर्ज करें (कॉमा से अलग करें): ",
    },
    "ask_education": {
        "en": "What is your highest education? ",
        "hi": "आपकी उच्चतम शिक्षा क्या है? ",
    },
    "ask_region": {
        "en": "Which region/state are you from? ",
        "hi": "आप किस राज्य/क्षेत्र से हैं? ",
    },
    "ask_language": {
        "en": "Which language should we chat in? (English/Hindi): ",
        "hi": "हमें किस भाषा में चैट करनी चाहिए? (English/Hindi): ",
    }
}


# -------------------- FUNCTION TO CALL SAMBANOVA --------------------
def ai_chat(user_input):
    """
    Send input to SambaNova API and return AI response.
    """
    try:
        response = client.chat.completions.create(
            model="Meta-Llama-3.1-8B-Instruct",
            messages=[{"role": "user", "content": user_input}],
            temperature=0.1,
            top_p=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error contacting AI: {e}"

# -------------------- STREAMLIT UI --------------------
def main():
    st.set_page_config(page_title="SkillBridge AI Chatbot", layout="wide")
    st.title("💬 SkillBridge AI Career Chatbot")
    
    st.markdown(
        "Interact with an AI assistant that provides personalized **job recommendations**, **courses**, "
        "and **career guidance** based on your skills, education, and region."
    )
    
    # --- Language selection ---
    language = st.selectbox(
        "Select Language / भाषा ",
        ("English", "Hindi")
    )
    lang_code = "en" if language == "English" else "hi" if language == "Hindi" else "ta"
    
    # --- User input fields ---
    skills = st.text_input("Enter your skills (comma-separated, e.g., electrical, wiring, maintenance)")
    education = st.text_input("Enter your highest education (e.g., Diploma in Electrical)")
    region = st.text_input("Enter your region/state (e.g., Tamil Nadu)")
    
    if st.button("Get Career Recommendations"):
        if not skills or not education or not region:
            st.warning("Please fill in all fields!")
        else:
            with st.spinner("Generating AI recommendations..."):
                # Prepare user query
                user_query = (
                    f"I am from {region}, with education {education}, and skills {skills}, and language{lang_code} "
                    f"Please provide personalized job recommendations (minimum 7-8 jobs) with job title, company name, location, and salary in a clear bullet point format.in the selected language"
                    f"Also provide 7-8 course recommendations with course name, provider, and link. "
                    f"and Extra Carrer Guidance 3-4 points."
                    f"Give the output without bold letters or extra formatting."
                )
                
                # Get AI response
                response = ai_chat(user_query)
                
                st.subheader("SkillBridge Job Recommendations:")
                st.text_area("Model Response", value=response, height=500)

# -------------------- ENTRY POINT --------------------
if __name__ == "__main__":
    main()
