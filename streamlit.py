import streamlit as st
import pandas as pd

st.set_page_config(page_title="Static Resume Matcher", layout="centered")
st.title("🔍 AI Resume Matcher (Static Upload Demo)")

# ----------------------------
# 1. Upload Resume (Word or PDF)
# ----------------------------
st.header("📤 Upload Resume (PDF or DOCX)")
uploaded_file = st.file_uploader("Upload your resume:", type=["pdf", "docx"])

if uploaded_file is not None:
    st.success(f"✅ You uploaded: `{uploaded_file.name}`")

    # ----------------------------
    # 2. Display Resume Content (Static Simulation)
    # ----------------------------
    st.header("📄 Resume Preview (Static Example)")
    st.markdown("""
    Ava Thompson  
    Phone: (374) 136-7622  
    Email: ava.thompson@example.com  

    Professional Summary  
    HR professional with 6+ years of experience in recruitment, employee relations, and compliance management.  

    Education  
    Bachelor of Human Resources, NYU, 2015  

    Experience  
    HR Generalist, PeopleFirst Solutions — 2018 to Present  
    - Managed employee onboarding and exit processes.  
    - Ensured HRIS data accuracy using Workday.  
    - Led training sessions on company policies and diversity.  

    HR Assistant, BrightHire — 2015 to 2018  
    - Supported recruitment operations and scheduled interviews.  
    - Processed payroll and maintained compliance records.  

    Skills  
    Recruitment, Onboarding, HR Compliance, Payroll, Workday
    """)

    # ----------------------------
    # 3. Predicted Category (Simulated)
    # ----------------------------
    st.header("📌 Predicted Resume Category")
    st.success("✅ **Human Resources (HR)**")

    # ----------------------------
    # 4. Extracted Features
    # ----------------------------
    st.header("🧾 Extracted Resume Features")
    extracted_features = {
        "Name": "Ava Thompson",
        "Phone": "(374) 136-7622",
        "Email": "ava.thompson@example.com",
        "Education": "Bachelor of Human Resources, NYU, 2015",
        "Soft Skills": "Communication, Organization, Empathy",
        "Technical Skills": "Workday, HRIS, Payroll Systems",
        "Experience": "HR Generalist at PeopleFirst (2018–Present), HR Assistant at BrightHire (2015–2018)"
    }

    for key, value in extracted_features.items():
        st.markdown(f"**{key}:** {value}")

    # ----------------------------
    # 5. Top 5 Job Recommendations
    # ----------------------------
    st.header("💼 Top 5 Job Recommendations")

    recommendations = [
        {
            "Job Title": "HR Coordinator",
            "Company": "TalentBridge",
            "Category": "Human Resources (HR)",
            "Match Score": 0.87,
            "Explanation": "Strong match based on HRIS tools, payroll, and training duties."
        },
        {
            "Job Title": "Recruitment Specialist",
            "Company": "EdgeCorp",
            "Category": "Human Resources (HR)",
            "Match Score": 0.84,
            "Explanation": "Excellent overlap in recruitment experience and communication skills."
        },
        {
            "Job Title": "HR Generalist",
            "Company": "BrightWave Inc.",
            "Category": "Human Resources (HR)",
            "Match Score": 0.81,
            "Explanation": "Experience in onboarding and compliance aligns well with role."
        },
        {
            "Job Title": "People Operations Associate",
            "Company": "NextGen Talent",
            "Category": "Human Resources (HR)",
            "Match Score": 0.79,
            "Explanation": "Good match with HR process optimization and system usage."
        },
        {
            "Job Title": "Payroll & Benefits Analyst",
            "Company": "FinWise",
            "Category": "Human Resources (HR)",
            "Match Score": 0.76,
            "Explanation": "Payroll systems and employee relations background fit role needs."
        },
    ]

    rec_df = pd.DataFrame(recommendations)
    st.table(rec_df[["Job Title", "Company", "Category", "Match Score"]])

    with st.expander("🔍 Match Explanations"):
        for job in recommendations:
            st.markdown(f"**{job['Job Title']} at {job['Company']}**")
            st.markdown(f"🧠 *{job['Explanation']}*")
            st.markdown("---")

else:
    st.warning("⏳ Please upload a resume (PDF or DOCX) to see results.")

st.caption("📌 This is a static prototype. The full system will dynamically analyze uploaded resumes.")
