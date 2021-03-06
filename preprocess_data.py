import numpy as np
import mxnet as mx
from collections import namedtuple, Counter
from unidecode import unidecode
from itertools import groupby
from mxnet.io import DataBatch, DataIter
from random import shuffle
from mxnet import ndarray
from time import time
import uuid
import os
from tqdm import tqdm

from utils import tokenize_text, invert_dict, get_s2s_data, Dataset

from seq2seq_iterator import Seq2SeqIter

import operator
import cPickle as pickle
import re
import warnings

if __name__ == '__main__':

    # Get rid of annoying Python deprecation warnings from built-in JSON encoder
    warnings.filterwarnings("ignore", category=DeprecationWarning)   
 
    start = time()

    dataset = get_s2s_data(
        src_train_path=  './data/wmt15-de-en/train.de',
        src_valid_path=  './data/wmt15-de-en/valid.de',
        src_test_path = './data/wmt15-de-en/test.de',
        targ_train_path= './data/wmt15-de-en/train.en',
        targ_valid_path= './data/wmt15-de-en/valid.en',
        targ_test_path = './data/wmt15-de-en/test.en'
    )

   
    preproc_duration = time() - start
    print("\nPreprocessing data took %.4f seconds\n" % preproc_duration)

    min_len = 5

    max_len = 55
    increment = 10

    all_pairs = [(i, j) for i in xrange(
            min_len,max_len+increment,increment
        ) for j in xrange(
            min_len,max_len+increment,increment
        )]

#    all_pairs = [(5, 5), (15,15), (20, 20)]
#    max_sent_len = 25

    batch_size=64

    print("Constructing train iterator")
    start = time()
    train_iter = Seq2SeqIter(dataset.src_train_sent, dataset.targ_train_sent, dataset.src_vocab, dataset.inv_src_vocab,
                     dataset.targ_vocab, dataset.inv_targ_vocab, layout='TN', batch_size=batch_size, buckets=all_pairs, max_sent_len=max_len)

    train_iter.bucketize()
    train_iter_duration = time() - start
    print("\nBucketizing data for training set iterator took %.4f seconds\n" % train_iter_duration)
	 
    print("Serializing training set iterator.")
    start = time()
    with open('./data/train_iterator.pkl', 'wb') as f:
        pickle.dump(train_iter, f, pickle.HIGHEST_PROTOCOL)
    train_ser_duration = time() - start
    print("\nSerializing training iterator took %.4f seconds\n" % train_ser_duration)   


    print("Constructing valid iterator")
    valid_iter_duration = time()
    valid_iter = Seq2SeqIter(dataset.src_valid_sent, dataset.targ_valid_sent, dataset.src_vocab, dataset.inv_src_vocab,
                     dataset.targ_vocab, dataset.inv_targ_vocab, layout='TN', batch_size=batch_size, buckets=all_pairs, max_sent_len=max_len)

    valid_iter.bucketize()
    valid_iter_duration = time() - start
    print("\nBucketizing data for validation set iterator took %.4f seconds\n" % valid_iter_duration)

    print("Serializing validation set iterator.")
    start = time()
    with open('./data/valid_iterator.pkl', 'wb') as f:
        pickle.dump(valid_iter, f, pickle.HIGHEST_PROTOCOL)
    valid_ser_duration = time() - start
    print("\nSerializing validation set iterator took %.4f seconds\n" % valid_ser_duration)

    print("Constructing test iterator")
    test_iter_duration = time()
    test_iter = Seq2SeqIter(dataset.src_test_sent, dataset.targ_test_sent, dataset.src_vocab, dataset.inv_src_vocab,
                     dataset.targ_vocab, dataset.inv_targ_vocab, layout='TN', batch_size=batch_size, buckets=all_pairs, max_sent_len=max_len)

    test_iter.bucketize()
    test_iter_duration = time() - start
    print("\nBucketizing data for test set iterator took %.4f seconds\n" % test_iter_duration)

    print("Serializing test set iterator.")
    start = time()
    with open('./data/test_iterator.pkl', 'wb') as f:
        pickle.dump(test_iter, f, pickle.HIGHEST_PROTOCOL)
    test_ser_duration = time() - start
    print("\nSerializing test set iterator took %.4f seconds\n" % test_ser_duration)

