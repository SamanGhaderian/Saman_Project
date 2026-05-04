import numpy as np

def get_channel(signal, channel_index=0):
    return signal[:, channel_index]


def get_window(signal, fs, seconds):
    samples = int(seconds * fs)
    return signal[:samples]


def compute_average(signal):
    return np.mean(signal)