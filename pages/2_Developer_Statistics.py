from charts import *
import os
from PIL import Image

 
st.set_page_config(
    page_title="Monitored Developers",
    page_icon="👨‍🔧",
    layout="wide",
)

 
mongo_client = pymongo.MongoClient("mongodb+srv://admin_nftanalytics:aMMctxcjh580awu8@cluster0.rf3jd.mongodb.net/?retryWrites=true&w=majority")
db = mongo_client["Crypto01"]
df_developer = pd.DataFrame(db.developer.find())
df_developer['followers'] = pd.to_numeric(df_developer['followers'])
df_developer = df_developer.sort_values(by=['followers'], ascending=False)

 #==========Create Page=============


st.title("Developer Insights")

st.info('Developer Statistics coming soon...', icon="ℹ️")

st.header("Total Developers: " + str(len(df_developer.index)))

fig = go.Figure(data=[go.Table(header=dict(values=['Name', 'followers', 'total commits']),
                 cells=dict(values=[df_developer['name'], df_developer['followers'], df_developer['total_commits']]))
                     ])
fig.update_layout(width=1000, height=30000)

st.plotly_chart(fig)
