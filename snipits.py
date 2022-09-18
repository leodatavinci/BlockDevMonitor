

st.info('Developers with a blockchain experience of more than three years are classified as seniors', icon="ℹ️")

options_sen_devs_per_chain = st.multiselect('Select Blockchains:    ', all_chains, ['Bitcoin', 'Ethereum', 'Binance', 'Cardano', 'Solana', 'Polygon'])

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

