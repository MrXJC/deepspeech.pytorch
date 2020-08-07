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
DATA = 'data_thchs30'
DATA_URL = ''
DATA_TGZ = DATA + '.tgz'
MANIFESTS = 'manifests'
DATA_CSV = os.path.join(MANIFESTS, DATA + '_manifest.csv')

parser = argparse.ArgumentParser(description='Processes and downloads ' + DATA)
parser.add_argument('--target-dir', default='.', help='Path to save dataset')
args = parser.parse_args()


def _parse(train_path, name, data):
    train_path = os.path.join(train_path, name)
    prefix = len(args.target_dir) if args.target_dir[-1] == '/' or args.target_dir[-1] == '\\' else len(args.target_dir) + 1
    with os.popen('find %s -type f -name "*.trn"' % train_path) as pipe:
        for line in pipe:
            try:
                meta_data = dict()
                txt_path = line.strip().split('/')
                txt_path[-2] = 'data'
                txt_path = '/'.join(txt_path)
                raw_path = line.replace('.trn', '').strip()
                duration = float(
                    subprocess.check_output(['soxi -D \"%s\"' % raw_path],
                                            shell=True))
                if duration == 0:
                    continue
                meta_data['duration'] = duration
                meta_data['path'] = raw_path[prefix:]
                with open(txt_path, 'r') as f:
                    text = f.readlines()[0].strip()
                    meta_data['text'] = text.replace(' ','')
                    meta_data['pinyin'] = ' '.join(
                        [x[0] for x in pinyin(meta_data['text'], style=Style.TONE3)])
                data.append(meta_data)
                if len(data)%10000 == 1:
                    pd.DataFrame(data, columns=['path', 'pinyin', 'text', 'duration']).to_csv(DATA_CSV, header=None, index=None)
                    print(len(data))
            except Exception as e:
                print(e)


def main():
    data = []
    target_path = os.path.join(args.target_dir, DATA)
    if not os.path.exists(target_path):
        tar_path = os.path.join(args.target_dir, DATA_TGZ)
        if not os.path.exists(tar_path):
            wget.download(DATA_URL, out=args.target_dir)
        tar = tarfile.open(tar_path)
        tar.extractall(args.tar_path)
    if not os.path.exists(MANIFESTS):
        os.makedirs(MANIFESTS)
    _parse(target_path, 'dev', data)
    _parse(target_path, 'test', data)
    _parse(target_path, 'train', data)
    pd.DataFrame(data, columns=['path', 'pinyin', 'text', 'duration']).to_csv(DATA_CSV, header=None, index=None)
#     os.remove(target_path)

if __name__ == '__main__':
    main()

