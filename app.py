import os
import pandas as pd
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# Lets get the api key from the environment
gemini_api_key = os.getenv('google-api-key-2')

# Lets configure the model
model = ChatGoogleGenerativeAI(
    model='gemini-2.5-flash-lite',
    api_key= gemini_api_key
)

#Design the UI of the application
st.title (":orange[WellNurture:] Your Personal Health Assistant 🥗🏋🏽‍♀️")
st.markdown('''
Get personalized health advice with this application. 
Ask your health-related questions and receive guidance tailored specifically for you.
''')

st.write('''
Follow these steps:
* Enter your details in the sidebar.
* Rate your activity and fitness on the scale of 0-5.
* Submit your details.
* Ask your questions on the main page
* Click generate and relax.''')

#Design the sidebar for all the parameters
st.sidebar.header(':red[ENTER YOUR DETAILS]')
name= st.sidebar.text_input('Enter your Name')
gender= st.sidebar.selectbox('Select your Gender', ['Male', 'Female', 'Other'])
age= st.sidebar.text_input('Enter your Age')
weight= st.sidebar.text_input('Enter your Weight (kgs)')
height= st.sidebar.text_input('Enter your Height (cms)')
bmi= round(pd.to_numeric(weight)/ ((pd.to_numeric(height)/100)**2),2)
active= st.sidebar.slider('Rate your activity (0-5)',0,5,step=1)
fitness= st.sidebar.slider('Rate your fitness (0-5)',0,5,step=1)
if st.sidebar.button('Submit'):
    st.sidebar.write(f"{name}, your BMI is: {bmi} kgs/m2")

#Lets use the gemini model to generate the report
user_input= st.text_input('Ask me your question:')
prompt= f'''
<Role> You are an expert in health and wellness and have 10+ years of experience in guiding people.
<Goal> Generate the customized report addressing the problem the user has asked. Here is the question the user has asked: {user_input}.
<context> Here are the details the user has provided.
name={name}
gender= {gender}
age= {age}
height= {height}
weight= {weight}
bmi={bmi}
activity rating (0-5)= {active}
fitness rating (0-5)= {fitness}

<Format> Following should be the outline of the report in the sequence provided below.
* Start with the 2-3 lines of comment on the details that user has provided.
* Explain what the real pproblem could be on the basis of input the user has provided.
* Suggest the possible reasons for the problem.
* What are the possible solutions?
* Mention the doctor from which specialization can be visited if required.
* In last create a final summary of all the things that have been discussed in the report.

<Instructions> 
* use bullet points wherever possible.
* create tables to represent data wherever possible.
* Strictly avoid prescribing any medicine.
'''

if st.button('Generate'):
    response= model.invoke(prompt)
    st.write(response.content)