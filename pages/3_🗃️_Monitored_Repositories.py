import pandas as pd
import pymongo
from pandas import DataFrame
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

 #==========Get Data=============
 
mongo_client = pymongo.MongoClient("mongodb+srv://admin_nftanalytics:aMMctxcjh580awu8@cluster0.rf3jd.mongodb.net/?retryWrites=true&w=majority")

db = mongo_client["Crypto01"]

 #==========Create Page=============
 
st.set_page_config(
    page_title="Blockchain Developer Activity Tracker",
    page_icon="🗂️",
    layout="wide",
)

if 'df_repositories' not in st.session_state:
    st.session_state.df_repositories = pd.DataFrame(db.repositories.find())
    
df_repositories = pd.DataFrame(st.session_state.df_repositories)

def make_clickable(val):
    # target _blank to open new window
    return '<a target="_blank" href="{}">{}</a>'.format(val, val)

df_repositories.style.format({'url': make_clickable})
    
if 'all_chains' not in st.session_state:
    df_all_chains = pd.DataFrame(db.chains.find())
    st.session_state.all_chains = list(set(df_all_chains['coin']))
    st.session_state.all_chains.append("All")
    
all_chains = st.session_state.all_chains

    
if 'options_list' not in st.session_state:
    st.session_state.options_list = ["Bitcoin"]
    

st.title("Monitored GitHub Repositories")

st.header("Total Repositories: " + str(len(st.session_state.df_repositories.index)))

st.info('Data Mining Methodology: The objective is to provide insights to developer activities on different blockchain protocols. GitHub repositories are herefore screened and assigned to a protocol by a key word algorithm applied to the repository name and description.', icon="ℹ️")

options = st.multiselect('Select chain', all_chains, ['Ethereum'])

df_repositories_filtered = df_repositories[df_repositories['classification'].isin(options)]

fig = go.Figure(data=[go.Table(columnwidth = [80,400], header=dict(values=['Chain', 'Repository URL']),
                 cells=dict(values=[df_repositories_filtered['classification'], df_repositories_filtered['url']]))
                     ])

fig.update_layout(width=1000, height=30000)

st.plotly_chart(fig)

