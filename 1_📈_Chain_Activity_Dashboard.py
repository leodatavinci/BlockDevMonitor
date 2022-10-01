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


#=============================

mongo_client = pymongo.MongoClient(st.secrets["connection_string"])
db = mongo_client["Crypto01"]

df_chains = pd.DataFrame(db.chains.find())
all_chains = list(set(df_chains['coin']))
    
#=============================

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
        
    fig = draw_chart(df, options, start_date, end_date, "Commits all Developers per Chain", 'date', 'commits')
    
    return fig

#def multiline_chart_commits_senior_devs(option_agg, start_date, end_date, options):
    
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

#def multiline_chart_new_senior_devs_per_chain(start_date, end_date, options):
           
    df_new_senior_developers_per_chain_per_mo = DataFrame(db.new_senior_developers_per_chain_per_mo.find())
    df_new_senior_developers_per_chain_per_mo['first_date']= pd.to_datetime(df_new_senior_developers_per_chain_per_mo['first_date'])  
    
    df = df_new_senior_developers_per_chain_per_mo 
        
    fig = draw_chart(df, options, start_date, end_date, "New Senior Developers per Chain per Month", 'first_date', 'new_developers')
    
    return fig


 #===============================
 
def main():
 
    #==========Create Page===========
    
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

    st.header("Following the developers to get insights into blockchain demand and building activities.")

    #=======================================

    with st.container():
        
        col1, col2 = st.columns(2)

        with col1:
            
            st.plotly_chart(pie_chart_all_repositories(), use_container_width=True)
            st.subheader(" ")
            
        with col2:
            
            df_totals = pd.DataFrame(db.totals.find())
            
            total_repositories = str(df_totals.iloc[0]['Total Repositories'])
            total_developers = str(df_totals.iloc[0]['Total Developers'])
            
            st.subheader(" ")
            st.subheader(" ")
            st.subheader(" ")
            st.subheader(" ")
            st.subheader(" ")
            st.subheader(" ")
            st.subheader(" ")
        
            st.subheader("Total # of Repositories monitored: " + total_repositories)
            st.subheader("Total # of Developers monitored: " + total_developers)
                    
                        
    with st.container():
        
        options_new_repositories_per_chain = st.multiselect('Select Blockchains:  ', all_chains, ['Ethereum', 'Binance', 'Cardano', 'Solana', 'Polygon'])

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

        st.plotly_chart(multiline_new_repositories_per_chain(end_date, start_date, options_new_repositories_per_chain), use_container_width=True)

    st.info('Sum of repositories created per chain per month.', icon="ℹ️")

    #=======================================

    #with st.container():

        #options_commits_sen_devs = st.multiselect('Select Blockchains: ', all_chains, ['Ethereum', 'Binance', 'Cardano', 'Solana', 'Polygon'])

        #col1, col2, col3, col4 = st.columns(4)

        #with col1:
            
            #start_date = datetime.today() - timedelta(days=draw_option_timespan(' '))
            #end_date = datetime.today()      

        #with col2:

            #option_agg = st.selectbox(
            #'Count of Commits per: ',
            #( 'Week', 'Month'),
            #1
            #)
            
        #with col3:
            #st.write("")
            
        #with col4:
            #st.write("")

        #st.plotly_chart(multiline_chart_commits_senior_devs(option_agg, end_date, start_date, options_commits_sen_devs), use_container_width=True)
        
        #st.info('Sum of the commits per chain during a defined time interval from senior developers. As seniors are qualified those who have made their first commit more than 3 years ago.', icon="ℹ️")

    #=======================================
    
    options_commits_all_devs = st.multiselect('Select Blockchains:', all_chains, ['Ethereum', 'Binance', 'Cardano', 'Solana', 'Polygon'])

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

    st.info('Sum of the commits per chain during a defined time interval', icon="ℹ️")

    #=======================================

    options_new_devs_per_chain = st.multiselect('Select Blockchains:   ', all_chains, ['Bitcoin', 'Ethereum', 'Binance', 'Cardano', 'Solana', 'Polygon'])

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

    st.plotly_chart(multiline_chart_new_devs_per_chain(end_date, start_date, options_new_devs_per_chain), use_container_width=True)

    st.info('Sum of new developers who start to develope on a chain for the first time per month.', icon="ℹ️")

    st.write("")
    st.write("")
    st.write("")

    st.info('More charts coming...', icon="👍")


if __name__ == "__main__":
    main()



            
                

            
            
            