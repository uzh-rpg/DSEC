# DSEC

<p align="center">
   <img src="http://rpg.ifi.uzh.ch/img/datasets/dsec/setup_description.png" height="230"/>
   <img src="http://rpg.ifi.uzh.ch/img/datasets/dsec/dataset_example.png" height="230"/>
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

## Install

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
conda install -y -c conda-forge h5py blosc-hdf5-plugin opencv scikit-video tqdm prettytable
# only for dataset loading:
conda install -y -c pytorch pytorch torchvision cudatoolkit=10.2
# only for visualilzation in the dataset loading:
conda install -y -c conda-forge matplotlib
```

## Data Format
The disparity groundtruth is provided in the rectified coordinate frames of the left cameras.

### Disparity

Disparity maps are saved as uint16 PNG files. We provide example python code in the dataset directory for convenience.

A value of 0 indicates an invalid pixel where no groundtruth exists.
Otherwise, disparity of valid pixels can be computed by converting the uint16 value to float and dividing it by 256:

```
disp[y,x]  = ((float)I[y,x])/256.0;
valid[y,x] = I[y,x]>0;
```

The reference view is the left event or rgb global shutter camera respectively. This is the same convention as the KITTI stereo benchmark.

### Image
Image data is available in 8-bit PNG files at a resolution of 1440x1080 and is already rectified.

Together with the images, we provide three timestamp files:
- Exposure timestamps for both left and right camera: The start and end of the exposure time is provided in microseconds
- Image timestamps: They are unified timestamps for both the left and right cameras and are computed as the average of the middle exposures from the left and right cameras. These timestamps are used to associate images with disparity maps.

### Events
Event data is stored at VGA resolution (640x480) in compressed h5 files. The structure of the h5 file is the following:

```
/events/p
/events/t
/events/x
/events/y
/ms_to_idx
/t_offset
```

- `/events/{p, t, x, y}` contains the polarity, time, x (column idx), and y (row idx) coordinates. The time is in microseconds.
- `/t_offset` is the time offset in microseconds that must be added to `events/t` to retrieve the time in synchronization with image data, disparity data, and events from the other camera. This offset enables the storage of timestamp data with fewer bits.
- `/ms_to_idx` is the mapping from milliseconds to event indices. It is used to efficiently retrieve event data within a time duration.  It is defined such that
  - `t[ms_to_idx[ms]] >= ms*1000`
  - `t[ms_to_idx[ms] - 1] < ms*1000`,

  where `ms` is the time in milliseconds and `t` the event timestamps in microseconds. We provide [python code](scripts/utils/eventslicer.py) that can be used to retrieve event data.

#### Rectification
Unlike image data, event data is not rectified or undistorted to simplify data storage.
Rectified and undistorted event data can be computed using the `rectify_maps.h5` file that is associated with each event h5 file.
We provide example python code in the dataset directory for convenience.

The event data stored in the `events.h5` file contains pixel coordinates as recorded by the sensor.
Hence, this data is subject to lens distortion and not yet rectified.
`rectify_map` contains the rectified pixel coordinates:

```
rectified_coordinates = rectify_map[y, x]
x_rectified = rectified_coordinates[..., 0]
y_rectified = rectified_coordinates[..., 1]
```
### Camera Calibration File
Camera calibration data is summarized in the `cam_to_cam.yaml`. The naming convention is as follows:

#### Intrinsics
- `cam0`: Event camera left
- `cam1`: Frame camera left
- `cam2`: Frame camera right
- `cam3`: Event camera right
- `camRectX` Rectified version of camX. E.g. camRect0 is the rectified version of cam0.

#### Extrinsics
- `T_XY`: Rigid transformation that transforms a point in the camY coordinate frame into the camX coordinate frame.
- `R_rectX`: Rotation that transforms a point in the camX coordinate frame into the camRectX coordinate frame.

#### Disparity to Depth
The following two quantities are perspective transformation matrices for [reprojecting a disparity image to 3D space](https://docs.opencv.org/4.5.2/d9/d0c/group__calib3d.html#ga1bc1152bd57d63bc524204f21fde6e02).
- `cams_03`: Event cameras
- `cams_12`: Frame cameras

## Disparity Evaluation

We provide a [python script](scripts/check_submission.py) to ensure that the structure of the submission directory is correct.
Usage example:

```Python
python check_submission.py SUBMISSION_DIR EVAL_DISPARITY_TIMESTAMPS_DIR
```

where `EVAL_DISPARITY_TIMESTAMPS_DIR` is the path to the unzipped directory containing evaluation timestamps. It can [downloaded on the webpage](https://dsec.ifi.uzh.ch/dsec-datasets/download/) or directly [here](https://download.ifi.uzh.ch/rpg/DSEC/test_disparity_timestamps.zip).
`SUBMISSION_DIR` is the path to the directory containing your submission.

Follow the instructions on the [webpage](https://dsec.ifi.uzh.ch/disparity-submission-format/) for a detailed description of the submission format.
