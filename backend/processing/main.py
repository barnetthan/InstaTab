import sys
from input import take_input
import librosa
from spleeter.separator import Separator
import os
import asyncio
import music21
import pretty_midi
from music21 import stream, note, meter, converter, instrument, stream
from midiutil import MIDIFile
import mir_eval
import pdb
# import pydsm
# import midi2tab
import numpy as np
import mido

async def make_tabs(video: str):
    # Convert the YouTube video to WAV
    wav_file = await take_input(video)

    # guitar_track = await extract_guitar_track(wav_file)

    # notes = detect_notes(guitar_track)
    #

    # pdb.set_trace()
    midi = convert_wav_to_midi(wav_file)


    # notes = detect_notes(wav_file)

    tabs = midi_to_tabs('temp_output.mid')

    # normalized_notes = normalize_notes(notes)

    # tabs = midi_to_tab(normalized_notes)

    # for string, fret in tabs:
    #     print(f'String {string}, Fret {round(fret)}')

    # print(len(tabs))

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


# def detect_notes(wav_file, magnitude_threshold=100.0):
#     y, sr = librosa.load(wav_file, sr=None)
#     pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)

#     notes = []
#     for t in range(pitches.shape[1]):
#         index = magnitudes[:, t].argmax()
#         pitch = pitches[index, t]
#         magnitude = magnitudes[index, t]
#         if pitch > 0 and magnitude > magnitude_threshold:
#             notes.append(librosa.hz_to_midi(pitch))


#     return notes



# def detect_notes(wav_file, magnitude_threshold=75.0, similarity_threshold=0.5):
#     y, sr = librosa.load(wav_file, sr=None)
#     pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)

#     notes = []
#     last_pitch = None

#     for t in range(pitches.shape[1]):
#         index = magnitudes[:, t].argmax()
#         pitch = pitches[index, t]
#         magnitude = magnitudes[index, t]

#         if pitch > 0 and magnitude > magnitude_threshold:
#             midi_note = librosa.hz_to_midi(pitch)
#             if last_pitch is None or abs(midi_note - last_pitch) > similarity_threshold:
#                 notes.append(midi_note)
#                 last_pitch = midi_note

#     return notes


# def detect_notes(wav_file, magnitude_threshold=50.0, similarity_threshold=0.75, time_threshold=0.15):
#     y, sr = librosa.load(wav_file, sr=None)
#     pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)

#     notes = []
#     last_pitch = None

#     for t in range(pitches.shape[1]):
#         index = magnitudes[:, t].argmax()
#         pitch = pitches[index, t]
#         magnitude = magnitudes[index, t]

#         if pitch > 0 and magnitude > magnitude_threshold:
#             midi_note = librosa.hz_to_midi(pitch)

#             if last_pitch is None or abs(midi_note - last_pitch) > similarity_threshold:
#                 notes.append(midi_note)
#                 last_pitch = midi_note

#     # Clump similar adjacent notes together within the time threshold
#     clumped_notes = []
#     current_note = None

#     for note in notes:
#         if current_note is None:
#             current_note = note
#         elif abs(note - current_note) <= similarity_threshold:
#             continue
#         else:
#             clumped_notes.append(current_note)
#             current_note = note

#     if current_note is not None:
#         clumped_notes.append(current_note)

#     return clumped_notes



# def detect_notes(wav_file, magnitude_threshold=50.0, similarity_threshold=0.75, time_threshold=0.15):
#     y, sr = librosa.load(wav_file, sr=None)
#     pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)

#     notes = []
#     last_pitch = None
#     last_time = None

#     for t in range(pitches.shape[1]):
#         index = magnitudes[:, t].argmax()
#         pitch = pitches[index, t]
#         magnitude = magnitudes[index, t]

#         if pitch > 0 and magnitude > magnitude_threshold:
#             midi_note = librosa.hz_to_midi(pitch)
#             current_time = t / sr  # Calculate the current time in seconds

#             if last_pitch is None or abs(midi_note - last_pitch) > similarity_threshold or (current_time - last_time) > time_threshold:
#                 notes.append(midi_note)
#                 last_pitch = midi_note
#                 last_time = current_time

#     # Clump similar adjacent notes together within the time threshold
#     clumped_notes = []
#     current_note = None

#     for note in notes:
#         if current_note is None:
#             current_note = note
#         elif abs(note - current_note) <= similarity_threshold:
#             continue
#         else:
#             clumped_notes.append(current_note)
#             current_note = note

#     if current_note is not None:
#         clumped_notes.append(current_note)

#     return clumped_notes


# def convert_wav_to_midi(wav_file):
#     y, sr = librosa.load(wav_file)
#     chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
#     pm = pretty_midi.PrettyMIDI()
#     instrument = pretty_midi.Instrument(program=0)

