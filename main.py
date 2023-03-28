import streamlit as st
from dub_transcript import dub
import fitz 
from pdfintepret import pdfintepret

st.set_page_config(
        page_title="Vernacular Video",
        page_icon=":books:",
    )

def main():
    
    st.title("Course Video")

    tab1, tab2, tab3 = st.tabs(["Watch Full Video", "Topic Based Learning", "Textbook Intepreter"])
    add_selectbox = st.sidebar.selectbox(
    "Choose your language",
    ("English", "Hindi", "Tamil")
    )

    with tab1:
        st.header("Video")
        if add_selectbox == "English":
            st.video('/content/mydrive/MyDrive/Krypthon-codes/video.mp4')
            with open('/content/mydrive/MyDrive/Krypthon-codes/audio.txt') as f:
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
        
    with tab3:
        st.header("Textbook Intepreter")

        uploaded_file = st.file_uploader("Choose a PDF file")
                
        if uploaded_file is not None:
            doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
            content = ""
            for page in doc:
                content += page.get_text()
        
            if add_selectbox == "Hindi":
                content = pdfintepret(content, 'hindi')
                st.write(content)
                
            elif add_selectbox == "Tamil":
                content = pdfintepret(content, 'tamil')
                st.write(content)
                
            else:
                st.write(content)

main()