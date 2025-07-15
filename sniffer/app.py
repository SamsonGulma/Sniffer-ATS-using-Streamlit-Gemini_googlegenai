import base64
from dotenv import load_dotenv
import streamlit as st
import io
import os
from PIL import Image
import pdf2image
import google.generativeai as googleai


load_dotenv()


googleai.configure(api_key=os.getenv('google_api_key'))

def get_gemini_reponse(input, pdf_content, prompt):
    model=googleai.GenerativeModel("gemini-1.5-flash")
    response=model.generate_content([input, pdf_content[0], prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        
        first_page=images[0]

        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format = 'JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type" : "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]

        return pdf_parts
    else: 
        raise FileNotFoundError("No file uploaded")
    

st.set_page_config(page_title="Sniffer")
st.header("Sniffer-- ATS Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=['pdf'])

if uploaded_file is not None:
    st.write('PDF Uploaded Successfully')

submission1 = st.button('Tell Me about the Resume')
# submission2 = st.button('How Can I Improvise My Skills')
submission3 = st.button('Percentage Match')

input_prompt1 = """You are an experienced HR with Tech Experience in the Field
Data Science, Full Stack Web Development, Big Data Engineering, DevOps, Data Analyst,
Your task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on wheter the candidte's profile aligns with the role. 
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements  
"""

# input_prompt2 = """ You are a Technical Human Resource Manager with expertise in 
# Data Science, Full Stack Web Development, Big Data Engineering, DevOps, Data Analyst,
# """


input_prompt3 = """ You are a skilled ATS (Application Tracking System) scanner 
with a deep understanding of Data Science, Full Stack Web Development, Big Data Engineering, 
DevOps, Data Analyst, and deep ATS Functionality, your task is to evaluate the resume against the 
provided job description, Then give me the percentage of match if the resume matches the Job Description. 
First the output should come as percentage and then keywords missing and last final thoughts. and Please I want the
your response be a numbered percentage. Just give me a number, How much does this candidate matches with Job Description ?
"""


if submission1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_reponse (input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a Resume")

elif submission3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_reponse (input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload a Resume")