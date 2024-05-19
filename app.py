from dotenv import load_dotenv
import streamlit as st
import os
import requests
from io import BytesIO
from PIL import Image
import google.generativeai as genai
# Load the .env variables
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

STABILITY_API_BASE_URL = "https://api.stability.ai/v2beta/stable-image/generate/core"

def generate_image(prompt):
    headers = {
        "authorization": f"Bearer {os.getenv('STABILITY_API_KEY')}",
        "accept": "image/*"
    }
    data = {
        "prompt": prompt,
        "output_format": "webp",
    }
    response = requests.post(
        STABILITY_API_BASE_URL,
        headers=headers,
        files={"none": ''},
        data=data
    )

    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        raise Exception(str(response.json()))

def generate_code(prompt):
    code_prompt = f"Generate a React component, including CSS and JavaScript, for the following design: {prompt}"
    response = chat.send_message(code_prompt, stream=True)
    code = ""
    for chunk in response:
        code += chunk.text
    return code

st.set_page_config(page_title='Design Bot', layout="centered")

st.markdown("""
    <style>
        body {
            background-color: #f0f2f6;
            font-family: 'Arial', sans-serif;
        }
        .main {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 12px 28px;
            text-align: center;
            font-size: 16px;
            margin: 20px 0;
            cursor: pointer;
            border-radius: 12px;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        .stTextInput>div>div>input {
            padding: 12px;
            border-radius: 8px;
            border: 1px solid #ddd;
            font-size: 16px;
            margin-bottom: 20px;
            width: 100%;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #333;
            
        }
        .stMarkdown h1 {
            margin-bottom: 20px;
            margin-top: 20px
        }
        .stMarkdown h2 {
            margin-top: 30px;
            margin-bottom: 10px;
        }
        .stMarkdown h3 {
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .stImage>div {
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

st.header("Design and Code Generating Bot")
st.subheader("Describe the design you want, and generate both the design and the code!!")

input_prompt = st.text_input("What design do you want!!", key="input")

submit = st.button("Generate")

if submit and input_prompt:
    try:
        generated_image = generate_image(input_prompt)
        generated_code = generate_code(input_prompt)
        st.subheader("Generated Design:")
        st.image(generated_image, use_column_width=True)
        st.subheader("Generated Code:")
        st.code(generated_code, language='javascript')
        
    except Exception as e:
        st.write("Failed to generate design and code")
        st.write(str(e))


