# -*- coding: utf-8 -*-
"""
Created on Sat May 17 13:06:59 2025

@author: USER
"""

import streamlit as st
import pandas as pd
import joblib
import re

#from PyPDF2 import PdfReader
import docx2txt
from sentence_transformers import SentenceTransformer
import numpy as np


# Load models and vectorizers
category_model = joblib.load("resume_category_classifier.pkl")
category_vectorizer = joblib.load("resume_tfidf_vectorizer.pkl")
recommendation_model = joblib.load("xgboost_resume_match_model.pkl")
recommendation_vectorizer = joblib.load("xgboost_tfidf_vectorizer.pkl")
bert_model = SentenceTransformer("all-MiniLM-L6-v2")

# Load job descriptions
df_jobs = pd.read_csv("job_descriptions_with_full_extraction.csv")
df_jobs.fillna("", inplace=True)

# ------------------------------
# Utility Functions
# ------------------------------
def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    return text

def extract_text_from_docx(uploaded_file):
    return docx2txt.process(uploaded_file)

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()

def extract_features(resume_text):
    # Dummy extraction for static example (replace with real pipeline)
    return {
        "Name": "Ava Thompson",
        "Phone": "(374) 136-7622",
        "Email": "ava.thompson@example.com",
        "Education": "Bachelor of Human Resources, NYU, 2015",
        "Soft Skills": "communication, teamwork, organization",
        "Technical Skills": "Workday, payroll, onboarding",
        "Experience": "HR Generalist, PeopleFirst Solutions — 2018 to Present | HR Assistant, BrightHire — 2015 to 2018"
    }

def predict_category(text):
    text_cleaned = clean_text(text)
    vec = category_vectorizer.transform([text_cleaned])
    return category_model.predict(vec)[0]

def get_top_5_recommendations(resume_text, resume_category):
    resume_clean = clean_text(resume_text)
    resume_vec = recommendation_vectorizer.transform([resume_clean])
    resume_embed = bert_model.encode(resume_clean)

    job_scores = []
    for _, j in df_jobs[df_jobs["Category"] == resume_category].iterrows():
        job_clean = clean_text(f"{j['Extracted Education']} {j['Extracted Skills']} {j['Extracted Duties']}")
        job_vec = recommendation_vectorizer.transform([job_clean])
        job_embed = bert_model.encode(job_clean)

        combined_vec = np.hstack((resume_vec.toarray()[0], job_vec.toarray()[0]))
        match_prob = recommendation_model.predict_proba([combined_vec])[0][1]

        similarity = np.dot(resume_embed, job_embed) / (np.linalg.norm(resume_embed) * np.linalg.norm(job_embed))

        job_scores.append({
            "Job Title": j["Job Title"],
            "Company": j.get("Company Name", ""),
            "Category": j["Category"],
            "Match Probability": round(match_prob, 3),
            "BERT Similarity": round(similarity, 3)
        })

    return sorted(job_scores, key=lambda x: x["Match Probability"], reverse=True)[:5]

# ------------------------------
# Streamlit App
# ------------------------------
st.set_page_config(page_title="Resume Matcher", layout="wide")
st.title("🔍 Resume Analysis & Job Matching")

uploaded_file = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])

if uploaded_file:
    # Extract raw resume text
    if uploaded_file.name.endswith(".pdf"):
        resume_text = extract_text_from_pdf(uploaded_file)
    else:
        resume_text = extract_text_from_docx(uploaded_file)

    st.subheader("📄 Uploaded Resume")
    st.text(resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text)

    # Extract features
    st.subheader("🔍 Extracted Resume Features")
    extracted = extract_features(resume_text)
    st.dataframe(pd.DataFrame([extracted]))

    # Predict category
    st.subheader("📌 Predicted Resume Category")
    predicted_category = predict_category(resume_text)
    st.success(f"Predicted Category: {predicted_category}")

    # Top 5 job recommendations
    st.subheader("📈 Top 5 Job Recommendations")
    recommendations = get_top_5_recommendations(resume_text, predicted_category)
    st.table(pd.DataFrame(recommendations))
