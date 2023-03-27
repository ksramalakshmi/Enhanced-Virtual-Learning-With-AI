import speech_recognition as sr
from pydub import AudioSegment
import os
import sys
from deep_translator import GoogleTranslator
from gtts import gTTS
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
import argparse


def dub(source, lang):
    # video = AudioSegment.from_file("/content/drive/MyDrive/video.mp4", format="mp4")
    video = AudioSegment.from_file(source, format="mp4")
    audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(4)
    audio.export("/content/mydrive/MyDrive/Krypthon-codes/audio.wav", format="wav")
    os.system('whisper "/content/mydrive/MyDrive/Krypthon-codes/audio.wav" --model medium.en')
    # translated = GoogleTranslator(source='english', target='hindi').translate_file('/content/audio.txt')
    if lang == 'ta':
        translated = GoogleTranslator(source='english', target='tamil').translate_file('/content/audio.txt')
    elif lang == 'hi':
        translated = GoogleTranslator(source='english', target='hindi').translate_file('/content/audio.txt')


    with open ('/content/mydrive/MyDrive/Krypthon-codes/translated.txt', 'w') as file:  
        file.write(translated)  

    file = open("/content/mydrive/MyDrive/Krypthon-codes/translated.txt", "r").read().replace("\n", " ")
    # language = 'ta'
    speech = gTTS(text=str(file), lang = lang, slow = False)
    speech.save("/content/mydrive/MyDrive/Krypthon-codes/translated_voice.mp3")

    # load the video
    # video_clip = VideoFileClip("/content/drive/MyDrive/video.mp4")
    video_clip = VideoFileClip(source)

    # load the audio
    audio_clip = AudioFileClip("/content/mydrive/MyDrive/Krypthon-codes/translated_voice.mp3")
    audio_clip = audio_clip.volumex(1)

    end = video_clip.end
    audio_clip = audio_clip.subclip(0, end)
    final_audio = audio_clip
    final_clip = video_clip.set_audio(final_audio)

    final_clip.write_videofile("/content/mydrive/MyDrive/Krypthon-codes/final.mp4")
