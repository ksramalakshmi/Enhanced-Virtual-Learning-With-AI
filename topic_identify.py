from moviepy.editor import VideoFileClip
from time import sleep
import speech_recognition as sr
from pydub import AudioSegment
import os
import glob
from pathlib import Path
import numpy as np 
import pandas as pd
import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from rake_nltk import Rake

def get_topics(videoFile):
    # full_video = "/content/drive/MyDrive/video.mp4"
    full_video = videoFile
    
    current_duration = VideoFileClip(full_video).duration
    divide_into_count = 3
    count=0
    single_duration = current_duration/divide_into_count
    current_video = f"{str(count)}.mp4"
    while current_duration > single_duration:
        clip = VideoFileClip(full_video).subclip(current_duration-single_duration, current_duration)
        current_duration -= single_duration
        current_video = f"{str(count)}.mp4"
        clip.to_videofile(current_video, codec="libx264", temp_audiofile='temp-audio.m4a', remove_temp=True, audio_codec='aac')
        count=count+1

    directory = '/content/'
    pathlist = Path(directory).glob('*.mp4')
    count=0
    for path in pathlist:
      video = AudioSegment.from_file(path, format="mp4")
      audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(4)
      audio.export("audio"+str(count)+".wav", format="wav")
      count=count+1
    
    for i in range(3):
        os.system("whisper {} --model medium.en".format("audio"+ str(i)+".wav"))
        os.system("cp {} {}".format("/content/"+ str(i)+".mp4", "/content/mydrive/MyDrive/Krypthon-codes/output_videos/"+str(i)+".mp4"))
        
    d={}
    directory = '/content/'
    pathlist = Path(directory).glob('*.txt')
    count=0
    for path in pathlist:
        with open(path,"r") as f:
            text = f.read()
            d[count]=text
            count=count+1
    
    STOPWORDS = set(stopwords.words('english'))
    r=Rake()
    
    topics=[]
    for i in d.keys():
        r.extract_keywords_from_text(d[i])
        phrase_df = pd.DataFrame(r.get_ranked_phrases_with_scores(), columns = ['score','phrase'])
        a=phrase_df.loc[phrase_df.score>3]
        for j in range(len(a)):
            if(len(a['phrase'][j].split())>2):
                continue
            else : 
                topics.append(a['phrase'][j])
                break
    
    d_topics = {}
    for i in range(3):
        d_topics[i] = topics[i]
    
    return d_topics