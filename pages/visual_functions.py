import pandas as pd 
import streamlit as st 
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_pandas_dataframe_agent
from langchain.agents.agent_types import AgentType
import plotly
import matplotlib
import matplotlib.pyplot as plt
import sklearn
from sklearn.linear_model import LinearRegression
import bokeh
import altair
import re #re stands for regular expression

# PAGE FOR MAKING DATA VISUALIZATION WITHOUT WRITING CODE


# User Uploads a CSV File in the other page
# For new functions we must run this function again to obtain a usable dataframe 
def load_csv(input_csv):
    df = pd.read_csv(input_csv)
    
    

    # Now we need to have the user be able to preview the dataframe 
    with st.expander("See the Dataframe"):
        st.write(df)
        
    df2 = df
    
    return df2






# Generate LLM Responses 
def generate_response(csv_file, input_query, ai_key): #input_question, question_list):
    llm = ChatOpenAI(model_name='gpt-3.5-turbo-0613', temperature=0.2, openai_api_key= ai_key)
    
    df = csv_file
    
    # Create Pandas Dataframe Agent 
    agent = create_pandas_dataframe_agent(llm, df, verbose= True, agent_type = AgentType.OPENAI_FUNCTIONS)
    
    # Perform Queries with the agent 
    response = agent.run(input_query)
    
    return st.success(response)
    
 
    




# Other Inputs 
def other_inputs(list_of_questions, input_file_csv):
    """Add an additional question etc."""
    question_list = list_of_questions
    input_file = input_file_csv
    
    #Select the question.
    #query_text = st.selectbox("Select an example query:", question_list, disabled= not input_file)
    query_text = st.selectbox("Select an example query:", question_list, disabled= input_file.empty)
    
    # openai_api_key = st.text_input("OpenAI API Key", type = "password", disabled = not (input_file and query_text))
    openai_api_key = st.text_input("OpenAI API Key", type = "password", disabled = not (query_text) and input_file.empty)
    
    # Dealing with other questions and verifying API key
    if query_text is "Other":
        # query_text = st.text_input("Enter your query", placeholder= "Enter your query...", disabled = not input_file)
        st.warning("Must include in prompt that you want the PLOTLY CODE IN PYTHON. Omitting this information will cause an error when you paste and run the code GPT gives you!", icon = "🚨")
        st.info("Enter in your custom question below. Leaving the line blank will result in the LLM interpreting your dataset's columns." ,icon = "ℹ")
        query_text_custom = st.text_area("Enter your query", placeholder= "Enter your query...", disabled = input_file.empty)
        # st.header("Output")
        
        # We want to comment the below line out in order to have the functionality called when it is ready.
        #return generate_response(input_file, query_text_custom, openai_api_key)
        
        # We need to make the query_text and the custom text the same
        
        query_text = query_text_custom
        
    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter your OpenAI API key to enable functionality!", icon = "⚠")
    if openai_api_key.startswith("sk-") and (input_file is not None):
        st.header("Output")
        # st.warning("If your output is showing an unexpected visualization. Press the three dots in the upper right hand corner and rerun the page. Once the page is refreshed then you can click the last two buttons. The write code and Make Plot Visualizations.")
        return generate_response(input_file, query_text, openai_api_key)




