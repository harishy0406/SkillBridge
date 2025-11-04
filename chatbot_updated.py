import streamlit as st
from sambanova import SambaNova

# -------------------- CONFIG --------------------
API_KEY = "27c9b911-0a48-4a28-b6d2-4119e6ac8863"

client = SambaNova(
    api_key=API_KEY,
    base_url="https://api.sambanova.ai/v1",
)

# -------------------- SAMBANOVA FUNCTION --------------------
def ai_chat(user_input):
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

# -------------------- STREAMLIT CHATBOT --------------------
def main():
    st.set_page_config(page_title="💬 SkillBridge AI Chatbot", layout="wide")
    st.title("💬 SkillBridge AI Career Chatbot")
    st.markdown("Your personal AI career assistant — guiding you with job and course recommendations.")

    # --- Session states to track progress ---
    if "step" not in st.session_state:
        st.session_state.step = 0
    if "lang_code" not in st.session_state:
        st.session_state.lang_code = "en"
    if "skills" not in st.session_state:
        st.session_state.skills = ""
    if "education" not in st.session_state:
        st.session_state.education = ""
    if "region" not in st.session_state:
        st.session_state.region = ""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # --- Chat history display ---
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.markdown(chat["content"])

    # --- Step-based conversation flow ---
    def ask_next_question():
        if st.session_state.step == 0:
            return "Hello! I am your AI career assistant. Which language would you like to use? (English/Hindi)"
        elif st.session_state.step == 1:
            return "Please enter your skills (comma-separated): "
        elif st.session_state.step == 2:
            return "What is your highest education?"
        elif st.session_state.step == 3:
            return "Which region/state are you from?"
        else:
            return None

    # --- User input box ---
    user_input = st.chat_input("Type your message here...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # --- Language selection ---
        if st.session_state.step == 0:
            if user_input.lower().startswith("h"):
                st.session_state.lang_code = "hi"
            else:
                st.session_state.lang_code = "en"
            st.session_state.step += 1

        elif st.session_state.step == 1:
            st.session_state.skills = user_input
            st.session_state.step += 1

        elif st.session_state.step == 2:
            st.session_state.education = user_input
            st.session_state.step += 1

        elif st.session_state.step == 3:
            st.session_state.region = user_input
            st.session_state.step += 1

            # --- Once all inputs collected ---
            with st.chat_message("assistant"):
                st.markdown("Got it! Let me analyze and generate recommendations...")

            user_query = (
                f"I am from {st.session_state.region}, with education {st.session_state.education}, "
                f"and skills {st.session_state.skills}. Please provide at least 7–8 job recommendations near to the region given in a tabluar format"
                f"with job title, company name, location, and salary in a clean table format. "
                f"Also provide 7–8 course recommendations with course name, provider, and link, "
                f"plus 3–4 career guidance tips. Respond in {st.session_state.lang_code} without bold letters."
            )

            with st.spinner("Analyzing your profile..."):
                response = ai_chat(user_query)

            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.session_state.step += 1

        # --- If still in Q&A phase ---
        if st.session_state.step < 4:
            next_question = ask_next_question()
            if next_question:
                st.session_state.chat_history.append({"role": "assistant", "content": next_question})

        st.rerun()

    # --- Start conversation if new ---
    if st.session_state.step == 0 and len(st.session_state.chat_history) == 0:
        st.session_state.chat_history.append({"role": "assistant", "content": ask_next_question()})
        st.rerun()

# -------------------- RUN --------------------
if __name__ == "__main__":
    main()
