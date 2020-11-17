# DSEC

<p align="center">
   <img src="http://rpg.ifi.uzh.ch/img/datasets/dsec/setup_description.png" width="400"/>
   <img src="http://rpg.ifi.uzh.ch/img/datasets/dsec/dataset_example.png" width="400"/>
</p>

DSEC is a hybrid stereo event camera and video camera dataset in driving scenarios.

**Under Construction**

This repository currently contains links to *raw data* of a subset of the DSEC dataset.
The full dataset will be made available upon publication of the dataset.

## Download Raw Data

Raw data of the sequences 00000 to 00020 are currently available.

### Image Data

Each 7z archive contains 8bit debayered images at 20 Hz. "left" or "right" refers to the left or right video camera of the stereo pair.

```bash
SEQ=00000 # or 00001, ..., 00020
LOCATION=left # or 'right'
wget "http://rpg.ifi.uzh.ch/datasets/DSEC/$SEQ/images/$LOCATION/debayer8bit.7z"
```

### Event Data

Each file contains raw event data in HDF5 format. "left" or "right" refers to the left or right event camera of the stereo pair.

```bash
SEQ=00000 # or 00001, ..., 00020
LOCATION=left # or 'right'
wget "http://rpg.ifi.uzh.ch/datasets/DSEC/$SEQ/events/$LOCATION/events.h5"
```

### Lidar Data

Each file contains lidar scan data in rosbag format. The raw scan data is saved in the `/velodyne_packets` topic of the bag.

```bash
SEQ=00000 # or 00001, ..., 00020
wget "http://rpg.ifi.uzh.ch/datasets/DSEC/$SEQ/lidar/velodyne.bag"
```

## Install

1. Clone

```bash
git clone git@github.com:uzh-rpg/DSEC.git
```

2. Install conda environment
```bash
conda create -n dsec python=3.8
conda activate dsec
conda install -y -c numba numba
conda install -y -c conda-forge h5py numpy pytables scikit-video tqdm
```

## Script Overview
- [Visualization of events](scripts/visualization/README.md)
