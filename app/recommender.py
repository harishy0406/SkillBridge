import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from difflib import get_close_matches



def clean_text(text):
    """
    Lowercase, remove punctuation, and extra spaces
    """
    if pd.isnull(text):
        return ""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Load datasets
users_df = pd.read_csv('data/users.csv')
jobs_df = pd.read_csv('data/jobs.csv')
courses_df = pd.read_csv('data/courses.csv')  

def recommend_jobs(user_input, top_n=5):
    """
    user_input: dict with keys
        'skills', 'education', 'region', 'language', 'preferred_job_type'
    """
    # Clean user skills and education
    user_skills = clean_text(user_input.get('skills', ''))
    user_education = clean_text(user_input.get('education', ''))
    user_region = user_input.get('region', '').lower()
    user_language = user_input.get('language', '').lower()
    preferred_job_type = user_input.get('preferred_job_type', '').lower()

    # Preprocess job dataset
    jobs_df['skills_clean'] = jobs_df['required_skills'].apply(clean_text)
    jobs_df['education_clean'] = jobs_df['education_required'].apply(clean_text)
    jobs_df['region_clean'] = jobs_df['region'].apply(lambda x: str(x).lower())
    jobs_df['language_clean'] = jobs_df['language_preference'].apply(lambda x: str(x).lower())
    jobs_df['job_type_clean'] = jobs_df['job_type'].apply(lambda x: str(x).lower())

    # Combine skills + education for vectorization
    jobs_df['combined_text'] = jobs_df['skills_clean'] + ' ' + jobs_df['education_clean']

    # TF-IDF Vectorizer
    vectorizer = TfidfVectorizer()
    job_vectors = vectorizer.fit_transform(jobs_df['combined_text'])
    user_vector = vectorizer.transform([user_skills + ' ' + user_education])

    # Cosine similarity
    similarity = cosine_similarity(user_vector, job_vectors).flatten()
    jobs_df['similarity'] = similarity

    # Initialize filtered_jobs
    filtered_jobs = jobs_df.copy()

    # Filter by job_type using closest match
    available_job_types = jobs_df['job_type'].unique()
    user_job_type = user_input['preferred_job_type']
    closest_match = get_close_matches(user_job_type, available_job_types, n=1, cutoff=0.6)
    if closest_match:
        user_job_type = closest_match[0]

    if user_job_type:
        filtered_jobs = filtered_jobs[filtered_jobs['job_type'].str.lower() == user_job_type.lower()]

    if 'region' in filtered_jobs.columns and user_input['region']:
        filtered_jobs = filtered_jobs[filtered_jobs['region'].str.lower() == user_input['region'].lower()]

    if 'language' in filtered_jobs.columns and user_input['language']:
        filtered_jobs = filtered_jobs[filtered_jobs['language'].str.lower() == user_input['language'].lower()]

    if 'job_type' in filtered_jobs.columns and user_input['preferred_job_type']:
        filtered_jobs = filtered_jobs[filtered_jobs['job_type'].str.lower() == user_input['preferred_job_type'].lower()]


    # If nothing found, relax filters
    if filtered_jobs.empty:
        filtered_jobs = jobs_df


    # Sort by similarity
    top_jobs = filtered_jobs.sort_values(by='similarity', ascending=False).head(top_n)

    # Optional: recommend courses
    recommended_courses = []
    for skill in user_skills.split(','):
        skill = skill.strip()
        courses = courses_df[courses_df['related_skill'].str.contains(skill, case=False, na=False)]
        recommended_courses.extend(courses['course_name'].tolist())

    return top_jobs, recommended_courses

if __name__ == "__main__":
    
    print("Welcome to SkillBridge Job Recommender!\nPlease enter your details:")

    skills = input("Enter your skills (comma-separated, e.g., electrical, wiring, maintenance): ").lower()
    education = input("Enter your highest education (e.g., Diploma in Electrical): ").lower()
    region = input("Enter your region/state (e.g., Tamil Nadu): ").title()
    language = input("Enter your preferred language (e.g., Tamil): ").title()
    preferred_job_type = input("Enter preferred job type (e.g., government, private): ").lower()

    user_input = {
        'skills': skills,
        'education': education,
        'region': region,
        'language': language,
        'preferred_job_type': preferred_job_type
    }

    # --- Get job recommendations ---
    jobs, _ = recommend_jobs(user_input, top_n=5)

    print("\nTop Jobs:")
    if not jobs.empty:
        print(jobs[['job_title', 'company_name', 'location', 'salary']])
    else:
        print("No matching jobs found.")

    # --- Smart Course Recommendation (TF-IDF Similarity) ---
    print("\nRecommended Courses:")

    try:
        # Load courses dataset
        courses_df = pd.read_csv("data/courses.csv")

        # Combine course name + related skills for richer context
        courses_df["combined_text"] = courses_df["course_name"].fillna("") + " " + courses_df["related_skill"].fillna("")

        # Create TF-IDF matrix
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(courses_df["combined_text"])

        # Transform user skills into TF-IDF vector
        user_vector = vectorizer.transform([skills])

        # Compute cosine similarity between user skills and all courses
        similarity_scores = cosine_similarity(user_vector, tfidf_matrix).flatten()

        # Attach scores to dataframe
        courses_df["similarity"] = similarity_scores

        # Sort by similarity
        top_courses = courses_df.sort_values(by="similarity", ascending=False).head(5)

        # Display top courses only if score > 0
        top_courses = top_courses[top_courses["similarity"] > 0]

    
        # Load courses dataset
        courses_df = pd.read_csv("data/courses.csv")

        # Extract user skills
        user_skills = [s.strip().lower() for s in skills.split(",")]

        # Match courses whose related skills overlap with user skills
        matched_courses = courses_df[
            courses_df['related_skill'].apply(
                lambda x: any(skill in x.lower() for skill in user_skills)
            )
        ]

        # --- Remove duplicates ---
        top_courses = matched_courses.drop_duplicates(subset='course_name')

        # --- Print courses neatly ---
        if not top_courses.empty:
            for _, row in top_courses.iterrows():
                print(f"- {row['course_name']}  ({row.get('provider', 'Unknown Provider')})")
        else:
            print("No closely matching courses found for your skills.")

    except Exception as e:
            print("Error loading or processing courses:", e)

