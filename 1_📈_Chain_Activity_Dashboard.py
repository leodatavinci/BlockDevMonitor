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
import streamlit.components.v1 as components



 
def main():
 
    #==========Create Page===========
    
    st.set_page_config(
        page_title="Open Crypto",
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

    st.title("The Open Crypto Dashboard")

    st.header("An Open Source Project for unbiased Crypto Data Insights")

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
    
    st.plotly_chart(bar_chart_total_and_active_repositories("Sum of total and active repositories per protocol"),use_container_width=True)

    st.info('Total of repositories that had at least one commmit in the last three months per chain.', icon="ℹ️")
        
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

    st.info('Sum of new developers who start to build on a chain for the first time per month.', icon="ℹ️")
    
    #=======================================
    
    st.plotly_chart(bar_chart_stackoverflow_questions("Total number of questions raised on Stackoverflow per protocol"),use_container_width=True)

    st.info('Total of technical questions raised on Stackoverflow per chain. Stackoverflow is an important forum for devs to support each other to find solutions for coding problems.', icon="ℹ️")

    #=======================================
   
    st.write("Number of active users per chain")
    
    components.html(
    """<iframe
    src="https://www.footprint.network/public/chart/open-crypto.io-users-per-chain-fp-1be75a9e-943c-4cad-ab95-6eaa9ffc19d7"
    frameborder="0"
    width="800"
    height="600"
    allowtransparency
    ></iframe>"""
    )
    
    st.info('Total of users that where active within the recent month per chain.', icon="ℹ️")
    
    #=======================================
    
    st.info('Map of the latest projects of the most successful developers on github.', icon="🏗️")
    
    st.info('Statistic on support and skepticism for crypto amongst US and EU politicians.', icon="🏗️")
    
    st.info('Statistic on crypto project endorsements by the 100 most influential figures in the crypto space.', icon="🏗️")
    


if __name__ == "__main__":
    main()



            
                

            
            
            