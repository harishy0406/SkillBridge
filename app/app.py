import streamlit as st
import pandas as pd
from recommender import recommend_jobs


# Page setup
st.set_page_config(page_title="SkillBridge Job Recommender", layout="wide")
st.title("SkillBridge Job Recommender")
st.write("Your AI-powered job and course recommendations")
# --- Sidebar for user input ---
st.sidebar.header("Enter Your Details")

# Predefined options
regions = ['Tamil Nadu', 'Kerala', 'Bihar', 'Uttar Pradesh', 'Maharashtra', 'Karnataka', 'Andhra Pradesh', 'Telangana', 'West Bengal', 'Gujarat']
languages = ['English', 'Hindi', 'Tamil', 'Telugu', 'Malayalam', 'Kannada', 'Bengali', 'Marathi']
job_types = ['Government', 'Private', 'Technician', 'Operator', 'Clerk', 'Internship', 'Training']

skills_input = st.sidebar.text_input("Skills (comma-separated, e.g., electrical, wiring, maintenance)")
education_input = st.sidebar.text_input("Highest Education (e.g., Diploma in Electrical)")
region_input = st.sidebar.selectbox("Region/State", regions)
language_input = st.sidebar.selectbox("Preferred Language", languages)
job_type_input = st.sidebar.selectbox("Preferred Job Type", job_types)

# --- Button to get recommendations ---
if st.sidebar.button("Get Recommendations"):
    
    if not skills_input or not education_input:
        st.warning("Please enter at least skills and education to get recommendations.")
    else:
        user_input = {
            'skills': skills_input.lower(),
            'education': education_input.lower(),
            'region': region_input.title(),
            'language': language_input.title(),
            'preferred_job_type': job_type_input.lower()
        }

        # Get recommendations
        top_jobs, top_courses = recommend_jobs(user_input, top_n=5)

        # --- Display Jobs ---
        st.subheader("Top Job Recommendations")
        if not top_jobs.empty:
            st.dataframe(top_jobs[['job_title', 'company_name', 'location', 'salary']].reset_index(drop=True))
        else:
            st.info("No matching jobs found.")

        # --- Display Courses in table ---
        st.subheader("Recommended Courses Based on Skills")
        if top_courses:
            courses_df = pd.DataFrame(top_courses, columns=['Course Name'])
            st.dataframe(courses_df.reset_index(drop=True))
        else:
            st.info("No relevant courses found for your skills.")
