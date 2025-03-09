import streamlit as st
import google.generativeai as genai
import nltk
import spacy
import docx
import re
from io import BytesIO  # Import for in-memory file handling

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Configure Gemini API
genai.configure(api_key="AIzaSyB_EBk48Hy7_9k98WWIOEmforU3MuHrcss")

# Function to extract keywords from job description
def extract_keywords(job_desc):
    doc = nlp(job_desc)
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "PROPN"]]
    return ", ".join(set(keywords))

# Function to generate ATS-optimized resume
def generate_resume(job_desc, user_skills, experience, education):
    keywords = extract_keywords(job_desc)
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    Generate an ATS-optimized resume for a candidate with:
    - Skills: {user_skills}
    - Experience: {experience}
    - Education: {education}
    - Job Description: {job_desc}
    - Use the following keywords to improve ATS score: {keywords}
    """

    response = model.generate_content(prompt)
    return response.text if response.text else "Error generating resume."

# Function to generate cover letter
def generate_cover_letter(job_desc, company_name, user_name):
    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
    Generate a personalized cover letter for {user_name} applying to {company_name}.
    - Job Description: {job_desc}
    - Highlight skills & experience while maintaining a professional tone.
    """

    response = model.generate_content(prompt)
    return response.text if response.text else "Error generating cover letter."

# Function to save document to memory for download
def generate_docx(content):
    doc = docx.Document()
    doc.add_paragraph(content)
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer

# Streamlit UI
st.set_page_config(page_title="AI Resume & Cover Letter Generator", layout="wide")
st.title("📄 AI Resume & Cover Letter Generator (ATS Optimized)")

# Tabs for Resume & Cover Letter
tab1, tab2 = st.tabs(["📜 Generate Resume", "✉️ Generate Cover Letter"])

# Resume Generator
with tab1:
    st.subheader("📜 ATS-Optimized Resume")
    job_desc = st.text_area("Paste the Job Description:", placeholder="Copy & paste job description here...",key="resume generator")
    user_skills = st.text_input("Enter Your Skills (comma-separated):", placeholder="Python, Data Analysis, AI...")
    experience = st.text_area("Describe Your Work Experience:", placeholder="3 years in data science, worked at X company...")
    education = st.text_input("Enter Your Education:", placeholder="B.Tech in Computer Science, XYZ University")
    
    if st.button("Generate Resume"):
        if job_desc and user_skills and experience and education:
            resume_text = generate_resume(job_desc, user_skills, experience, education)
            st.write(resume_text)

            # Generate .docx file and enable download
            resume_docx = generate_docx(resume_text)
            st.download_button(
                label="📥 Download Resume",
                data=resume_docx,
                file_name="Resume.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        else:
            st.warning("Please fill in all fields before generating the resume.")

# Cover Letter Generator
with tab2:
    st.subheader("✉️ Tailored Cover Letter")
    company_name = st.text_input("Enter Company Name:", placeholder="Google, Microsoft, Tesla...")
    user_name = st.text_input("Enter Your Name:", placeholder="John Doe")
    job_desc_cl = st.text_area("Paste the Job Description:", placeholder="Copy & paste job description here...",key="Cover letter generator")

    if st.button("Generate Cover Letter"):
        if company_name and user_name and job_desc_cl:
            cover_letter_text = generate_cover_letter(job_desc_cl, company_name, user_name)
            st.write(cover_letter_text)

            # Generate .docx file and enable download
            cover_letter_docx = generate_docx(cover_letter_text)
            st.download_button(
                label="📥 Download Cover Letter",
                data=cover_letter_docx,
                file_name="CoverLetter.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        else:
            st.warning("Please fill in all fields before generating the cover letter.")

st.markdown("🚀 Developed using Streamlit & Google Gemini AI")
