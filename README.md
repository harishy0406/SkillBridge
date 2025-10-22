
# SkillBridge: AI-Powered Job & Course Recommender

[![Python](https://img.shields.io/badge/python-3.10-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/streamlit-v1.25-orange?logo=streamlit)](https://streamlit.io/)


## 🚀 Project Overview

**SkillBridge** is an AI-powered platform that helps users discover personalized **job recommendations**, **career guidance**, and **skill-based course suggestions**. It is designed for **students, freshers, and professionals** seeking career opportunities tailored to their skills and education.

Key features include:

- **Job Recommendation Engine**: Matches user skills, education, region, language, and preferred job type with suitable jobs.
- **Course Recommendations**: Suggests courses that improve the user's skills for career growth.
- **Multilingual Support**: English, Hindi, and Tamil.
- **Chatbot AI**: Conversational assistant that provides career guidance using AI.
- **Streamlit Web UI**: Interactive and visually appealing interface with tables and background images.
- **Data Visualization**: Insights into skills, job distribution, and locations.


## 📂 Folder Structure

```bash
SkillBridge/
│
├─ app/
│   ├─ recommender.py
│   ├─ chatbot_ai.py
│   └─ streamlit_app.py
│
├─ data/
│   ├─ users.csv
│   ├─ jobs.csv
│   └─ courses.csv
│
├─ notebooks/
│   ├─ EDA.ipynb
│   └─ model_training.ipynb
│
├─ requirements.txt
└─ README.md
```


## 🧰 Tech Stack

- Python 3.x
- Streamlit for UI
- Pandas & NumPy for data handling
- Scikit-learn for ML models (Random Forest, Naive Bayes)
- TF-IDF Vectorizer for skills and education features
- SambaNova API / Perplexity API for AI-powered chatbot
- Matplotlib & Seaborn for visualizations


## ⚙️ Installation

1. Clone the repository:

```bash
git clone https://github.com/harishy0406/SkillBridge.git
cd SkillBridge
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
# Windows
venv\\Scripts\\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the Streamlit app:

```bash
streamlit run app/chatbot_ui.py
```

## 📈 Example Outputs

**Job Recommendations Table** and **Course Recommendations Table**

1. Chatbot Input :

<img width="1817" height="671" alt="image" src="https://github.com/user-attachments/assets/7b321a07-1890-4cc6-8e93-cee60bfc42db" />

2. Output Recommendation in streamlit :

<img width="1813" height="766" alt="image" src="https://github.com/user-attachments/assets/4c0bf629-de03-4dd4-bc77-85aaa08218ac" />

3. Output Recommendation in CLI :
   
<img width="1183" height="700" alt="image" src="https://github.com/user-attachments/assets/ef02eb0f-8a8c-4707-8891-4dfe428a8267" />






## 🌟 Future Enhancements

- More multilingual support
- Live job postings integration
- Cloud deployment
- Enhanced AI chatbot with interactive options

## 🤝 Contribution  
   
Want to contribute? Feel free to fork the repo and create a pull request with your ideas. Let’s make **EduVault** even better! 💡  

---

