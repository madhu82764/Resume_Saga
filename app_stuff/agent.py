import google.generativeai as genai
import os
import PyPDF2 as pdf
import json
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL = "gemini-1.5-flash"


def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text


def hr_evaluate_resume(pdf_content: dict, job_description: str) -> str:
    prompt = """
    You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
    Please share your professional evaluation on whether the candidate's profile aligns with the role. 
    Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements."""
    model = genai.GenerativeModel(MODEL)
    resp = model.generate_content([prompt, pdf_content, job_description])
    return resp.text.strip()

def ats_score_resume(pdf_content: dict, job_description: str) -> str:
    prompt = """
    You are an ATS system.
    Compare the resume with the job description.
    Output a match percentage, missing keywords, and improvement tips.
    """
    model = genai.GenerativeModel(MODEL)
    resp = model.generate_content([prompt, pdf_content, job_description])
    return resp.text.strip()

hr_tool = FunctionTool(
    func=hr_evaluate_resume
)

ats_tool = FunctionTool(
    func=ats_score_resume
)

# Create the ADK Agent
resume_agent = LlmAgent(
    name="resume_agent",
    description="Agent that evaluates your resume and finds out areas of improvements",
    model=MODEL,
    tools=[hr_evaluate_resume, ats_score_resume])