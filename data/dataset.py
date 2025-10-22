import pandas as pd
import numpy as np
from faker import Faker
import random

fake = Faker()

# -----------------------------
# Parameters
# -----------------------------
num_rows = 800  # Number of users
job_rows = 200  # Number of jobs
course_rows = 50  # Number of courses

# -----------------------------
# 1️⃣ Generate Users Dataset
# -----------------------------
education_levels = ['High School', 'ITI', 'Diploma', 'Bachelor', 'Master']
skills_list = ['electrical', 'wiring', 'maintenance', 'plumbing', 'computer', 'accounting', 'mechanics']
job_types = ['Government', 'Private', 'Technician', 'Operator', 'Clerk']
regions = ['Tamil Nadu', 'Kerala', 'Bihar', 'Uttar Pradesh', 'Maharashtra']
languages = ['English', 'Hindi', 'Tamil', 'Telugu', 'Malayalam']

users_data = []

for i in range(1, num_rows + 1):
    skill_sample = random.sample(skills_list, k=random.randint(1, 3))
    user = {
        'user_id': i,
        'name': fake.first_name(),
        'age': random.randint(18, 35),
        'gender': random.choice(['M','F']),
        'education': random.choice(education_levels),
        'skills': ', '.join(skill_sample),
        'experience': f"{random.randint(0,5)} years",
        'preferred_job_type': random.choice(job_types),
        'region': random.choice(regions),
        'language': random.choice(languages),
        'interests': random.choice(['Government job', 'Private job', 'Training', 'Internship'])
    }
    users_data.append(user)

users_df = pd.DataFrame(users_data)
users_df.to_csv('users.csv', index=False)
print("Users dataset generated: users.csv")

# -----------------------------
# 2️⃣ Generate Jobs Dataset
# -----------------------------
job_titles = ['Electrical Technician', 'Plumber', 'Computer Operator', 'Accountant', 'Mechanic']

jobs_data = []
for i in range(1, job_rows + 1):
    skill_sample = random.sample(skills_list, k=random.randint(1, 3))
    job = {
        'job_id': i,
        'job_title': random.choice(job_titles),
        'company_name': fake.company(),
        'required_skills': ', '.join(skill_sample),
        'experience_required': f"{random.randint(0,3)}+ years",
        'education_required': random.choice(education_levels),
        'salary': f"₹{random.randint(10000,50000)} per month",
        'job_type': random.choice(job_types),
        'location': fake.city(),
        'region': random.choice(regions),
        'language_preference': random.choice(languages),
        'apply_link': fake.url()
    }
    jobs_data.append(job)

jobs_df = pd.DataFrame(jobs_data)
jobs_df.to_csv('jobs.csv', index=False)
print("Jobs dataset generated: jobs.csv")

# -----------------------------
# 3️⃣ Generate Courses Dataset
# -----------------------------
course_names = ['Electrician Level 1', 'Computer Basics', 'Plumbing Fundamentals', 'Mechanics Training', 'Accountancy Skills']

courses_data = []
for i in range(1, course_rows + 1):
    skill_sample = random.sample(skills_list, k=random.randint(1, 2))
    course = {
        'course_id': i,
        'course_name': random.choice(course_names),
        'related_skill': ', '.join(skill_sample),
        'provider': random.choice(['Skill India', 'NSDC', 'Coursera']),
        'region': random.choice(regions),
        'link': fake.url()
    }
    courses_data.append(course)

courses_df = pd.DataFrame(courses_data)
courses_df.to_csv('courses.csv', index=False)
print("Courses dataset generated: courses.csv")
