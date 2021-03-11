# DSEC

<p align="center">
   <img src="http://rpg.ifi.uzh.ch/img/datasets/dsec/setup_description.png" width="400"/>
   <img src="http://rpg.ifi.uzh.ch/img/datasets/dsec/dataset_example.png" width="400"/>
</p>

DSEC is a hybrid stereo event camera and video camera dataset in driving scenarios.

Visit the [project webpage](http://rpg.ifi.uzh.ch/dsec.html) to download the dataset.

**Announcements**
- 11.03.2021: The dataset is now public on <http://rpg.ifi.uzh.ch/dsec.html>. Simplified download instructions will be made available in the upcoming days.

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
