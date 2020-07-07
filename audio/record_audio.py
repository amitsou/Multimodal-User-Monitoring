import sys
import time
import numpy
import scipy
import cv2
import argparse
import scipy.io.wavfile as wavfile
from pyAudioAnalysis import ShortTermFeatures as sF
from pyAudioAnalysis import MidTermFeatures as mF
from pyAudioAnalysis import audioTrainTest as aT
import scipy.signal
import itertools
import operator
import datetime
import signal
import pyaudio
import os
import struct

global fs
global all_data
global outstr
fs = 8000
FORMAT = pyaudio.paInt16
all_data = []
plot_h = 150
plot_w = 720
status_h = 150


def signal_handler(signal, frame):
    """
    This function is called when Ctr + C is pressed and is used to output the
    final buffer into a WAV file
    """
    # write final buffer to wav file
    if len(all_data) > 1:
        wavfile.write(outstr + ".wav", fs, numpy.int16(all_data))
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)



"""
Utility functions
"""


def most_common(L):
    # get an iterable of (item, iterable) pairs
    SL = sorted((x, i) for i, x in enumerate(L))
    groups = itertools.groupby(SL, key=operator.itemgetter(0))

    # auxiliary function to get "quality" for an item
    def _auxfun(g):
        item, iterable = g
        count = 0
        min_index = len(L)
        for _, where in iterable:
            count += 1
            min_index = min(min_index, where)
        return count, -min_index

    # pick the highest-count/earliest item
    return max(groups, key=_auxfun)[0]


def plotCV(function, width, height, max_val):
    if len(function) > width:
        hist_item = height * (function[len(function) - width - 1:-1] / max_val)
    else:
        hist_item = height * (function / max_val)
    h = numpy.zeros((height, width, 3))
    hist = numpy.int32(numpy.around(hist_item))

    for x, y in enumerate(hist):
        cv2.line(h, (x, int(height / 2)),
                 (x, height - y), (255, 0, 255))

    return h


"""
Core functionality:
"""


def record_audio(block_size, fs=8000, show_spec=False, show_chroma=False,
                 log_sounds=False, logs_all=False):

    # inialize recording process
    mid_buf_size = int(fs * block_size)
    pa = pyaudio.PyAudio()
    stream = pa.open(format=FORMAT, channels=1, rate=fs,
                     input=True, frames_per_buffer=mid_buf_size)
    mid_buf = []
    count = 0
    global all_data
    global outstr
    all_data = []
    # initalize counters etc
    time_start = time.time()
    outstr = datetime.datetime.now().strftime("%Y_%m_%d_%I:%M%p")
    out_folder = outstr + "_segments"
    if log_sounds:
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)
    # load segment model
    [classifier, MEAN, STD, class_names,
     mt_win, mt_step, st_win, st_step, _] = aT.load_model("model")

    while 1:
        try:
            block = stream.read(mid_buf_size)
            count_b = len(block) / 2
            format = "%dh" % (count_b)
            shorts = struct.unpack(format, block)
            cur_win = list(shorts)
            mid_buf = mid_buf + cur_win
            del cur_win

            # time since recording started:
            e_time = (time.time() - time_start)
            # data-driven time
            data_time = (count + 1) * block_size
            x = numpy.int16(mid_buf)
            seg_len = len(x)

            # extract features
            # We are using the signal length as mid term window and step,
            # in order to guarantee a mid-term feature sequence of len 1
            [mt_feats, _, _] = mF.mid_feature_extraction(x, fs,
                                                         seg_len,
                                                         seg_len,
                                                         round(fs * st_win),
                                                         round(fs * st_step)
                                                         )
            cur_fv = (mt_feats[:, 0] - MEAN) / STD
            # classify vector:
            [res, prob] = aT.classifier_wrapper(classifier, "svm_rbf",
                                                cur_fv)
            win_class = class_names[int(res)]
            win_prob = prob[int(res)]

            if logs_all:
                all_data += mid_buf
            mid_buf = numpy.double(mid_buf)


            # Activity Detection:
            print("{0:.2f}\t{1:s}\t{2:.2f}".format(e_time,
                                                   win_class,
                                                   win_prob))

            if log_sounds:
                # TODO: log audio files
                out_file = os.path.join(out_folder,
                                        "{0:.2f}_".format(e_time).zfill(8) +
                                        win_class + ".wav")
                #shutil.copyfile("temp.wav", out_file)
                wavfile.write(out_file, fs, x)

            textIm = numpy.zeros((status_h, plot_w, 3))
            statusStrTime = "time: %.1f sec" % e_time + \
                            " - data time: %.1f sec" % data_time + \
                            " - loss : %.1f sec" % (e_time - data_time)
            cv2.putText(textIm, statusStrTime, (0, 11),
                        cv2.FONT_HERSHEY_PLAIN, 1, (200, 200, 200))
            cv2.putText(textIm, win_class, (0, 33),
                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
            cv2.imshow("Status", textIm)
            cv2.moveWindow("Status", 50, 0)
            mid_buf = []
            ch = cv2.waitKey(10)
            count += 1
        except IOError:
            print("Error recording")


def parse_arguments():
    record_analyze = argparse.ArgumentParser(description="Real time "
                                                         "audio analysis")
    record_analyze.add_argument("-bs", "--blocksize",
                                  type=float, choices=[0.25, 0.5, 0.75, 1, 2],
                                  default=1, help="Recording block size")
    record_analyze.add_argument("-fs", "--samplingrate", type=int,
                                  choices=[4000, 8000, 16000, 32000, 44100],
                                  default=8000, help="Recording block size")
    record_analyze.add_argument("--chromagram", action="store_true",
                                  help="Show chromagram")
    record_analyze.add_argument("--spectrogram", action="store_true",
                                  help="Show spectrogram")
    record_analyze.add_argument("--record_segments", action="store_true",
                                  help="Record detected sounds to wavs")
    record_analyze.add_argument("--record_all", action="store_true",
                                  help="Record the whole recording to a single"
                                       " audio file")
    return record_analyze.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    fs = args.samplingrate
    if fs != 8000:
        print("Warning! Segment classifiers have been trained on 8KHz samples. "
              "Therefore results will be not optimal. ")
    record_audio(args.blocksize, fs, args.spectrogram,
                 args.chromagram, args.record_segments, args.record_all)
