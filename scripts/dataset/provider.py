from pathlib import Path

import torch

from dataset.sequence import Sequence

class DatasetProvider:
    def __init__(self, dataset_path: Path, delta_t_ms: int=50, num_bins=15):
        train_path = dataset_path / 'train'
        assert dataset_path.is_dir(), str(dataset_path)
        assert train_path.is_dir(), str(train_path)

        train_sequences = list()
        for child in train_path.iterdir():
            train_sequences.append(Sequence(child, 'train', delta_t_ms, num_bins))

        self.train_dataset = torch.utils.data.ConcatDataset(train_sequences)

    def get_train_dataset(self):
        return self.train_dataset

    def get_val_dataset(self):
        # Implement this according to your needs.
        raise NotImplementedError

    def get_test_dataset(self):
        # Implement this according to your needs.
        raise NotImplementedError
