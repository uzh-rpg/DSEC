# Visualization Tools

## Visualize Event Data

Event data is provided in hdf5 format. The visualization tools can be used to query this data and visualize it in video format. Have a look at the scripts to see how event data can be efficiently queried.

To visualize event data in video format use the following script:

```bash
delta_t=50
python events2video.py path/to/events.h5 path/to/output.mp4 --delta_time_ms $delta_t
```

This will generate a video by generating event frames of 50 milliseconds of duration.
