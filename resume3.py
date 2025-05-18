import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Static Resume Matcher", layout="centered")
st.title(" AI Resume Matcher (Static Upload Demo)")

# ----------------------------------
# Uploaded Resume (Simulated Logic)
# ----------------------------------

st.header(" Upload Resume (PDF or DOCX)")
uploaded_file = st.file_uploader("Upload your resume:", type=["pdf", "docx"])

# Sample resume data dictionary
example_data = {
    "Ava_Thompson_Resume.pdf": {
        "category": "Human Resources (HR)",
        "content": """Ava Thompson\nPhone: (374) 136-7622\nEmail: ava.thompson@example.com\n\nProfessional Summary\nHR professional with 6+ years of experience in recruitment, employee relations, and compliance management.\n\nEducation\nBachelor of Human Resources, NYU, 2015\n\nExperience\nHR Generalist, PeopleFirst Solutions — 2018 to Present\n- Managed employee onboarding and exit processes.\n- Ensured HRIS data accuracy using Workday.\n- Led training sessions on company policies and diversity.\n\nHR Assistant, BrightHire — 2015 to 2018\n- Supported recruitment operations and scheduled interviews.\n- Processed payroll and maintained compliance records.\n\nSkills\nRecruitment, Onboarding, HR Compliance, Payroll, Workday\n""",
        "features": {
            "Name": "Ava Thompson",
            "Phone": "(374) 136-7622",
            "Email": "ava.thompson@example.com",
            "Education": "Bachelor of Human Resources, NYU, 2015",
            "Soft Skills": "Communication, Organization, Empathy",
            "Technical Skills": "Workday, HRIS, Payroll Systems",
            "Experience": "HR Generalist at PeopleFirst (2018–Present), HR Assistant at BrightHire (2015–2018)"
        },
        "recommendations": [
            {"Job Title": "HR Coordinator", "Company": "TalentBridge", "Category": "Human Resources (HR)", "Match Score": 0.87, "Explanation": "Strong match based on HRIS tools, payroll, and training duties."},
            {"Job Title": "Recruitment Specialist", "Company": "EdgeCorp", "Category": "Human Resources (HR)", "Match Score": 0.84, "Explanation": "Excellent overlap in recruitment experience and communication skills."},
            {"Job Title": "HR Generalist", "Company": "BrightWave Inc.", "Category": "Human Resources (HR)", "Match Score": 0.81, "Explanation": "Experience in onboarding and compliance aligns well with role."},
            {"Job Title": "People Operations Associate", "Company": "NextGen Talent", "Category": "Human Resources (HR)", "Match Score": 0.79, "Explanation": "Good match with HR process optimization and system usage."},
            {"Job Title": "Payroll & Benefits Analyst", "Company": "FinWise", "Category": "Human Resources (HR)", "Match Score": 0.76, "Explanation": "Payroll systems and employee relations background fit role needs."}
        ]
    },
    "Liam_Scott_Resume.pdf": {
        "category": "Information Technology (IT)",
        "content": """Liam Scott\nPhone: (202) 555-8123\nEmail: liam.scott@devtech.com\n\nProfessional Summary\nFull-stack developer with 5+ years building scalable web apps with Django, React, and PostgreSQL.\n\nEducation\nBachelor of Computer Science, MIT, 2016\n\nExperience\nSoftware Engineer, NovaSoft — 2019 to Present\n- Built REST APIs with Django and Flask.\n- Implemented CI/CD using GitHub Actions and Docker.\n\nJunior Developer, CodePro — 2016 to 2019\n- Developed UI components in React and Redux.\n- Worked with PostgreSQL and MongoDB for backend services.\n\nSkills\nPython, Django, React, PostgreSQL, Git, Docker\n""",
        "features": {
            "Name": "Liam Scott",
            "Phone": "(202) 555-8123",
            "Email": "liam.scott@devtech.com",
            "Education": "Bachelor of Computer Science, MIT, 2016",
            "Soft Skills": "Teamwork, Analytical Thinking, Problem Solving",
            "Technical Skills": "Python, Django, React, PostgreSQL, Docker",
            "Experience": "Software Engineer at NovaSoft (2019–Present), Junior Developer at CodePro (2016–2019)"
        },
        "recommendations": [
            {"Job Title": "Backend Developer", "Company": "CloudCore", "Category": "Information Technology (IT)", "Match Score": 0.88, "Explanation": "Excellent Python/Django backend experience and CI/CD knowledge."},
            {"Job Title": "Full Stack Engineer", "Company": "NextGen Apps", "Category": "Information Technology (IT)", "Match Score": 0.85, "Explanation": "Strong experience with React and Django stack."},
            {"Job Title": "Software Engineer", "Company": "CodeBright", "Category": "Information Technology (IT)", "Match Score": 0.83, "Explanation": "Good backend/frontend balance and database skills."},
            {"Job Title": "DevOps Associate", "Company": "StreamOps", "Category": "Information Technology (IT)", "Match Score": 0.80, "Explanation": "Hands-on with Docker and GitHub Actions."},
            {"Job Title": "Platform Engineer", "Company": "TechWare", "Category": "Information Technology (IT)", "Match Score": 0.78, "Explanation": "Strong full-stack capabilities with scalable architectures."}
        ]
    },
    "Sophia_Moore_Resume.pdf": {
        "category": "Healthcare Professional",
        "content": """Sophia Moore\nPhone: (312) 404-2290\nEmail: sophia.moore@medline.org\n\nProfessional Summary\nRegistered Nurse with 8+ years of experience in emergency care and patient assessment in high-volume hospitals.\n\nEducation\nBachelor of Nursing, University of Illinois, 2014\n\nExperience\nER Nurse, City Hospital — 2016 to Present\n- Provided critical care in fast-paced ER setting.\n- Coordinated with physicians for trauma cases.\n\nNursing Assistant, Mercy Health — 2014 to 2016\n- Monitored vital signs and administered medications.\n- Assisted in daily care routines and charting.\n\nSkills\nPatient Care, Emergency Medicine, EHR Systems, IV Administration\n""",
        "features": {
            "Name": "Sophia Moore",
            "Phone": "(312) 404-2290",
            "Email": "sophia.moore@medline.org",
            "Education": "Bachelor of Nursing, University of Illinois, 2014",
            "Soft Skills": "Compassion, Communication, Decision Making",
            "Technical Skills": "EHR Systems, Emergency Response, IV Setup",
            "Experience": "ER Nurse at City Hospital (2016–Present), Nursing Assistant at Mercy Health (2014–2016)"
        },
        "recommendations": [
            {"Job Title": "Emergency RN", "Company": "MetroCare", "Category": "Healthcare Professional", "Match Score": 0.89, "Explanation": "ER and trauma experience fits perfectly."},
            {"Job Title": "Clinical Nurse", "Company": "HealthFirst", "Category": "Healthcare Professional", "Match Score": 0.85, "Explanation": "Skilled in emergency and patient management systems."},
            {"Job Title": "Nursing Supervisor", "Company": "St. Mary's Medical", "Category": "Healthcare Professional", "Match Score": 0.84, "Explanation": "Leadership potential and critical care history."},
            {"Job Title": "Hospital Shift Lead", "Company": "PulsePlus Clinics", "Category": "Healthcare Professional", "Match Score": 0.82, "Explanation": "ER routine coordination and team collaboration experience."},
            {"Job Title": "ICU Nurse", "Company": "Lifeline Hospital", "Category": "Healthcare Professional", "Match Score": 0.80, "Explanation": "Ready for high-pressure clinical environment."}
        ]
    }
}

