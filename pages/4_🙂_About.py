from charts import *
import os
from PIL import Image

 
st.set_page_config(
    page_title="About",
    page_icon="🙂",
    layout="wide",
)

st.write("Hi, I'm Leo from Switzerland and a Blockchain Enthusiast and Data Scientist. Created this tracker over the weekend to have a dashboard to provide an indication for the developer activities on the different blockchains and to get an understanding which ecosystems are growing the fastests and what the developers are counting on.")

st.write("More charts will be added to give further insight to blockchain development activities. The objective of the project is to give a makro understanding of the development in general but also to provide a screening of new hot projects that are growing fast, respectively are beeing launched by experienced developers.")

st.write("Best regards, Leo")

image = Image.open(os.getcwd() + "\\pages\\profile_pic.png")

st.image(image, caption='Leo Data Vinci')

