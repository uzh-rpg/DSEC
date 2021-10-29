# DSEC

<p align="center">
   <img src="http://rpg.ifi.uzh.ch/img/datasets/dsec/setup_description.png" height="225"/>
   <img src="http://rpg.ifi.uzh.ch/img/datasets/dsec/dataset_example.png" height="225"/>
</p>

DSEC is a hybrid stereo event camera and video camera dataset in driving scenarios.

Visit the [project webpage](https://dsec.ifi.uzh.ch/) to download the dataset.

If you use this code in an academic context, please cite the following work:

```bibtex
@InProceedings{Gehrig21ral,
  author  = {Mathias Gehrig and Willem Aarents and Daniel Gehrig and Davide Scaramuzza},
  title   = {DSEC: A Stereo Event Camera Dataset for Driving Scenarios},
  journal = {IEEE Robotics and Automation Letters},
  year    = {2021},
  doi     = {10.1109/LRA.2021.3068942}
}
```
and
```bibtex
@InProceedings{Gehrig3dv2021,
  author = {Mathias Gehrig and Mario Millh\"ausler and Daniel Gehrig and Davide Scaramuzza},
  title = {E-RAFT: Dense Optical Flow from Event Cameras},
  booktitle = {International Conference on 3D Vision (3DV)},
  year = {2021}
}
```

## Install

In this repository we provide code for loading data and verifying the submission for the benchmarks. For details regarding the dataset, visit the [DSEC webpage](https://dsec.ifi.uzh.ch/).

1. Clone

```bash
git clone git@github.com:uzh-rpg/DSEC.git
```

2. Install conda environment to run example code
```bash
conda create -n dsec python=3.8
conda activate dsec
conda install -y -c anaconda numpy
conda install -y -c numba numba
conda install -y -c conda-forge h5py blosc-hdf5-plugin opencv scikit-video tqdm prettytable imageio
# only for dataset loading:
conda install -y -c pytorch pytorch torchvision cudatoolkit=10.2
# only for visualilzation in the dataset loading:
conda install -y -c conda-forge matplotlib
```

## Disparity Evaluation

We provide a [python script](scripts/check_disparity_submission.py) to ensure that the structure of the submission directory is correct.
Usage example:

```Python
python check_disparity_submission.py SUBMISSION_DIR EVAL_DISPARITY_TIMESTAMPS_DIR
```

where `EVAL_DISPARITY_TIMESTAMPS_DIR` is the path to the unzipped directory containing evaluation timestamps. It can [downloaded on the webpage](https://dsec.ifi.uzh.ch/dsec-datasets/download/) or directly [here](https://download.ifi.uzh.ch/rpg/DSEC/test_disparity_timestamps.zip).
`SUBMISSION_DIR` is the path to the directory containing your submission.

Follow the instructions on the [webpage](https://dsec.ifi.uzh.ch/disparity-submission-format/) for a detailed description of the submission format.

## Optical Flow Evaluation

We provide a [python script](scripts/check_optical_flow_submission.py) to ensure that the structure of the submission directory is correct.
Usage example:

```Python
python check_optical_flow_submission.py SUBMISSION_DIR EVAL_FLOW_TIMESTAMPS_DIR
```

where `EVAL_FLOW_TIMESTAMPS_DIR` is the path to the unzipped directory containing evaluation timestamps. It can [downloaded on the webpage](https://dsec.ifi.uzh.ch/dsec-datasets/download/) or directly [here](https://download.ifi.uzh.ch/rpg/DSEC/test_forward_optical_flow_timestamps.zip).
`SUBMISSION_DIR` is the path to the directory containing your submission.

Follow the instructions on the [webpage](https://dsec.ifi.uzh.ch/optical-flow-submission-format/) for a detailed description of the submission format.
