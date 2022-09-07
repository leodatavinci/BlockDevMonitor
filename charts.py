import pandas as pd
import pymongo
from pandas import DataFrame
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st



      
"""
        
if 'df_developer' not in st.session_state:
        
    def get_df_developer():

        df_developer = pd.DataFrame(st.session_state.db.developer.find())

        df_developer = df_developer.sort_values(by='followers', ascending=False)

        st.session_state.df_developer = df_developer
        
if 'df_all_dev_1d' not in st.session_state:

        df_commits = pd.DataFrame(st.session_state.db.commits_per_chain_1d.find())

        st.session_state.df_commits_per_chain_1d = df_commits
        
if 'df_all_dev_1w' not in st.session_state:

        df_commits = pd.DataFrame(st.session_state.db.commits_per_chain_1w.find())

        st.session_state.df_commits_per_chain_1w = df_commits
        
if 'df_all_dev_1m' not in st.session_state:

        df_commits = pd.DataFrame(st.session_state.db.commits_per_chain_1m.find())

        st.session_state.df_commits_per_chain_1m = df_commits 
        
        
if 'df_repositories' not in st.session_state:
        
    def get_df_repositories():

        df_repositories = pd.DataFrame(st.session_state.db.repositories.find())

        st.session_state.df_repostiories = df_repositories
        
        
if 'df_commits' not in st.session_state:
        
    def get_df_commits():

        df_commits = pd.DataFrame(st.session_state.db.commits.find())

        st.session_state.df_commits = df_commits
    

if 'df_merged_repostiroes_commuts' not in st.session_state:
    
    def query_get_commits_and_dev_data():
        
        st.session_state.df_merged_repostiries_commits = pd.merge(DataFrame(st.session_state.df_repositories), DataFrame(st.session_state.df_commits), left_on=['url'], right_on=['repository'], how='inner')
          


def draw_chart(df, options, start_date, end_date, title):
        
    fig = go.Figure()
        
    chart_chains = options
    
    for chain in chart_chains: 
    
        df_chain = df.loc[df['chain'] == chain]
        df_chain = df_chain[(df_chain['date'] > end_date) & (df_chain['date'] <= start_date)]
        
        fig.add_trace(go.Scatter(x=df_chain['date'], y=df_chain['commits'],
                    mode='lines+markers',
                    name=chain)
                    )
    
    fig.update_layout(title=title, autosize=False,
            width=1200, height=900,
            margin=dict(l=40, r=40, b=40, t=40))
    
    return fig
    
        
        
        
def multiline_chart_commits_all_devs(option_agg, start_date, end_date, options):
    
    if option_agg == 'Day':
        col = 'commits_per_chain_1d'

        
    elif option_agg == 'Week':
        col = 'commits_per_chain_1w'

        
    elif option_agg == 'Month':
        col = 'commits_per_chain_1m'
            
    df_commits_per_chain = DataFrame(db[col].find())
    df_commits_per_chain['date']= pd.to_datetime(df_commits_per_chain['date'])  
    
    df = df_commits_per_chain
        
    fig = draw_chart(df, options, start_date, end_date, "Commits all Developers")
    
    return fig


def multiline_chart_commits_senior_devs(option_agg, start_date, end_date, options):
        
    if option_agg == 'Day':
        col = 'commits_per_chain_sen_dev_1d'

        
    elif option_agg == 'Week':
        col = 'commits_per_chain_sen_dev_1w'

        
    elif option_agg == 'Month':
        col = 'commits_per_chain_sen_dev_1m'
            
    df_commits_per_chain = DataFrame(db[col].find())
    df_commits_per_chain['date']= pd.to_datetime(df_commits_per_chain['date'])  
    
    df = df_commits_per_chain
        
    fig = draw_chart(df, options, start_date, end_date, "Commits Senior Developers")
    
    return fig

"""     