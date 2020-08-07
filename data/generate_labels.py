# -*- coding: utf-8 -*-
import json
manifest_path = 'manifest.csv'
labels = []
with open(manifest_path, 'r') as f:
    for x in f.readlines():
        idx = x.strip().split(',')
        labels.extend(idx[1].split(' '))
labels = list(set(labels))
labels.append(' ')
labels.append('_')
labels.reverse()
print(len(labels))
f = open('labels/label_pinyin.json', 'w')
json.dump(labels, f, ensure_ascii=False)

labels = []
with open(manifest_path, 'r') as f:
    for x in f.readlines():
        idx = x.strip().split(',')
        labels.extend(list(idx[2]))
labels = list(set(labels))
labels.append(' ')
labels.append('_')
labels.reverse()
print(len(labels))
f = open('labels/label_word.json', 'w')
json.dump(labels, f, ensure_ascii=False)

