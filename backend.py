################################ Importing modules ################################
from langgraph.graph import StateGraph, START, END
from langchain_huggingface import HuggingFaceEndpoint
from langchain_groq import ChatGroq
from openai import OpenAI
from typing import TypedDict, Dict, Any
from dotenv import load_dotenv
load_dotenv()   
import os
import pandas as pd


################################ Importing data ################################
def importing_data(data):
    df = pd.read_csv(data, encoding="latin1")
    df_json_first = df.head(1).to_json(orient="records", indent=2)
    df_json = df.to_json(orient="records", indent=2)

    return df,df_json_first,df_json


################################ Importing Models ################################
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"), 
    model="openai/gpt-oss-120b"
)

################################ Importing data ################################

#### Defining a state
class DashboardState(TypedDict):
    json_data : str
    chart_options: str
    dahsbaord_code: str

####
def chart_type(state: DashboardState) -> DashboardState:
    sample_json = state['json_data']

    prompt = f"""
    You are helping design a KPI dashboard. Here is a 1-row sample of the dataset in JSON:
    {sample_json}

    Return FIVE key visualization ideas (with the fields to use) and overall dashboard Filters.
    STRICTLY return valid JSON in this exact shape (no code fences, no commentary):

    [
    {{"metric":"Metric Name","reason":"Why use it","fields":["field1","field2"]}},
    ... 4 more objects ...,
    {{"Filters":["field1","field2","field3"]}}
    ]
"""

    # response = llm_model(open_model,prompt)
    response = llm.invoke(prompt).content

    state['chart_options'] = response
    return state

####
def dahsboard_type(state: DashboardState) -> DashboardState:
    chart_options = state['chart_options']

    prompt = f"""
    Create an interactive HTML + JavaScript dashboard (single HTML file) with FIVE charts based on:

    Key metrics + Filters (JSON):
    {chart_options}

    Requirements:
    - Use the latest Plotly.js via CDN.
    - Add a Filters panel that filters all charts.
        - All the filters should be horizontally aligned, with dropdown bars other than date filter.
        - Also add a reset button at the right of the panel which resets the filter to original way.
    - Keep layout responsive with a simple grid (2 columns on wide screens).
    - Write clean, modern vanilla JS (no frameworks).
    - GIVE ME THE CODE ONLY. NO EXPLANATION. NO MARKDOWN FENCES.
"""
    
    # response = llm_model(open_model,prompt)
    response = llm.invoke(prompt)

    state['dahsbaord_code'] = response
    return state


####
graph = StateGraph(DashboardState)

graph.add_node('chart_type', chart_type)
graph.add_node('dahsboard_type', dahsboard_type)

graph.add_edge(START, 'chart_type')
graph.add_edge('chart_type', 'dahsboard_type') 
graph.add_edge('dahsboard_type', END)

workflow = graph.compile()