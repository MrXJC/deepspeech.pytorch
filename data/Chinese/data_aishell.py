# -*- coding: utf-8 -*-
import argparse
import os
import io
import shutil
import tarfile
import wget
import pandas as pd
from pypinyin import pinyin, lazy_pinyin, Style
import subprocess
import json
DATA = 'data_aishell'
DATA_URL = ''
DATA_TGZ = DATA + '.tgz'
MANIFESTS = 'manifests'
DATA_CSV = os.path.join(MANIFESTS, DATA + '_manifest.csv')
# No meta data
parser = argparse.ArgumentParser(description='Processes and downloads ' + DATA)
parser.add_argument('--target-dir', default='.', help='Path to save dataset')
args = parser.parse_args()


def _parse(train_path, data):
    prefix = len(args.target_dir) if args.target_dir[-1] == '/' or args.target_dir[-1] == '\\' else len(args.target_dir) + 1
    with os.popen('find %s -type f -name "*.wav"' % train_path) as pipe:
        for line in pipe:
            try:
                meta_data = dict()
                raw_path = line.strip()
                duration = float(
                    subprocess.check_output(['soxi -D \"%s\"' % raw_path],
                                            shell=True))
                if duration == 0:
                    continue
                meta_data['duration'] = duration
                meta_data['path'] = raw_path[prefix:]
                data.append(meta_data)
                if len(data)%10000 == 1:
                    print(len(data))
            except Exception as e:
                print(e)


def _construct_data(target_path):
    train_path = os.path.join(target_path, 'wav')
    for x in os.listdir(train_path):
        if x[-2:] == 'gz':
            tar_path = os.path.join(train_path, x)
            tar = tarfile.open(tar_path)
            tar.extractall(train_path)
            os.remove(tar_path)
    # data = []
    # data_path = os.path.join(train_path, 'train')
    # for x in os.listdir(data_path):
        # _parse(os.path.join(data_path, x), data)
    # data_path = os.path.join(train_path, 'test')
    # for x in os.listdir(data_path):
        # _parse(os.path.join(data_path, x), data)
    # data_path = os.path.join(train_path, 'dev')
    # for x in os.listdir(data_path):
        # _parse(os.path.join(data_path, x), data)
    # transcript_path = os.path.join(os.path.join(target_path, 'transcript'), 'aishell_transcript_v0.8.txt')
    # with open(transcript_path, 'r') as f:
        # transcript_dict = {name+'.wav': text.strip().replace(' ','') for name, text in [(x[:16], x[16:]) for x in f.readlines()]}
    # df = pd.DataFrame(data)
    # df['text'] = df['path'].map(lambda x: transcript_dict.get(os.path.basename(x), ''))
    # df['pinyin'] = df['text'].map(lambda x: ' '.join([y[0] for y in pinyin(x, style=Style.TONE3)]))
    # df[['path', 'pinyin', 'text', 'duration']].to_csv(DATA_CSV, header=None, index=None)

def main():
    target_path = os.path.join(args.target_dir, DATA)
    if not os.path.exists(target_path):
        tar_path = os.path.join(args.target_dir, DATA_TGZ)
        if not os.path.exists(tar_path):
            wget.download(DATA_URL, out=args.target_dir)
        tar = tarfile.open(tar_path)
        tar.extractall(args.target_dir)
    if not os.path.exists(MANIFESTS):
        os.makedirs(MANIFESTS)
    _construct_data(target_path)
#     os.remove(target_path)
if __name__ == '__main__':
    main()

