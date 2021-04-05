from pathlib import Path

import cv2
import numpy as np
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm

from dataset.provider import DatasetProvider
from dataset.visualization import disp_img_to_rgb_img, show_disp_overlay, show_image


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('dsec_dir', help='Path to DSEC dataset directory')
    parser.add_argument('--visualize', action='store_true', help='Visualize data')
    parser.add_argument('--overlay', action='store_true', help='If visualizing, overlay disparity and voxel grid image')
    args = parser.parse_args()

    visualize = args.visualize
    dsec_dir = Path(args.dsec_dir)
    assert dsec_dir.is_dir()

    dataset_provider = DatasetProvider(dsec_dir)
    train_dataset = dataset_provider.get_train_dataset()

    batch_size = 1
    num_workers = 0
    train_loader = DataLoader(
            dataset=train_dataset,
            batch_size=batch_size,
            shuffle=True,
            num_workers=num_workers,
            drop_last=False)
    with torch.no_grad():
        for data in tqdm(train_loader):
            if batch_size == 1 and visualize:
                disp = data['disparity_gt'].numpy().squeeze()
                disp_img = disp_img_to_rgb_img(disp)
                if args.overlay:
                    left_voxel_grid = data['representation']['left'].squeeze()
                    ev_img = torch.sum(left_voxel_grid, axis=0).numpy()
                    ev_img = (ev_img/ev_img.max()*256).astype('uint8')
                    show_disp_overlay(ev_img, disp_img, height=480, width=640)
                else:
                    show_image(disp_img)
