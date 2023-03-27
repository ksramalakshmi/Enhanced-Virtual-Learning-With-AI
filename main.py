import streamlit as st
from dub_transcript import dub

st.set_page_config(
        page_title="Vernacular Video",
        page_icon=":books:",
    )

def main():
    
    st.title("Course Video")

    tab1, tab2 = st.tabs(["Watch Full Video", "Topic Based Learning"])
    add_selectbox = st.sidebar.selectbox(
    "Choose your language",
    ("English", "Hindi", "Tamil")
    )

    with tab1:
        st.header("Video")
        if add_selectbox == "English":
            st.video('/content/mydrive/MyDrive/Krypthon-codes/video.mp4')
            with open('/content/audio.txt') as f:
                text = f.read()
            st.write(text)
            
        elif add_selectbox == "Hindi":
            dub('/content/mydrive/MyDrive/Krypthon-codes/video.mp4', 'hi')
            st.video('/content/mydrive/MyDrive/Krypthon-codes/final.mp4')
            with open('/content/mydrive/MyDrive/Krypthon-codes/translated.txt') as f:
                text = f.read()
            st.write(text)
            
        elif add_selectbox == "Tamil":
            dub('/content/mydrive/MyDrive/Krypthon-codes/video.mp4', 'ta')
            st.video('/content/mydrive/MyDrive/Krypthon-codes/final.mp4')
            with open('/content/mydrive/MyDrive/Krypthon-codes/translated.txt') as f:
                text = f.read()
            st.write(text)

            

    with tab2:
        st.header("Choose Topic")


main()

# dub('/content/mydrive/MyDrive/Krypthon-codes/video.mp4', 'ta')