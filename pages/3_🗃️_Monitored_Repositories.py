import pandas as pd
import pymongo
from pandas import DataFrame
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from charts import *



 #==========Get Data=============
 
mongo_client = pymongo.MongoClient("mongodb+srv://admin_nftanalytics:aMMctxcjh580awu8@cluster0.rf3jd.mongodb.net/?retryWrites=true&w=majority")

db = mongo_client["Crypto01"]

df_repositories = pd.DataFrame(db.repositories.find())

df_all_chain = pd.DataFrame(db.chains.find())

all_chains = list(set(df_all_chain['coin']))


 #==========Create Page=============
 
st.set_page_config(
    page_title="Blockchain Developer Activity Tracker",
    page_icon="🗂️",
    layout="wide",
)

st.title("Monitored GitHub Repositories")

st.header("Total Repositories: " + str(len(df_repositories.index)))

st.info('Data Mining Methodology: The objective is to provide insights to developer activities on different blockchain protocols. GitHub repositories are herefore screened and assigned to a protocol by a key word algorithm applied to the repository name and description. The key word rules to conclude on what protocol a project is building on, are configured to keep the number of false positive repositories as low as possible.', icon="ℹ️")

all_chains.append("All")

options = st.multiselect('Select chain',all_chains, ["Ethereum"])

df_repositories = df_repositories[df_repositories['classification'].isin(options)]

fig = go.Figure(data=[go.Table(header=dict(values=['Chain', 'Repository URL']),
                 cells=dict(values=[df_repositories['classification'], df_repositories['url']]))
                     ])
fig.update_layout(width=1000, height=30000)

st.plotly_chart(fig)