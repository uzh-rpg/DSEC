import sys
version = sys.version_info
assert version[0] >= 3, 'Python 2 is not supported'
assert version[1] >= 6, 'Requires Python 3.6 or higher'

import argparse
import os
from pathlib import Path
from typing import Dict

import numpy as np

has_cv2 = True
try:
    import cv2
except ImportError:
    has_cv2 = False

try:
    from PIL import Image
except ImportError:
    assert has_cv2, 'Either install opencv-python or Pillow'


def is_string_swiss(input_str: str) -> bool:
    is_swiss = False
    is_swiss |= 'thun_' in input_str
    is_swiss |= 'interlaken_' in input_str
    is_swiss |= 'zurich_city_' in input_str
    return is_swiss


def load_disparity(filepath: Path):
    assert filepath.is_file()
    assert filepath.suffix == '.png', filepath.suffix
    if has_cv2:
        disp = cv2.imread(str(filepath), cv2.IMREAD_ANYDEPTH).astype("float32") / 256.0
    else:
        disp = np.array(Image.open(str(filepath))).astype("float32") / 256.0
    return disp


def files_per_sequence(disparity_timestamps_dir: Path) -> Dict[str, int]:
    out_dict = dict()
    for entry in disparity_timestamps_dir.iterdir():
        assert entry.is_file()
        assert entry.suffix == '.csv', entry.suffix
        assert is_string_swiss(entry.stem), entry.stem
        data = np.loadtxt(entry, dtype=np.int64, delimiter=', ', comments='#')
        assert data.ndim == 2, data.ndim
        num_files = data.shape[0]
        out_dict[entry.stem] = num_files
    return out_dict


if __name__ ==  '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('submission_dir', help='Path to submission directory')
    parser.add_argument('disparity_timestamps_dir', help='Path to directory containing the disparity timestamps for evaluation.')

    args = parser.parse_args()

    ref_disp_ts_dir = Path(args.disparity_timestamps_dir)
    assert ref_disp_ts_dir.is_dir()

    submission_dir = Path(args.submission_dir)
    assert submission_dir.is_dir()

    name2num = files_per_sequence(ref_disp_ts_dir)

    expected_disparity_shape = (480, 640)

    expected_dir_names = set([*name2num])
    actual_dir_names = set(os.listdir(submission_dir))
    assert expected_dir_names == actual_dir_names, f'Expected directories in your submission: {expected_dir_names}.\nMissing directories: {expected_dir_names.difference(actual_dir_names)}'

    for seq in submission_dir.iterdir():
        assert seq.is_dir()
        assert is_string_swiss(seq.name), seq.name
        num_files = 0
        for prediction in seq.iterdir():
            disparity = load_disparity(prediction)
            assert disparity.shape == expected_disparity_shape, f'Expected shape:{expected_disparity_shape}, actual shape: {disparity.shape}'
            assert disparity.min() >= 0, disparity.min()
            num_files += 1
        assert seq.name in [*name2num], f'{seq.name} not in {[*name2num]}'
        assert num_files == name2num[seq.name], f'expected {name2num[seq.name]} files in {str(seq)} but only found {num_files} files'

    print('Your submission directory has the correct structure: Ready to submit!\n')
    print('Note, that we will sort the files according to their names in each directory and evaluate them sequentially. Follow the exact naming instructions if you are unsure.')