#     for pitch, chroma_notes in enumerate(chroma):
#         for time, value in enumerate(chroma_notes):
#             if value > 0:
#                 note = pretty_midi.Note(
#                     velocity=int(value * 127),
#                     pitch = pitch,
#                     start=time * 0.01,
#                     end=(time + 1) * 0.01
#                 )
#                 instrument.notes.append(note)

#     pm.instruments.append(instrument)

#     midi_file = 'temp_output.mid'
#     pm.write(midi_file)


def hz_to_note_num(hz):
    """
    Converts a frequency in Hz to a MIDI note number.

    Args:
        hz (float): The frequency in Hertz.

    Returns:
        int: The MIDI note number.
    """

    A4_freq = 440.0  # Reference frequency for A4
    return 12 * np.log2(hz / A4_freq) + 69

def convert_wav_to_midi(wav_file, fmin=32.7032, n_bins=84):
    """
    Converts a WAV file to a MIDI file using librosa and pretty_midi.

    Args:
        wav_file (str): Path to the input WAV file.
        output_midi_file (str): Path to the output MIDI file.
        fmin (float, optional): Minimum frequency of the CQT. Defaults to None, which uses librosa's default.
        n_bins (int, optional): Number of frequency bins in the CQT. Defaults to None, which uses librosa's default.
    """

    # Load the audio file
    y, sr = librosa.load(wav_file, mono=True)

    # Convert audio to a pitch representation (e.g., using CQT)
    C = librosa.cqt(y, sr=sr, fmin=fmin, n_bins=n_bins)

    # Detect onsets and offsets of notes
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    # Estimate note durations (e.g., using tempo estimation)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beats, sr=sr)

    # Create a PrettyMIDI object
    midi = pretty_midi.PrettyMIDI()

    # Create an instrument (e.g., piano)
    instrument = pretty_midi.Instrument(program=0)

    # Iterate over detected onsets and create MIDI notes
    for onset_time, beat_time in zip(onset_times, beat_times):
        # Estimate pitch from the CQT matrix
        pitch = np.argmax(C[:, int(librosa.time_to_frames(onset_time, sr=sr))])
        frequency = librosa.cqt_frequencies(fmin=fmin, n_bins=n_bins)[pitch]
        note_number = hz_to_note_num(frequency)

        # Estimate note duration based on the next onset or beat time
        duration = next((t - onset_time for t in onset_times if t > onset_time), beat_time - onset_time)

        # Create a MIDI note and add it to the instrument
        note = pretty_midi.Note(velocity=100, pitch=int(round(note_number)), start=onset_time, end=onset_time + duration)
        instrument.notes.append(note)

    # Add the instrument to the MIDI object and write to file
    midi.instruments.append(instrument)
    midi.write('temp_output.mid')
# # Example usage
# wav_file = 'your_audio.wav'
# output_midi_file = 'output.mid'
# wav_to_midi(wav_file, output_midi_file)


    # track = 0
    # time = 0

    # midi_notes, _ = mir_eval.melody.chroma_to_midi(chroma)
    # midi_file = MIDIFile(1)
    # for note in midi_notes:
    #     pitch = int(note[0])
    #     duration = int(note[1])
    #     velocity = int(note[2])

    #     midi_file.addNote(track, 0, pitch, time, duration, velocity)
    #     time += duration

    # with open ('temp_output.mid', 'wb') as file:
    #     midi_file.writeFile(file)


# def midi_to_tabs(midi_file):
#     # Load the MIDI file
#     midi_data = pretty_midi.PrettyMIDI(midi_file)
#     guitar_stream = stream.Stream()

#     pdb.set_trace()

#     # Iterate through all instruments in the MIDI file
#     for instrument in midi_data.instruments:
#         # Filter for guitar (you may need to adjust this)
#         # if instrument.name.lower() == 'guitar':
#         for note in instrument.notes:
#             # Convert MIDI note number to string representation
#             guitar_note = note.pitch # Get the MIDI number

#             # Here we convert MIDI note to string/tab position (basic example)
#             # You might want to create a more sophisticated mapping for guitar tabs
#             if 40 <= guitar_note <= 68:  # A common range for guitar notes
#                 guitar_stream.append(note.Note(guitar_note))

#     # Save to a file or print results
#     #

#     # for note in guitar_stream.notes:
#     #     string = note.pitch - 40 + 1
#     #     fret = note.octave - 2
#     #     print(f'String {string}, Fret {fret}')
#     guitar_stream.write('musicxml', fp='output_tabs.xml')  # Or handle output as needed

# def midi_to_tabs(midi_file):
    # midi_data = pydsm.MidiFile(midi_file)
    # tabs = midi2tab.from_file(midi_file)
    # for tab in tabs:
    #     print(f'String {tab.string}, Fret {tab.fret}')


