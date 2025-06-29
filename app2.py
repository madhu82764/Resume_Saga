import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# def get_gemini_response(input):
#     model=genai.GenerativeModel('gemini-1.5-flash')
#     response=model.generate_content(input)
#     return response.text

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, pdf_content, prompt])
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text




#Prompt Template
input_prompt1 = """
 You are an experienced Technical Human Resource Manager,your task is to review the provided resume against the job description. 
  Please share your professional evaluation on whether the candidate's profile aligns with the role. 
 Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements.
"""

input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""


input_prompt3= """
Given a resume document, thoroughly analyze all its elements including font styles, font sizes, layout structure, colors, spacing, and template design. Then generate comprehensive LaTeX code that replicates the exact same resume appearance and formatting when compiled in Overleaf. Ensure the LaTeX code includes all necessary packages, custom commands, and formatting details to produce a visually identical resume with precise alignment and styling.
"""
input_prompt4 = """
Identify and correct any errors or bugs present in the LaTeX code used for formatting a professional resume. Ensure that the document layout is visually appealing, with clear sections for personal information, work experience, education, skills, and any additional relevant details. Pay attention to proper formatting, such as font styles, sizes, bullet points, alignment, and overall consistency throughout the resume. Make sure that the final output is polished and ready for submission in a job application or professional setting.
"""
# input_prompt="""
# Hey Act Like a skilled or very experience ATS(Application Tracking System)
# with a deep understanding of tech field,software engineering,data science ,data analyst
# and big data engineer. Your task is to evaluate the resume based on the given job description.
# You must consider the job market is very competitive and you should provide 
# best assistance for improving thr resumes. Assign the percentage Matching based 
# on Jd and the missing keywords with high accuracy
# resume:{text}
# description:{jd}

# I want the response in one single string having the structure
# {{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
# """

##Submit button
# if submit:
#     if uploaded_file is not None:
#         text=input_pdf_text(uploaded_file)
#         response=get_gemini_repsonse(input_prompt)
#         st.subheader(response)


## streamlit app
st.set_page_config(page_title= "ATS Resume Expert")
st.title("Resume Saga")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please upload the pdf")

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")


submit1 = st.button("Tell me about the Resume")

submit2 = st.button("How can I improve my skills")

submit3 = st.button("Show the latex code for the resume")

# submit4 = st.button("Help resolve error in Latex Code")

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_text(uploaded_file)
        response1=get_gemini_response(input_prompt1, pdf_content, jd)
        st.subheader("The Response is")
        st.write(response1)
    else:
        st.write("Please upload the resume")
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_text(uploaded_file)
        response2=get_gemini_response(input_prompt2, pdf_content, jd)
        st.subheader("The Response is")
        st.write(response2)
    else:
        st.write("Please upload the resume")
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_text(uploaded_file)
        response3=get_gemini_response(input_prompt3, pdf_content, jd)
        st.subheader("The Response is")
        st.write(response3)
    else:
        st.write("Please upload the resume")
# elif submit4:
#     if get_gemini_response(input_prompt3, pdf_content, jd) is not None:
#         response=get_gemini_response(input_prompt4, get_gemini_response(input_prompt3, pdf_content, jd), jd)
#         st.subheader("The Response is")
#         st.write(response)
#     else:
#         st.write("Please generate the latex code first")

