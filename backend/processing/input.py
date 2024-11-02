from pytube import YouTube
from pydub import AudioSegment
import os

def download_youtube_video(video_url):
    # Download the YouTube video
    yt = YouTube(video_url)
    print(f'Downloading: {yt.title}')
    video_stream = yt.streams.filter(only_audio=True).first()
    mp4_file = video_stream.download(filename='temp_video.mp4')
    return mp4_file

def convert_mp4_to_mp3(mp4_file):
    # Convert MP4 to MP3
    mp3_file = 'output.mp3'
    audio = AudioSegment.from_file(mp4_file, format='mp4')
    audio.export(mp3_file, format='mp3')
    return mp3_file

def convert_mp3_to_wav(mp3_file):
    # Convert MP3 to WAV
    wav_file = 'output.wav'
    audio = AudioSegment.from_file(mp3_file, format='mp3')
    audio.export(wav_file, format='wav')
    return wav_file

def take_input(video_url):
    mp4_file = download_youtube_video(video_url)
    mp3_file = convert_mp4_to_mp3(mp4_file)
    wav_file = convert_mp3_to_wav(mp3_file)

    # Clean up temporary files
    os.remove(mp4_file)
    os.remove(mp3_file)

    print(f'Converted WAV file: {wav_file}')

if __name__ == "__main__":
    # Replace with your YouTube video URL
    youtube_video_url = 'https://www.youtube.com/watch?v=YOUR_VIDEO_ID'
    take_input(youtube_video_url)
