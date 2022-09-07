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

st.info('The total amount of GitHub Repositories in scope is much higher than the number of repos that are beeing monitored. To ensure the data integrity a rigid algorightm is applied to filter and classify the repositories retrieved from GitHub. The filter configuration is very sensitive to ensure the number of false positive repositores (Repos that are not blockchain related) is kept as low as possible.', icon="ℹ️")

all_chains.append("All")

options = st.multiselect('Select chain',all_chains, ["Ethereum"])

df_repositories = df_repositories[df_repositories['classification'].isin(options)]

fig = go.Figure(data=[go.Table(header=dict(values=['Chain', 'Repository URL']),
                 cells=dict(values=[df_repositories['classification'], df_repositories['url']]))
                     ])
fig.update_layout(width=1000, height=30000)

st.plotly_chart(fig)