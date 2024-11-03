import mido
from mido import Message, MidiFile, MidiTrack, MetaMessage
from math import sqrt
import wave
import numpy as np
from numpy.fft import fft
from scipy.signal import resample_poly

def data2midi(F, fs, N, bol, minvol):
    half_n = N // 2
    sec = N / fs
    soundtime = int(round(60 * sec, 0))
    volumes = (np.abs(F) / N * 4) ** 0.6

    freqs = np.arange(1, half_n) / sec
    midinotes = 69 + np.log10(freqs / 440) / 0.025085832972
    rounded_midinotes = np.round(midinotes).astype(int)

    otolist = np.zeros(128, dtype=np.int8)
    last_note = -1
    maxvolume = -1

    for i in range(1, half_n):
        i_sec = i / sec
        volume = volumes[i]
        if 32 < i_sec < 12873:
            rounded_midinote = rounded_midinotes[i - 1]
            if last_note != rounded_midinote:
                if last_note != -1:
                    maxvolume *= 0.2
                    maxvolume = min(maxvolume, 127)
                    otolist[last_note] = int(round(maxvolume, 0))
                last_note = rounded_midinote
                maxvolume = volume
            else:
                maxvolume = sqrt(maxvolume ** 2 + volume ** 2)

    sim = 2
    for j in range(24, 128):
        ol = otolist[j]
        bl = bol[j]
        if bl != 0:
            if ol < bl - sim or bl + sim < ol or ol < minvol or ol == 0:
                track.append(Message('note_off', note=j, channel=0, time=0))
                if ol > minvol:
                    track.append(Message('note_on', note=j, velocity=ol, channel=0, time=0))
            else:
                otolist[j] = bl
        else:
            if bl > minvol:
                track.append(Message('note_on', note=j, velocity=ol, channel=0, time=0))

    track.append(Message('note_off', note=0, channel=0, time=soundtime))

    return otolist


def read_wav(file_path):
    wf = wave.open(file_path, "rb")
    buf = wf.readframes(-1)

    if wf.getsampwidth() == 2:
        data = np.frombuffer(buf, dtype=np.int16)
    else:
        data = np.zeros(len(buf), dtype=np.int16)

    if wf.getnchannels() == 2:
        mono_data = data[::2]
    else:
        mono_data = data
    wf.close()
    return mono_data


def info_wav(file_path):
    ret = {}
    wf = wave.open(file_path, "rb")
    ret["ch"] = wf.getnchannels()
    ret["byte"] = wf.getsampwidth()
    ret["fs"] = wf.getframerate()
    ret["N"] = wf.getnframes()
    ret["sec"] = ret["N"] / ret["fs"]
    wf.close()
    return ret


def audio_split(data, win_size, overlap=4):
    len_data = len(data)
    win = np.hanning(win_size)

    step_size = win_size // overlap
    num_segments = (len_data - win_size) // step_size + 1

    indices = np.arange(0, num_segments * step_size, step_size)

    splited_data = np.zeros((num_segments + 1, win_size), dtype=np.int16)

    for idx, start in enumerate(indices):
        end = start + win_size
        segment = data[start:end]

        win_segment = segment * win

        splited_data[idx, :] = win_segment

    remaining = len_data - indices[-1] - win_size
    if remaining > 0:
        win = np.hanning(len(segment))
        win_segment = segment * win

        padded_segment = np.pad(win_segment, (0, win_size - len(win_segment)), 'constant')

        splited_data[-1, :] = padded_segment

    return splited_data


def change_samplingrate(target_fs, data, fs):
    data = data.astype(np.int32)

    data_max_val = max(np.max(data), -np.min(data))
    data = data / data_max_val

    downed_data = resample_poly(data, target_fs, fs)

    max_val = max(np.max(downed_data), -np.min(downed_data))
    amp = 32767 / max_val

    downed_data = downed_data * amp

    downed_data = np.clip(downed_data, -32768, 32767)

    downed_data = downed_data.astype(np.int16)

    return downed_data


def convert_wav_to_midi(wav_file):
    mid = MidiFile()
    global track
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(MetaMessage('set_tempo', tempo=mido.bpm2tempo(480)))


    data = read_wav(wav_file)

    wi = info_wav(wav_file)

    new_fs = 40960
    if wi["fs"] != new_fs:
        samped_data = change_samplingrate(new_fs, data, wi["fs"])
    else:
        samped_data = data
    del data

    win_size = 1024 * 16

    splited_data = audio_split(samped_data, win_size)
    del samped_data

    minvol = 4
    bol = [0 for _ in range(128)]
    len_splited_data = len(splited_data)
    for i in range(0, len_splited_data):
        ffted_data = fft(splited_data[i])
        bol = data2midi(ffted_data, new_fs, len(ffted_data.imag), bol, minvol)

    time = int(round(120 * (len_splited_data/new_fs), 0))
    for i in range(35, 128):
        if bol[i] > minvol:
            track.append(Message('note_on', note=bol[i], channel=0, time=0))
    for j in range(35, 128):
        if j == 0:
            track.append(Message('note_off', note=0, channel=0, time=time))
        else:
            track.append(Message('note_off', note=j, channel=0, time=0))

    out_file = "test_wav.mid"
    mid.save(out_file)
