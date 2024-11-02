import sys
from input import take_input
import librosa
from spleeter.separator import Separator
import os

def make_tabs(video: str):
    # Convert the YouTube video to WAV
    wav_file = take_input(video)

    guitar_track = extract_guitar_track(wav_file)

    # Extract features from the WAV file
    features = extract_features(wav_file)

    # You can now use the extracted features for further processing
    print("Feature extraction complete.")


def extract_guitar_track(wav_file):
    # Initialize spleeter separator
    separator = Separator('spleeter:2stems')

    # Separate the audio into vocals and accompaniment
    separator.separate_to_file(wav_file, 'output')

    # The separated guitar track will be in the 'output' directory
    guitar_track = os.path.join('output', 'temp_video', 'accompaniment.wav')

    return guitar_track

def extract_features(wav_file):
    # Load the audio file
    y, sr = librosa.load(wav_file, sr=None)

    # Extract features
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    mel = librosa.feature.melspectrogram(y=y, sr=sr)
    contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    tonnetz = librosa.feature.tonnetz(y=y, sr=sr)

    print(f'MFCCs: {mfccs.shape}')
    print(f'Chroma: {chroma.shape}')
    print(f'Mel: {mel.shape}')
    print(f'Contrast: {contrast.shape}')
    print(f'Tonnetz: {tonnetz.shape}')

    return {
        'mfccs': mfccs,
        'chroma': chroma,
        'mel': mel,
        'contrast': contrast,
        'tonnetz': tonnetz
    }
