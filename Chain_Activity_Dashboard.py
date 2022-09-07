import pandas as pd
import pymongo
from pandas import DataFrame
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from datetime import timedelta
from charts import *


#===========Golval Variables============



#===========Functions============

def draw_option_timespan(invisible_index):

        option_timespan = st.selectbox(
        'Time span' + str(invisible_index),
        ('1 Month', '6 Months', '1 Year', 'All'), 1
        )
        
        if option_timespan == '1 Month':
            days = 1 * 31
        elif option_timespan == '6 Months':
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
        
    fig = draw_chart(df, options, start_date, end_date, "Commits all Developers per Chain", 'date', 'commits')
    
    return fig


def multiline_chart_commits_senior_devs(option_agg, start_date, end_date, options):
    
    """
    if option_agg == 'Day':
        col = 'commits_per_chain_sen_dev_1d'
    """
        
    if option_agg == 'Week':
        col = 'commits_per_chain_sen_dev_1w'

        
    elif option_agg == 'Month':
        col = 'commits_per_chain_sen_dev_1m'
            
    df_commits_per_chain = DataFrame(db[col].find())
    df_commits_per_chain['date']= pd.to_datetime(df_commits_per_chain['date'])  
    
    df = df_commits_per_chain
        
    fig = draw_chart(df, options, start_date, end_date, "Commits Senior Developers per Chain", 'date','commits')
    
    return fig

def multiline_new_repositories_per_chain(start_date, end_date, options):
           
    df_new_repositories_per_mo = DataFrame(db.new_repositories_per_mo.find())
    df_new_repositories_per_mo['date']= pd.to_datetime(df_new_repositories_per_mo['date'])  
    
    df = df_new_repositories_per_mo
        
    fig = draw_chart(df, options, start_date, end_date, "New Repositories per Chain per Month", 'date','total_repositories')
    
    return fig

def multiline_chart_new_devs_per_chain(start_date, end_date, options):
           
    df_new_developers_per_chain_per_mo = DataFrame(db.new_developers_per_chain_per_mo.find())
    df_new_developers_per_chain_per_mo['first_date']= pd.to_datetime(df_new_developers_per_chain_per_mo['first_date'])  
    
    df = df_new_developers_per_chain_per_mo 
        
    fig = draw_chart(df, options, start_date, end_date, "New Developers per Chain per Month", 'first_date', 'new_developers')
    
    return fig

def multiline_chart_new_senior_devs_per_chain(start_date, end_date, options):
           
    df_new_senior_developers_per_chain_per_mo = DataFrame(db.new_senior_developers_per_chain_per_mo.find())
    df_new_senior_developers_per_chain_per_mo['first_date']= pd.to_datetime(df_new_senior_developers_per_chain_per_mo['first_date'])  
    
    df = df_new_senior_developers_per_chain_per_mo 
        
    fig = draw_chart(df, options, start_date, end_date, "New Senior Developers per Chain per Month", 'first_date', 'new_developers')
    
    return fig



 #==========Get Data=============
 
mongo_client = pymongo.MongoClient(st.secrets["connection_string"])
db = mongo_client["Crypto01"]

df_chains = pd.DataFrame(db.chains.find())
all_chains = list(set(df_chains['coin']))
 
 #==========Create Page=============
 
 
st.set_page_config(
    page_title="GitHub Repository Monitor",
    page_icon="📈",
    layout="wide",
)


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


st.title("Blockchain Project GitHub Repository Monitor")

st.write("Following the developers to get insights into blockchain demand and building activities.")

#=======================================

with st.container():
    
    options_commits_all_devs = st.multiselect('Select Blockchains:', all_chains, ['Ethereum', 'Binance', 'Cardano', 'Solana', 'Polygon', 'Near Protocol'])
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
   
        start_date = datetime.today() - timedelta(days=draw_option_timespan(''))
        end_date = datetime.today()      

    with col2:
    
        option_agg = st.selectbox(
        'Count of Commits per:',
        ('Week', 'Month'),
        1
        )
        
    with col3:
        st.write("")
        
    with col4:
        st.write("")
        

st.plotly_chart(multiline_chart_commits_all_devs(option_agg, end_date, start_date, options_commits_all_devs), use_container_width=True)

#=======================================

with st.container():

    st.info('Developers with a blockchain experience of more than three years are classified as seniors', icon="ℹ️")

    options_commits_sen_devs = st.multiselect('Select Blockchains: ', all_chains, ['Ethereum', 'Binance', 'Cardano', 'Solana', 'Polygon', 'Near Protocol'])

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        
        start_date = datetime.today() - timedelta(days=draw_option_timespan(' '))
        end_date = datetime.today()      

    with col2:

        option_agg = st.selectbox(
        'Count of Commits per: ',
        ('Day', 'Week', 'Month'),
        1
        )
        
    with col3:
        st.write("")
        
    with col4:
        st.write("")

    st.plotly_chart(multiline_chart_commits_senior_devs(option_agg, end_date, start_date, options_commits_sen_devs), use_container_width=True)

#=======================================

options_new_repositories_per_chain = st.multiselect('Select Blockchains:  ', all_chains, ['Ethereum', 'Binance', 'Cardano', 'Solana', 'Polygon', 'Near Protocol'])

col1, col2, col3, col4 = st.columns(4)

with col1:
    
    start_date = datetime.today() - timedelta(days=draw_option_timespan('  '))
    end_date = datetime.today()      

with col2:
    st.write("")
    
with col3:
    st.write("")
    
with col4:
    st.write("")

st.plotly_chart(multiline_new_repositories_per_chain( end_date, start_date, options_new_repositories_per_chain), use_container_width=True)

#=======================================

options_new_devs_per_chain = st.multiselect('Select Blockchains:   ', all_chains, ['Ethereum', 'Binance', 'Cardano', 'Solana', 'Polygon', 'Near Protocol'])

col1, col2, col3, col4 = st.columns(4)

with col1:

    start_date = datetime.today() - timedelta(days=draw_option_timespan('   '))
    end_date = datetime.today()      

with col2:
    st.write("")
    
with col3:
    st.write("")
    
with col4:
    st.write("")

st.plotly_chart(multiline_chart_new_devs_per_chain(end_date, start_date, options_new_devs_per_chain))

#=======================================

st.info('Developers with a blockchain experience of more than three years are classified as seniors', icon="ℹ️")

options_sen_devs_per_chain = st.multiselect('Select Blockchains:    ', all_chains, ['Ethereum', 'Binance', 'Cardano', 'Solana', 'Polygon', 'Near Protocol'])

col1, col2, col3, col4 = st.columns(4)

with col1:
    

    start_date = datetime.today() - timedelta(days=draw_option_timespan('    '))
    end_date = datetime.today()      

with col2:
    st.write("")
    
with col3:
    st.write("")
    
with col4:
    st.write("")

st.plotly_chart(multiline_chart_new_senior_devs_per_chain(end_date, start_date, options_sen_devs_per_chain), use_container_width=True)



        
            

            
            
            