# ----------------------------
# Detect Uploaded Resume
# ----------------------------
if uploaded_file is not None:
    resume_key = uploaded_file.name

    if resume_key in example_data:
        resume = example_data[resume_key]

        st.success(f" You uploaded: `{resume_key}`")

        # 2. Resume Content
        st.header("📄 Resume Preview")
        st.markdown(resume["content"])

        # 3. Predicted Category
        st.header(" Predicted Resume Category")
        st.success(f" **{resume['category']}**")

        # 4. Extracted Features
        st.header("🧾 Extracted Resume Features")
        for key, value in resume["features"].items():
            st.markdown(f"**{key}:** {value}")

        # 5. Job Recommendations
        st.header("💼 Top 5 Job Recommendations")
        rec_df = pd.DataFrame(resume["recommendations"])
        st.table(rec_df[["Job Title", "Company", "Category", "Match Score"]])

        with st.expander("🔍 Match Explanations"):
            for job in resume["recommendations"]:
                st.markdown(f"**{job['Job Title']} at {job['Company']}**")
                st.markdown(f"🧠 *{job['Explanation']}*")
                st.markdown("---")
    else:
        st.warning("⚠️ This resume is not recognized in the static demo.")
else:
    st.info("📁 Please upload one of the sample resumes (PDF): Ava_Thompson_Resume.pdf, Liam_Scott_Resume.pdf, Sophia_Moore_Resume.pdf")
