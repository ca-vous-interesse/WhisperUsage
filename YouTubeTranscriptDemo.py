import os
import subprocess
import re
import json
from datetime import timedelta
import whisper

#https://github.com/openai/whisper/blob/main/README.md

# Load a video from url and convert to audio, return audio file name
def GetYoutubeAudio(url):
    # get video title
    print("Checking url "+url)
    t = subprocess.check_output(['yt-dlp', '-J', url]).decode('utf-8')
    j = json.loads(t)
    title = j['title']
    # get audio file
    audiofile = title+".mp3"
    if not (os.path.exists(audiofile)):
        print("Getting audio from Youtube: "+audiofile)
        os.system('yt-dlp --extract-audio --audio-format mp3 -o "'+audiofile+'" '+url)
    else:
        print("Audio file " + audiofile + " already exists, using it...")
    return audiofile

# Load a video file and convert to audio, return audio file name
def ConvertVideoToAudio(video_file, output_ext="mp3"):
    """Converts video to audio directly using `ffmpeg` command
    with the help of subprocess module"""
    filename, ext = os.path.splitext(video_file)
    filename = filename + "." + output_ext
    subprocess.call(["ffmpeg", "-y", "-i", video_file, f"{filename}"], 
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.STDOUT)
    return filename

# Load the modele desired and return it for recognition processing
# 0=tiny=~1GB/32X, 1=base=~1GB/16X, 2=small=~2GB/6X, 3=medium=~5GB/2X, 4=large=~10GB/1X
def LoadModel(power=4):
    modelpower={0:"tiny", 1:"base", 2:"small", 3:"medium", 4:"large"}
    modelspeed={0:"32x",  1:"16x",  2:"6x",    3:"2x",     4:"1x"}
    modelsize ={0:"~1GB", 1:"~1GB", 2:"~2GB",  3:"~5GB",   4:"~10GB"}
    if power>4 or power<0:
        print("Model's power shall be between 1..4!")
        for i in range(0,5): print(str(i)+": "+modelpower[i]+", speed: "+modelspeed[i]+", size: "+modelsize[i])
        quit()
    modelname = modelpower[power]
    print("Loading model '"+modelname+"', speed: "+modelspeed[power]+", size: "+modelsize[power]+ "...")
    print("This may download (for the first run only) the model data from the OpenAI repository)")
    model = whisper.load_model(modelname)
    return model

# Recognize from audio/video/url to text file, 
# model could be a preloaded model or a number 0..4, 4 is bigger but more powerful
# silence_duration is the minimal duration of silence between paragraphs
#                  if too short this could lead to separation every words, too large will consider only one paragraph
#                  Typically from 0.4 to 5
# Provide either url or audio file or video file
def RecognizeToText(model=None, silence_duration=0.15, url=None, videofile=None, audiofile=None):
    modelno = model
    if videofile==None and audiofile==None and url==None:
        print("Precise either video, audio file, or URL...")
        quit()
    if audiofile==None:
        if videofile==None:
            audiofile = GetYoutubeAudio(url)
        else:
            audiofile = ConvertVideoToAudio(videofile)
    if model==None:
        model = LoadModel()
    elif isinstance(model, int):
        model = LoadModel(model)
    print("Beginning transcribe to text file...")
    result = model.transcribe(audiofile, fp16=False, verbose=True)
    text=""
    last_end_time = 0
    for i, seg in enumerate(result['segments']):
        partial_str = seg['text']
        start_time = seg['start']
        if last_end_time == 0: last_end_time = start_time
        diff = (start_time-last_end_time)
        if diff>=silence_duration: 
            partial_str = partial_str + '\n'
        else:
            partial_str = partial_str + " "
        last_end_time = seg['end']
        text=text+partial_str
    text = re.sub('[ \t]+', ' ', text)
    text = re.sub('\n[ ]+', '\n', text)
    with open(audiofile.replace(".mp3", ".txt"), "w") as textfile:
        textfile.write(text)
    print("Text saved in "+audiofile)
    return audiofile, text

# Recognize from audio/video/url to SRT subtitle text file, 
# model could be a preloaded model or a number 0..4, 4 is bigger but more powerful
def RecognizeToSRT(model=None, url=None, videofile=None, audiofile=None):
    if videofile==None and audiofile==None and url==None:
        print("Precise either video, audio file, or URL...")
        quit()
    if audiofile==None:
        if videofile==None:
            audiofile = GetYoutubeAudio(url)
        else:
            audiofile = ConvertVideoToAudio(videofile)
    if model==None:
        model = LoadModel()
    elif isinstance(model, int):
        model = LoadModel(model)
    print("Beginning transcribe to subtitle SRT...")
    result = model.transcribe(audiofile, fp16=False, verbose=True)
    text=""
    last = 0
    srtFilename = audiofile.replace(".mp3", ".srt")
    with open(srtFilename, 'w', encoding='utf-8') as srtFile:
        for i, segment in enumerate(result['segments']):
            startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
            endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
            text = segment['text']
            if text[0]==' ': text = text[1:]
            segmentId = segment['id']+1
            segment = f"{segmentId}\n{startTime} --> {endTime}\n{text}\n\n"
            srtFile.write(segment)
    print("Text saved in "+srtFilename)
    return srtFilename, text

# La partie que vous pouvez modifier
# Choix de l'URL
video_url = "https://youtu.be/WoPkwOcK9Qc"
# Choix de la génération de SRT ou de texte (ici SRT en commentaire)
#file, text = RecognizeToSRT(url=video_url)
file, text = RecognizeToText(model=3, silence_duration=0.1, url=video_url)
    