def midi_to_tabs(midi_file):
    """
    Converts a MIDI file to basic guitar tab notation.

    Args:
        midi_file: Path to the MIDI file.

    Returns:
        None
    """

    # # Load the MIDI file
    # midi_stream = converter.parse(midi_file)

    # # Extract guitar parts (adjust this based on your MIDI file)
    # # guitar_parts = midi_stream.parts.filters(lambda p: p.partName.startswith('Guitar'))

    # # Define standard guitar tuning
    # tuning = ['E', 'A', 'D', 'G', 'B', 'E']
    # pdb.set_trace()
    # # Iterate over guitar parts and extract notes and chords
    # for part in midi_stream:
    #     for note in part.flat.notes:
    #         # Extract note information
    #         pitch = note.pitch.midi
    #         duration = note.duration.quarterLength

    #         # Convert MIDI pitch to guitar fret position (simplified)
    #         fret = pitch % 12
    #         string = tuning.index(note.pitch.name[0])


    # Define standard guitar tuning
    tuning = ['E2', 'A2', 'D3', 'G3', 'B3', 'E4']

    # Load the MIDI file
    midi_data = pretty_midi.PrettyMIDI(midi_file)

    # Create an empty list to store the tab notation
    tabs = []

    # Iterate over all instruments in the MIDI file
    for instrument in midi_data.instruments:
        # Filter for guitar (you may need to adjust this)
        # if instrument.name.lower() == 'guitar':
            i = 0
            for note in instrument.notes:
                # Extract note information
                pitch = note.pitch
                start_time = note.start
                end_time = note.end

                # Find the closest string to the note
                closest_string = None
                closest_distance = float('inf')
                for i, string_note in enumerate(tuning):
                    string_note_number = pretty_midi.note_name_to_number(string_note)
                    distance = abs(pitch - string_note_number)
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_string = i

                # Calculate the fret position
                fret = pitch - pretty_midi.note_name_to_number(tuning[closest_string])
                if fret < 0:
                    fret += 12  # Add 12 to bring it within the valid range

                # Add the tab notation to the list
                currentNote = {"string": closest_string + 1, "time": i, "fret": fret}
                tabs.append(currentNote)
                tabs.sort(key=lambda x: x['string'])
                i += 1

    # Print the tab notation
    for string, fret in tabs:
        print(f'String {string}, Fret {fret}')

    return tabs

# def detect_notes(wav_file, magnitude_threshold=0.0, similarity_threshold=0.1, time_threshold=0.01):
#     y, sr = librosa.load(wav_file, sr=None)
#     pitches, magnitudes = librosa.core.piptrack(y=y, sr=sr)

#     notes = []
#     last_pitch = None
#     last_time = None

#     for t in range(pitches.shape[1]):
#         index = magnitudes[:, t].argmax()
#         pitch = pitches[index, t]
#         magnitude = magnitudes[index, t]

#         if pitch > 0 and magnitude > magnitude_threshold:
#             midi_note = librosa.hz_to_midi(pitch)
#             current_time = t / sr  # Calculate the current time in seconds

#             if (last_pitch is None or abs(midi_note - last_pitch) > similarity_threshold) and \
#                (last_time is None or (current_time - last_time) > time_threshold):
#                 notes.append(midi_note)
#                 last_pitch = midi_note
#                 last_time = current_time

#     return notes

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



# def midi_to_tab(midi_notes):
#     tuning = [40, 45, 50, 55, 59, 64]  # Standard tuning E2, A2, D3, G3, B3, E4

#     tabs = []
#     for note in midi_notes:
#         best_string = None
#         best_fret = None
#         min_fret = float('inf')

#         for string, base_note in enumerate(tuning):
#             fret = note - base_note
#             if 0 <= fret <= 18 and fret < min_fret:  # Assumes max of 18 frets
#                 best_string = string + 1
#                 best_fret = fret
#                 min_fret = fret

#         if best_string is not None and best_fret is not None:
#             tabs.append((best_string, best_fret))
#         else:
#             # If the note is outside the range, try shifting it by octaves
#             while note > 76:  # E4 (highest open string on a standard-tuned guitar)
#                 note -= 12  # Transpose down one octave
#             while note < 40:  # E2 (lowest open string on a standard-tuned guitar)
#                 note += 12  # Transpose up one octave

#             # Try finding the best string and fret again after octave shift
#             for string, base_note in enumerate(tuning):
#                 fret = note - base_note
#                 if 0 <= fret <= 18 and fret < min_fret:  # Assumes max of 18 frets
#                     best_string = string + 1
#                     best_fret = fret
#                     min_fret = fret

#             if best_string is not None and best_fret is not None:
#                 tabs.append((best_string, best_fret))
#             else:
#                 print(f"Note {note} not included. Outside of guitar range")

#     return tabs



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
    youtube_video_url = 'https://youtu.be/eF-mB4hWdMg?si=3DptNc7svDUYPyRF'
    await make_tabs(youtube_video_url)

if __name__ == "__main__":
    asyncio.run(main())
    # Replace with your YouTube video URL
    # youtube_video_url = 'https://youtu.be/f6hmNzvq9oU?si=PqdnfxcxmnieXNko'
