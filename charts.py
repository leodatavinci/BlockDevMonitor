import pandas as pd
import pymongo
from pandas import DataFrame
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st


mongo_client = pymongo.MongoClient(st.secrets["connection_string"])
global db
db = mongo_client["Crypto01"]

df_chains = pd.DataFrame(db.chains.find())
all_chains = list(set(df_chains['coin']))


def draw_option_timespan(invisible_index):

        option_timespan = st.selectbox(
        'Time span' + str(invisible_index),
        ('6 Months', '1 Year', 'All'), 2
        )

        if option_timespan == '6 Months':
            days = 6 * 31
        elif option_timespan == '1 Year':
            days = 12 * 31
        elif option_timespan == 'All':
            days = 120 * 31
        
        return days


def draw_chart(df, options, start_date, end_date, title, x_axis, y_axis):
        
    fig = go.Figure()
        
    chart_chains = options
    
    for chain in chart_chains: 
    
        df_chain = df.loc[df['chain'] == chain]
        df_chain = df_chain[(df_chain[x_axis] > end_date) & (df_chain[x_axis] <= start_date)]
        
        fig.add_trace(go.Scatter(x=df_chain[x_axis], y=df_chain[y_axis],
                    mode='lines+markers',
                    name=chain)
                    )
        
        fig.update_layout(title=title, autosize=False,
                width=700, height=600,
                margin=dict(l=40, r=40, b=40, t=100))
    
    return fig

def pie_chart_all_repositories():
    
    df_repository_count = pd.DataFrame(db.repository_count.find())
    df_repository_count.loc[df_repository_count['Total Repositories'] < 1500, 'chain'] = 'Other Chains'
    df_repository_count = df_repository_count.reset_index(level=0)
    
    fig = px.pie(df_repository_count, values=df_repository_count['Total Repositories'], names=df_repository_count['chain'], title='Repositories per Chain Monitored')
    fig.update_traces(textinfo='value')
       
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
        
    fig = draw_chart(df, options, start_date, end_date, "Commits all Developers per Protocol", 'date', 'commits')
    
    return fig

def multiline_chart_commits_per_active_devs_per_chain_per_mo(option_agg, start_date, end_date, options):
    
    """
    if option_agg == 'Day':
        col = 'commits_per_chain_sen_dev_1d'
    """
        
    if option_agg == 'Week':
        col = 'commits_per_chain_sen_active_dev_1w'

        
    elif option_agg == 'Month':
        col = 'commits_per_chain_sen_active_dev_1m'
            
    df_commits_per_chain = DataFrame(db[col].find())
    df_commits_per_chain['date']= pd.to_datetime(df_commits_per_chain['date'])  
    
    df = df_commits_per_chain
        
    fig = draw_chart(df, options, start_date, end_date, "Commits Active Developers per Protocol", 'date','commits')
    
    return fig

def multiline_chart_commits_per_sen_active_devs_per_chain_per_mo(option_agg, start_date, end_date, options):
    
    """
    if option_agg == 'Day':
        col = 'commits_per_chain_sen_dev_1d'
    """
        
    if option_agg == 'Week':
        col = 'commits_per_chain_sen_active_dev_1w'

        
    elif option_agg == 'Month':
        col = 'commits_per_chain_sen_active_dev_1m'
            
    df_commits_per_chain = DataFrame(db[col].find())
    df_commits_per_chain['date']= pd.to_datetime(df_commits_per_chain['date'])  
    
    df = df_commits_per_chain
        
    fig = draw_chart(df, options, start_date, end_date, "Commits Senior Active Developers per Protocol", 'date','commits')
    
    return fig

def multiline_new_repositories_per_chain(start_date, end_date, options):
           
    df_new_repositories_per_mo = DataFrame(db.new_repositories_per_mo.find())
    df_new_repositories_per_mo['date']= pd.to_datetime(df_new_repositories_per_mo['date'])  
    
    df = df_new_repositories_per_mo
        
    fig = draw_chart(df, options, start_date, end_date, "New Repositories per Protocol per Month", 'date','total_repositories')
    
    return fig

def multiline_chart_new_devs_per_chain(start_date, end_date, options):
           
    df_new_developers_per_chain_per_mo = DataFrame(db.new_developers_per_chain_per_mo.find())
    df_new_developers_per_chain_per_mo['first_date']= pd.to_datetime(df_new_developers_per_chain_per_mo['first_date'])  
    
    df = df_new_developers_per_chain_per_mo 
        
    fig = draw_chart(df, options, start_date, end_date, "New Developers per Protocol per Month", 'first_date', 'new_developers')
    
    return fig

#def multiline_chart_commits_per_sen_active_devs_per_chain_per_mo(start_date, end_date, options):
           
    df_commits_per_chain_sen_active_dev_1m = DataFrame(db.commits_per_chain_sen_active_dev_1m.find())
    df_commits_per_chain_sen_active_dev_1m['first_date']= pd.to_datetime(df_commits_per_chain_sen_active_dev_1m['first_date'])  
    
    df = df_commits_per_chain_sen_active_dev_1m 
        
    fig = draw_chart(df, options, start_date, end_date, "Commits per active senior developers per Protocol", 'first_date', 'new_developers')
    
    return fig

def bar_chart_stackoverflow_questions(title):
           
    df_stackoverflow_questions = DataFrame(db.stackoverflow_question_sums.find({'question_counter': { '$ne': 0 }}))
    
    df_stackoverflow_questions.rename({'chain': 'Chain', 'question_counter': 'Total questions raised'}, axis=1, inplace=True)
  
    df = df_stackoverflow_questions
    
    fig = px.bar(df, x='Chain', y='Total questions raised')
    
    fig.update_layout(title=title, autosize=False, barmode = 'stack', xaxis = {
   'categoryorder': 'total descending'
    })
    
    return fig

 #===============================

def bar_chart_total_and_active_repositories(title):
           
    df_sum_active_repos_per_protocol = DataFrame(db.sum_active_repos_per_protocol.find())

    #df = df_sum_active_repos_per_protocol.loc[((df_sum_active_repos_per_protocol['total']>200)]
    
    #df_sum_active_repos_per_protocol.rename({'chain': 'Chain', 'question_counter': 'Total questions raised'}, axis=1, inplace=True)
    
    fig = px.bar(df_sum_active_repos_per_protocol, x='chain', y='total_active_repose')
    
    fig.update_layout(title=title, autosize=False, barmode = 'stack', xaxis = {
   'categoryorder': 'total descending'
    })
    
    return fig