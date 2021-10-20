import sys
version = sys.version_info
assert version[0] >= 3, 'Python 2 is not supported'
assert version[1] >= 6, 'Requires Python 3.6 or higher'

import argparse
from enum import Enum, auto
import os
os.environ['IMAGEIO_USERDIR'] = '/var/tmp'
from pathlib import Path
from typing import Dict

import imageio
imageio.plugins.freeimage.download()
import numpy as np


class WriteFormat(Enum):
    OPENCV = auto()
    IMAGEIO = auto()


def is_string_swiss(input_str: str) -> bool:
    is_swiss = False
    is_swiss |= 'thun_' in input_str
    is_swiss |= 'interlaken_' in input_str
    is_swiss |= 'zurich_city_' in input_str
    return is_swiss


def flow_16bit_to_float(flow_16bit: np.ndarray, valid_in_3rd_channel: bool):
    assert flow_16bit.dtype == np.uint16
    assert flow_16bit.ndim == 3
    h, w, c = flow_16bit.shape
    assert c == 3

    if valid_in_3rd_channel:
        valid2D = flow_16bit[..., 2] == 1
        assert valid2D.shape == (h, w)
        assert np.all(flow_16bit[~valid2D, -1] == 0)
    else:
        valid2D = np.ones_like(flow_16bit[..., 2], dtype=np.bool)
    valid_map = np.where(valid2D)

    # to actually compute something useful:
    flow_16bit = flow_16bit.astype('float')

    flow_map = np.zeros((h, w, 2))
    flow_map[valid_map[0], valid_map[1], 0] = (flow_16bit[valid_map[0], valid_map[1], 0] - 2**15) / 128
    flow_map[valid_map[0], valid_map[1], 1] = (flow_16bit[valid_map[0], valid_map[1], 1] - 2**15) / 128
    return flow_map, valid2D


def load_flow(flowfile: Path, valid_in_3rd_channel: bool, write_format=WriteFormat):
    assert flowfile.exists()
    assert flowfile.suffix == '.png'

    # imageio reading assumes write format was rgb
    flow_16bit = imageio.imread(str(flowfile), format='PNG-FI')
    if write_format == WriteFormat.OPENCV:
        # opencv writes as bgr -> flip last axis to get rgb
        flow_16bit = np.flip(flow_16bit, axis=-1)
    else:
        assert write_format == WriteFormat.IMAGEIO

    channel3 = flow_16bit[..., -1]
    assert channel3.max() <= 1, f'Maximum value in last channel should be 1: {flowfile}'
    flow, valid2D = flow_16bit_to_float(flow_16bit, valid_in_3rd_channel)
    return flow, valid2D


def list_of_dirs(dirpath: Path):
    return next(os.walk(dirpath))[1]


def files_per_sequence(flow_timestamps_dir: Path) -> Dict[str, int]:
    out_dict = dict()
    for entry in flow_timestamps_dir.iterdir():
        assert entry.is_file()
        assert entry.suffix == '.csv', entry.suffix
        assert is_string_swiss(entry.stem), entry.stem
        data = np.loadtxt(entry, dtype=np.int64, delimiter=', ', comments='#')
        assert data.ndim == 2, data.ndim
        num_files = data.shape[0]
        out_dict[entry.stem] = num_files
    return out_dict


def check_submission(submission_dir: Path, flow_timestamps_dir: Path):
    assert flow_timestamps_dir.is_dir()
    assert submission_dir.is_dir()

    name2num = files_per_sequence(flow_timestamps_dir)

    expected_flow_shape = (480, 640, 2)
    expected_valid_shape = (480, 640)
    expected_dir_names = set([*name2num])
    actual_dir_names = set(list_of_dirs(submission_dir))
    assert expected_dir_names == actual_dir_names, f'Expected directories in your submission: {expected_dir_names}.\nMissing directories: {expected_dir_names.difference(actual_dir_names)}'

    for seq in submission_dir.iterdir():
        if not seq.is_dir():
            continue
        assert seq.is_dir()
        assert is_string_swiss(seq.name), seq.name
        num_files = 0
        for prediction in seq.iterdir():
            flow, valid_map = load_flow(prediction, valid_in_3rd_channel=False, write_format=WriteFormat.IMAGEIO)
            assert flow.shape == expected_flow_shape, f'Expected shape: {expected_flow_shape}, actual shape: {flow.shape}'
            assert valid_map.shape == expected_valid_shape, f'Expected shape: {expected_valid_shape}, actual shape: {valid_map.shape}'
            num_files += 1
        assert seq.name in [*name2num], f'{seq.name} not in {[*name2num]}'
        assert num_files == name2num[seq.name], f'expected {name2num[seq.name]} files in {str(seq)} but only found {num_files} files'

    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('submission_dir', help='Path to submission directory')
    parser.add_argument('flow_timestamps_dir', help='Path to directory containing the flow timestamps for evaluation.')

    args = parser.parse_args()

    print('start checking submission')
    check_submission(Path(args.submission_dir), Path(args.flow_timestamps_dir))
    print('Your submission directory has the correct structure: Ready to submit!\n')
    print('Note, that we will sort the files according to their names in each directory and evaluate them sequentially. Follow the exact naming instructions if you are unsure.')
