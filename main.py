import os

from PIL import Image
import PyPDF2 as pdf
import streamlit as st
import google.generativeai as genai


from langchain.agents import AgentType, initialize_agent, load_tools
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools.google_jobs import GoogleJobsQueryRun
from langchain_community.utilities.google_jobs import GoogleJobsAPIWrapper

from dotenv import load_dotenv 
load_dotenv()



# #  Model for the first task is from langchain to make use of duckduckgo 
# #  search and its multiple advantages. Also this model will be used for the first task


# os.environ["SERPAPI_API_KEY"] = 'AIzaSyAbOolM9L9KwJpzu1SQD5T_nBe2CVOuCpE'

# model = ChatGoogleGenerativeAI(model="gemini-pro", 
#                              temperature=0.7,
#                              google_api_key='AIzaSyAbOolM9L9KwJpzu1SQD5T_nBe2CVOuCpE')


# tool = GoogleJobsQueryRun(api_wrapper=GoogleJobsAPIWrapper())
# tools_1=load_tools(["ddg-search"], llm=model)
# tools_2=load_tools(["ddg-search"], llm=model)


# PREFIX = """Your tasks is to provide a list of opportutnities offered by the company Google. 
# You have access to the following tools:
# duckduckgo_search: A wrapper around DuckDuckGo Search. Useful for when you need to answer 
# questions about current events. Input should be a search query.
# """
# ASPIRATIONS = """{aspirations}"""
# PASSIONS = """{passions} """
# FORMAT_INSTRUCTIONS = """Use the following format:

# Question: the input question you must answer
# Thought: you should always think about what to do
# Action: the action to take, should be one of [{duckduckgo_search}]
# Action Input: the input to the action
# Observation: the result of the action
# ... (this Thought/Action/Action Input/Observation can repeat N times)
# Thought: I now know the final answer
# Final Answer: the final answer to the original input question"""
# SUFFIX = """Begin!

# Question: {input}
# Thought:{agent_scratchpad}"""

# agent=initialize_agent(agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#                        tools=tools_1, 
#                        llm=model, 
#                        agents_kwargs={
#                                       'prefix':PREFIX,
#                                       'aspiration': ASPIRATIONS,
#                                       'passions':PASSIONS,
#                                       'format_instructions':FORMAT_INSTRUCTIONS,
#                                       'suffix':SUFFIX})

# agent_2=initialize_agent(agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#                        tools=tools_2, 
#                        llm=model, 
#                        agents_kwargs={
#                                       'prefix':PREFIX,
#                                       'aspiration': ASPIRATIONS,
#                                       'passions':PASSIONS,
#                                       'format_instructions':FORMAT_INSTRUCTIONS,
#                                       'suffix':SUFFIX})


# # Model for the seconf task is from google generativeai.
# # Also this model will be used for the first task

genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

model_1 = genai.GenerativeModel('gemini-pro')


def get_gemini_response(prompt, aspirations):
    response = model_1.generate_content([prompt, aspirations])
    return response.text



#Prompt List



# def input_pdf_text(uploaded_file):
#     if uploaded_file is not None:
#         reader = pdf.PDdfReader(uploaded_file)
#         text = []
#         for page in reader(len(reader.pages)):
#             page = reader.pages[page]
#             text+= str(page.extract_text())
#         return text
#     else:
#         raise FileNotFoundError("No file uploaded")
    

st.set_page_config(page_title='Career Planning Assistant')
st.header('Career Planning Assistant')
aspirations = st.text_input("What do you aspire to be: ", key="aspiration")
passions = st.text_input("Passions in life", key="passion")
profile = st.text_input("A little about yourself", key="profile")
job_description = st.text_input("Job Description", key="job description")
uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=["pdf"])


if uploaded_file is not None:
    st.write("Uploaded file successfully")

submit1 = st.button("Google products based on aspiration")

submit2 = st.button("Career plan based on Aspirations")

submit3 = st.button("Gemini surprise me with a career")

submit4 = st.button("Compare Resume against Job Description")

submit5 = st.button("Manifestation Techniques")




#List of Prompts

google_ressource_prompt3 = """
You provide tailored Google opportunities to individuals based on their passions or aspirations
such as scholarships, courses, stipends, job opportunities from sites such as google build your 
future or others. Your tasks is to provide a list of opportutnities by the company Google """


career_plan_prompt = """
You are an experienced Career planner. You assist individuals in achieving their dream career
by setting goals and developing a plan to achieve it. 
Your task is guess career for the individual and design the career plan to achieve the dream career. 
Your tone has positive and encouraging """

guess_career_input_prompt = """
You are an expert career planner. You have extensive knowledge on how to navigate the work force
Your task is guess a single career plans for that takes into considerations all the attribute of 
the individuals """


manifestation_prompt = """
You are a mafestation Guru in the style of Abdullah the ethiopian mystic and neville goddard.
Your task is to provide a set of affirmation techniques that can be recited daily to
help restore confidence. """


resume_job_comparism = """
Compare the resume against the job description and find the missing skills and areas that need to be 
improved. Assign a percentage matching and Provide some ressources for improvement based on the aspirations
Resume:{uploaded_life}
Job Description: {job_description}
aspirations:{aspirations}
"""



#Google ressources based on aspirations
if submit1:
    if aspirations is not None:
        response = get_gemini_response(google_ressource_prompt3,aspirations)
        st.subheader("Here is what was found: ")
        st.write(response)
    else:
        st.write("Please put your aspirations")

#Career plan based on Aspiration
elif submit2:
    if aspirations is not None:
        response = get_gemini_response(career_plan_prompt, aspirations)
        st.subheader("Here is your career plan:  ")
        st.write(response)
    # else:
        st.write("Please input aspirations")

#Surpise career plan
elif submit3:
    if uploaded_file is not None:
        response = get_gemini_response(guess_career_input_prompt, profile)
        st.subheader("The response is ")
        st.write(response)
    else:
        st.write("Please upload resume")

#Comparism of Resume against Job Description
elif submit4:
    if passions is not None:
        response = get_gemini_response(resume_job_comparism, aspirations)
        st.subheader("These manifestation can help. Things get better: ")
        st.write(response)
    else:
        st.write("Please input your passions")

#Manifestation techniques
elif submit5:
    if passions is not None:
        response = get_gemini_response(manifestation_prompt, passions)
        st.subheader("These manifestation can help. Things get better: ")
        st.write(response)
    else:
        st.write("Please input passions")



