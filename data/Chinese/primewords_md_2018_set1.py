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
DATA = 'primewords_md_2018_set1'
DATA_URL = ''
DATA_TGZ = DATA + '.tar.gz'
MANIFESTS = 'manifests'
DATA_CSV = os.path.join(MANIFESTS, DATA + '_manifest.csv')

parser = argparse.ArgumentParser(description='Processes and downloads ' + DATA)
parser.add_argument('--target-dir', default='.', help='Path to save dataset')
args = parser.parse_args()

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
    prefix = len(args.target_dir) if args.target_dir[-1] == '/' or args.target_dir[-1] == '\\' else len(args.target_dir) + 1
    data_path = os.path.join(target_path, 'set1_transcript.json')
    data = json.load(open(data_path, 'r'))
    df = pd.DataFrame(data)
    audio_path = os.path.join(target_path, 'audio_files')
    df['path'] = df['file'].map(lambda x: os.path.join(os.path.join(os.path.join(audio_path, x[0]), x[:2]), x)[prefix:])
    df['text'] = df['text'].map(lambda x: x.replace(' ',''))
    df['pinyin'] = df['text'].map(lambda x: ' '.join([y[0] for y in pinyin(x, style=Style.TONE3)]))
    df['duration'] = df['length']
    df[['path', 'pinyin', 'text', 'duration']].to_csv(DATA_CSV, header=None, index=None)
#     # _construct_data(target_path, 'dev', data)
    # _construct_data(target_path, 'test', data)
    # _construct_data(target_path, 'train', data)
    # pd.DataFrame(data, columns=['path', 'pinyin', 'text', 'duration']).to_csv(DATA_CSV, header=None, index=None)
#     os.remove(target_path)
if __name__ == '__main__':
    main()

