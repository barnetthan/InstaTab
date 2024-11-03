from yt_dlp import YoutubeDL
from pydub import AudioSegment
import os
import asyncio
import hashlib
import pdb

async def download_youtube_video(video_url):
    # Download the YouTube video
    # yt = YouTube(video_url)
    # print(f'Downloading: {yt.title}')
    # video_stream = yt.streams.filter(only_audio=True).first()
    # mp4_file = video_stream.download(filename='temp_video.mp4')
    # return mp4_file
    video_hash = hashlib.md5(video_url.encode()).hexdigest()
    mp3_file = os.path.abspath(f'/app/processing/temp_video_{video_hash}.mp3')
    print(mp3_file)
    if os.path.exists(mp3_file):
        print(f'Using cached file: {mp3_file}')
        return mp3_file


    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': mp3_file,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    print("This is where the output is going")
    print(ydl_opts['outtmpl'])

    loop = asyncio.get_event_loop()
    with YoutubeDL(ydl_opts) as ydl:
        await loop.run_in_executor(None, ydl.download, [video_url])

    # mp3_file = os.path.abspath("/app/processing/temp_video.mp3")
    return mp3_file

def convert_mp3_to_wav(mp3_file):
    # Convert MP3 to WAV
    wav_file = 'output.wav'
    audio = AudioSegment.from_file(mp3_file, format='mp3')
    audio.export(wav_file, format='wav')
    return wav_file

async def take_input(video_url):
    print("in take_input")
    mp3_file = await download_youtube_video(video_url)
    print("consumed video")
    wav_file = convert_mp3_to_wav(mp3_file)

    # Clean up temporary files
    # os.remove(mp3_file)

    print(f'Converted WAV file: {wav_file}')
    return wav_file
