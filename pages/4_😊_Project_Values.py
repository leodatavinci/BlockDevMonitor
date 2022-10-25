import streamlit as st
import os
from PIL import Image

 
st.set_page_config(
    page_title="About",
    page_icon="🙂",
    layout="wide",
)

st.title("Let's do an Open Source Project")

st.write("I'm Leo and a Blockchain Enthusiast and created this tracker to have a dashboard to provide an indication for the developer activities on blockchains and to get an understanding which ecosystems are growing the fastests and what the developers are counting on. This is a provisional version and there is lots of room for improvement.")

st.subheader("Increasing demand for blockchain data insights!")

st.write("As the number of implementation is growing there are various new opportunities to provide usefull data insights into blockchain activities. For now this are only some charts of OffChain GitHub data but the music beginns when combining with OnChain information. If you are interested in this topic as well please DM me to have a chat and we can share our visions and perhaps can build together and make this an open source project.")

st.write("leodatavinci@gmail.com")

st.write("Cheers, Leo")

dir_path = os.path.dirname(os.path.realpath(__file__))

image = Image.open(dir_path + "/profile_pic.png")

st.image(image, caption='Leo Data Vinci')

