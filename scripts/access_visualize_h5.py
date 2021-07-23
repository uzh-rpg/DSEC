#!/usr/bin/env python3

import argparse
from tqdm import tqdm
from pathlib import Path
import h5py
from visualization.eventreader import EventReader
from utils.eventslicer import EventSlicer
import matplotlib.pyplot as plt
import numpy as np

def main():
    """Example reading of h5 events.
    EventReader and EventSlicer are python classes from the DSEC code base (https://github.com/uzh-rpg/DSEC).
    Publication of the DSEC datset can be found under (https://dsec.ifi.uzh.ch/):
        Mathias Gehrig, Willem Aarents, Daniel Gehrig and Davide Scaramuzza (2021).
        DSEC: A Stereo Event Camera Dataset for Driving Scenarios. IEEE Robotics and Automation Letters.
    """

    parser = argparse.ArgumentParser(description="Reading a h5 event file")
    parser.add_argument("--event_file", help="Folder with h5 file format. Events in 'events' are of type (x, y, t, p)"
                        "ms_to_idx is same as in DSEC file format, which allows accessing event chunks using time index",
                        # default="/home/simon/data/DSEC/interlaken_00_c_events_left/events.h5")
                        default="/home/simon/data/TUM-VIE/mocap_trans/events_sync/events_right.h5")

    args = parser.parse_args()
    rawfile = Path(args.event_file)
    h5file = h5py.File(rawfile)
    print(h5file.keys())
    events = h5file['events']
    print("Contains %d events" % (events['t'].shape[0]))
    print("Event duration is %.2f seconds" % ((events['t'][-1] - events['t'][0])*1e-6))

    # Option1: Add your custom code here
    """
        Custom Code
    """

    # Option2: Alternatively, you can use the code from DSEC´s event data tool,
    # which for example allows to use an EventReader object for reading chunk-by-chunk
    dt_ms = 100
    for evs in tqdm(EventReader(rawfile, dt_ms)):
        print(evs.keys)
        print(evs['t'].shape)
        break

    # DSEC´s tools also allow to use an EventSlicer object for reading in specific time interval
    slicer = EventSlicer(h5file)
    # get exemplary event batch between (15ms, 35ms)
    evs = slicer.get_events(15e3, 35e3)

    # Visualize the event batch as accumulated event image
    plt.figure()
    ev_arr = np.stack([evs['x'], evs['y'], evs['t'], evs['p']], axis=1)
    pos = ev_arr[np.where(ev_arr[:, 3] == 0)]
    neg = ev_arr[np.where(ev_arr[:, 3] == 1)]
    plt.scatter(pos[:, 0], pos[:, 1], color="blue", s=0.7)
    plt.scatter(neg[:, 0], neg[:, 1], color="red", s=0.7)
    plt.xlim(0, 1280)
    plt.ylim(0, 720)
    plt.gca().invert_yaxis()
    

if __name__ == '__main__':
    main()
