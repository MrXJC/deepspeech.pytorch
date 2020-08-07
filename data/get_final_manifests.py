# -*- coding: utf-8 -*-
import pandas as pd
import argparse
import os
import re
from pypinyin import lazy_pinyin

parser = argparse.ArgumentParser(description='Processes and downloads an4.')
parser.add_argument('--merge-dir', default='manifests/', help='Path to all manifest files you want to merge')
parser.add_argument('--prefix_path', default='/root/Project/research/data/', help='Path to all data')
parser.add_argument('--min-duration', default=1, type=int,
                    help='Prunes training samples shorter than the min duration (given in seconds, default 1)')
parser.add_argument('--max-duration', default=15, type=int,
                    help='Prunes training samples longer than the max duration (given in seconds, default 15)')
parser.add_argument('--split-size', default=10000, type=int,
                    help='the size of test and val  data (work when the split_ratio is 0 default 10000)')
parser.add_argument('--split-ratio', default=0, type=float,
                    help='the split-ratio of test and val data (default 0)')
parser.add_argument('--shuffle', action='store_true', help='shuffle')

args = parser.parse_args()


# manifest dir
data_path = 'manifest.csv'
train_path = 'train_manifest.csv'
test_path = 'test_manifest.csv'
val_path = 'val_manifest.csv'


def merge_manifest():
    df = None
    for file in os.listdir(args.merge_dir):
        if file.endswith(".csv"):
            df_ = pd.read_csv(os.path.join(args.merge_dir, file), header=None)
            if df is None:
                df = df_
            else:
                df = pd.concat([df, df_])
    return df


def clean_manifest(df):
    df = df.dropna()
    # delete invalid duration
    df = df[df[3].map(lambda x: args.min_duration < x < args.max_duration)]
    # delete the sentence with English
    df = df[df[2].map(lambda x:not bool(re.search('[a-zA-Z]', x)))]
    # delete the shendiao

    # add the prefix
    df[0] = args.prefix_path+df[0]
    # change the format
    # df[1] = df[2].map(lambda x:  ' '.join(lazy_pinyin(x)))
    return df


def generate_labels(df):
    pass


def split_manifest(df):
    if args.shuffle:
        df = df.sample(frac=1).reset_index(drop=True)
    length = len(df)
    split_size = args.split_size
    split_ratio = args.split_ratio
    if split_ratio != 0:
        split_size = length * split_ratio
    df.to_csv(data_path, header=None, index=None)
    df.iloc[:-int(split_size*2)].to_csv(train_path, header=None, index=None)
    df.iloc[-int(split_size*2):-int(split_size)].to_csv(test_path, header=None, index=None)
    df.iloc[-int(split_size):].to_csv(val_path, header=None, index=None)
    print('data size: ', length)
    print('train size: ', length-split_size * 2)
    print('test size: ', int(split_size))
    print('val size: ', int(split_size))



df = merge_manifest()
df = clean_manifest(df)
split_manifest(df)






