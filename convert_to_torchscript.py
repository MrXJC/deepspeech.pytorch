# -*- coding: utf-8 -*-
import torch
import json
import argparse
import warnings
from opts import add_inference_args
from utils import load_model
warnings.simplefilter('ignore')


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(description='DeepSpeech transcription')
    arg_parser = add_inference_args(arg_parser)
    args = arg_parser.parse_args()
    device = torch.device("cuda" if args.cuda else "cpu")
    model = load_model(device, args.model_path, args.model_name, args.half)
    spect = torch.zeros(1, 1, int(model.audio_conf['sample_rate']*model.audio_conf['window_size']//2 + 1),
                        args.max_length)
    input_sizes = torch.IntTensor([args.max_length])
    traced_cell = torch.jit.trace(model, (spect, input_sizes))
    traced_cell.save(args.model_path + '-script.zip')
    script_json = {'audio_conf': model.audio_conf, 'labels': model.labels}
    with open(args.model_path + '-script.json', 'w') as f:
        json.dump(script_json, f)

