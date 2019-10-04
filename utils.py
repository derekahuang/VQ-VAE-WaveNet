from mu_law_ops import mu_law_decode_np
import numpy as np


def sample(pdf):
    cdf = np.cumsum(pdf, axis=1)
    cdf = cdf.reshape([-1])
    pred = cdf.searchsorted(np.random.rand())
    raw = np.reshape(pred, [])
    decoded = np.reshape(mu_law_decode_np(pred), [])
    return raw, decoded


def decode(predictions, mode='sample'):
    if mode == 'sample':
        raw, decoded = sample(predictions)
    elif mode == 'greedy':
        prob = tf.nn.softmax(predictions)
        pred = tf.math.argmax(prob, axis=-1)
        raw = tf.reshape(pred, [])
        decoded = tf.reshape(mu_law_decode(pred), [])
    else:
        print('implement on your own')
        return 0, 0
    return raw, decoded


def display_time(t, second):
    '''
    t: the time one batch used
    second: estimated remaining seconds based on t
    '''
    minute, hour = None, None
    if second > 60:
        minute = second // 60
        second %= 60
        if minute > 60:
            hour = minute // 60
            minute %= 60
    if hour is not None:
        display = ' [BATCH %.3fs / ETA %dh %dm %.3fs]     ' % (t, hour, minute, second)
    elif minute is not None:
        display = ' [BATCH %.3fs / ETA %dm %.3fs]     ' % (t, minute, second)
    else:
        display = ' [BATCH %.3fs / ETA %.3fs]     ' % (t, second)
    return display


def write_speaker_to_int(dataset='vctk'):
    if dataset == 'vctk':
        func = lambda s: s.split('/')[0]
        file_list = 'vctk_train.txt'
        write_as = 'vctk_speakers.txt'
    elif dataset == 'librispeech':
        func = lambda s: s.split('/')[-1].split('-', 1)[0]
        file_list = 'librispeech_train_clean_100.txt'
        write_as = 'librispeech_speakers.txt'
    else:
        assert 1 == 0, 'not implemented'

    speaker_to_int = {}
    with open(file_list) as file:
        files = file.readlines()
    with open(write_as, 'w') as file:
        for filename in files:
            speaker = func(filename)
            if speaker not in speaker_to_int:
                speaker_to_int[speaker] = len(speaker_to_int)
                file.write(speaker + ', ' + str(speaker_to_int[speaker]) + '\n')


def get_speaker_to_int(speaker_path):
    with open(speaker_path) as file:
        lines = file.readlines()
    speaker_to_int = {}
    for line in lines:
        speaker, number = line.strip().split(', ')
        speaker_to_int[speaker] = int(number)
    return speaker_to_int


if __name__ == '__main__':
    write_speaker_to_int('vctk')
    write_speaker_to_int('librispeech')

