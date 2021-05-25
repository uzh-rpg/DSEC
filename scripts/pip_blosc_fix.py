import os

# Load hdf5plugin first
import hdf5plugin
# Direct h5py to the new plugin directory
os.environ["HDF5_PLUGIN_PATH"] = hdf5plugin.PLUGINS_PATH
# When h5py loads, it will scrape the new plugin directory
import h5py

f = h5py.File("/Datasets/DSEC/train_split/interlaken_00_c/events/left/events.h5")

x = f['events/x'][:1000]
