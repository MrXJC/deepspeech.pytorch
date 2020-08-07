# -*- coding: utf-8 -*-
import argparse
import os
import io
import shutil
import tarfile
import wget
import pandas as pd
from pypinyin import pinyin, lazy_pinyin, Style
from pydub import AudioSegment
DATA = 'magicdata'
DATA_URL = ''
DATA_TGZ = DATA + '.tgz'
MANIFESTS = 'manifests'
DATA_CSV = os.path.join(MANIFESTS, DATA + '_manifest.csv')

parser = argparse.ArgumentParser(description='Processes and downloads ' + DATA)
parser.add_argument('--target-dir', default='.', help='Path to save dataset')
args = parser.parse_args()


def _construct_data(target_path, env, data):
    tar_path = os.path.join(target_path, env+'_set.tar.gz')
    if os.path.exists(tar_path):
        tar = tarfile.open(tar_path)
        tar.extractall(target_path)
        # os.remove(tar_path)
    train_path = os.path.join(tar_path, env, 'TRANS.txt')
    df = pd.read_csv(train_path, sep='\t')
    df = df.rename(columns={'Transcription': 'text'})
    df['path'] = 'magicdata/'+env+'/' + df['SpeakerID']+'/'+df['UtteranceID']
    df['duration'] = df['path'].map(lambda x: len(AudioSegment.from_file(x))/1000)
    df['pinyin'] = df['text'].map(lambda text: ' '.join([x[0] for x in pinyin(text, style=Style.TONE3)]))
    return df


def main():
    data = []
    target_path = os.path.join(args.target_dir, DATA)
    # if not os.path.exists(target_path):
        # tar_path = os.path.join(args.target_dir, DATA_TGZ)
        # if not os.path.exists(tar_path):
            # wget.download(DATA_URL, out=args.target_dir)
        # tar = tarfile.open(tar_path)
        # tar.extractall(args.tar_path)
    if not os.path.exists(MANIFESTS):
        os.makedirs(MANIFESTS)
    df_ = []
    for env in ['train', 'test', 'dev']:
        df = _construct_data(target_path, env, data)
        if len(df_) >0:
            df_ = pd.concat([df_,df],axis=0)
        else:
            df_ = df
    df_[['path', 'pinyin', 'text', 'duration']].to_csv(DATA_CSV, header=None, index=None)
#     os.remove(target_path)

if __name__ == '__main__':
    main()

