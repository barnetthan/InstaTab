import sys
from input import take_input
import librosa
from spleeter.separator import Separator
import os
import asyncio
import music21

async def make_tabs(video: str):
    # Convert the YouTube video to WAV
    wav_file = await take_input(video)

    # guitar_track = await extract_guitar_track(wav_file)

    # notes = detect_notes(guitar_track)

    notes = detect_notes(wav_file)

    tabs = midi_to_tab(notes)

    # normalized_notes = normalize_notes(notes)

    # tabs = midi_to_tab(normalized_notes)

    for string, fret in tabs:
        print(f'String {string}, Fret {fret}')

    print(len(tabs))

    print("Complete")


async def extract_guitar_track(wav_file):
    # Initialize spleeter separator
    separator = Separator('spleeter:2stems')

    # Separate the audio into vocals and accompaniment
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, separator.separate_to_file, wav_file, 'output')

    # The separated guitar track will be in the 'output' directory
    guitar_track = os.path.join('output', 'temp_video', 'accompaniment.wav')

    return guitar_track


def detect_notes(wav_file, magnitude_threshold=100.0):
    y, sr = librosa.load(wav_file, sr=None)
    pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)

    notes = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        magnitude = magnitudes[index, t]
        if pitch > 0 and magnitude > magnitude_threshold:
            notes.append(librosa.hz_to_midi(pitch))


    return notes

# def normalize_notes(midi_notes):
#     normalized_notes = []
#     for note in midi_notes:
#         while note > 64:
#             note -= 12
#         while note < 40:
#             note += 12
#         normalized_notes.append(note)
#     return normalized_notes


def normalize_notes(midi_notes):
    # Convert MIDI notes to music21 notes
    music21_notes = [music21.note.Note(midi=int(note)) for note in midi_notes]

    # Create a music21 stream
    stream = music21.stream.Stream(music21_notes)

    # Analyze the key of the piece
    key = stream.analyze('key')
    print(f"Detected key: {key}")

    # # Transpose the stream to C major or A minor
    # if key.mode == 'major':
    #     interval = music21.interval.Interval(key.tonic, music21.pitch.Pitch('C'))
    # else:
    #     interval = music21.interval.Interval(key.tonic, music21.pitch.Pitch('A'))

    # transposed_stream = stream.transpose(interval)

    # Convert transposed notes back to MIDI
    # normalized_notes = [note.pitch.midi for note in transposed_stream.notes]

    # Ensure notes are within the guitar range
    # final_notes = []
    # for note in normalized_notes:
    #     while note > 64:  # E4 (highest open string on a standard-tuned guitar)
    #         note -= 12  # Transpose down one octave
    #     while note < 40:  # E2 (lowest open string on a standard-tuned guitar)
    #         note += 12  # Transpose up one octave
    #     final_notes.append(note)

    return normalized_notes


# def midi_to_tab(midi_notes):
#     tuning = [40, 45, 50, 55, 59, 64]

#     #List[Tuple(int, int, int)]
#     #String, time, fret

#     tabs = []
#     for note in midi_notes:
#         best_string = None
#         best_fret = None
#         min_fret = float('inf')
#         for string, base_note in enumerate(tuning):
#             fret = note - base_note
#             if 0 <= fret <= 18 and fret < min_fret: #Assumes max of 18 frets
#                 best_string = string + 1
#                 best_fret = fret
#                 min_fret = fret
#         if best_string is not None and best_fret is not None
#                 tabs.append((string + 1, fret))
#                 break
#             else:
#                 print("Note not included. outside of guitar range")

#     return tabsa



def midi_to_tab(midi_notes):
    tuning = [40, 45, 50, 55, 59, 64]  # Standard tuning E2, A2, D3, G3, B3, E4

    tabs = []
    for note in midi_notes:
        best_string = None
        best_fret = None
        min_fret = float('inf')

        for string, base_note in enumerate(tuning):
            fret = note - base_note
            if 0 <= fret <= 18 and fret < min_fret:  # Assumes max of 18 frets
                best_string = string + 1
                best_fret = fret
                min_fret = fret

        if best_string is not None and best_fret is not None:
            tabs.append((best_string, best_fret))
        else:
            # If the note is outside the range, try shifting it by octaves
            while note > 64:  # E4 (highest open string on a standard-tuned guitar)
                note -= 12  # Transpose down one octave
            while note < 40:  # E2 (lowest open string on a standard-tuned guitar)
                note += 12  # Transpose up one octave

            # Try finding the best string and fret again after octave shift
            for string, base_note in enumerate(tuning):
                fret = note - base_note
                if 0 <= fret <= 18 and fret < min_fret:  # Assumes max of 18 frets
                    best_string = string + 1
                    best_fret = fret
                    min_fret = fret

            if best_string is not None and best_fret is not None:
                tabs.append((best_string, best_fret))
            else:
                print(f"Note {note} not included. Outside of guitar range")

    return tabs



# def extract_features(wav_file):
#     # Load the audio file
#     y, sr = librosa.load(wav_file, sr=None)

#     # Extract features
#     mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
#     chroma = librosa.feature.chroma_stft(y=y, sr=sr)
#     mel = librosa.feature.melspectrogram(y=y, sr=sr)
#     contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
#     tonnetz = librosa.feature.tonnetz(y=y, sr=sr)

#     print(f'MFCCs: {mfccs.shape}')
#     print(f'Chroma: {chroma.shape}')
#     print(f'Mel: {mel.shape}')
#     print(f'Contrast: {contrast.shape}')
#     print(f'Tonnetz: {tonnetz.shape}')

#     return {
#         'mfccs': mfccs,
#         'chroma': chroma,
#         'mel': mel,
#         'contrast': contrast,
#         'tonnetz': tonnetz
#     }

async def main():
    youtube_video_url = 'http://youtube.com/watch?v=2lAe1cqCOXo'
    await make_tabs(youtube_video_url)

if __name__ == "__main__":
    asyncio.run(main())
    # Replace with your YouTube video URL
    # youtube_video_url = 'https://youtu.be/f6hmNzvq9oU?si=PqdnfxcxmnieXNko'
