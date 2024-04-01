from esinet import util
from esinet.simulation import Simulation
from esinet.net import Net
import os
import mne
import numpy as np
from copy import deepcopy
import sys
import pytz

if __name__ == '__main__':
    plot_params = dict(surface='white', hemi='both', verbose=0)
    subjects_dir = os.path.join(mne.datasets.sample.data_path(), 'subjects')
    mne.set_config('SUBJECTS_DIR', subjects_dir)

    #加载数据
    data_path = mne.datasets.sample.data_path()
    raw_fname = os.path.join(data_path, 'MEG', 'sample',
                             'sample_audvis_filt-0-40_raw.fif')

    raw = mne.io.read_raw_fif(raw_fname, verbose=0)  # already has an average reference
    events = mne.find_events(raw, stim_channel='STI 014', verbose=0)

    event_id = dict(aud_l=1)  # event trigger and conditions
    tmin = -0.2  # start of each epoch (200ms before the trigger)
    tmax = 0.5  # end of each epoch (500ms after the trigger)
    raw.info['bads'] = ['MEG 2443', 'EEG 053']
    baseline = (None, 0)  # means from the first instant to t = 0
    reject = dict(grad=4000e-13, mag=4e-12, eog=150e-6)

    epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True,
                        picks=('meg', 'eog'), baseline=baseline, reject=reject,
                        verbose=0)

    fname_fwd = data_path + '/MEG/sample/sample_audvis-meg-oct-6-fwd.fif'
    fwd = mne.read_forward_solution(fname_fwd, verbose=0)

    epochs_stripped = epochs.copy().load_data().pick_types(meg='mag')
    fwd = fwd.pick_channels(epochs_stripped.ch_names)
    fwd = mne.convert_forward_solution(fwd, surf_ori=True, force_fixed=True,
                                       use_cps=True, verbose=0)

    #将样本数据可视化
    epochs_stripped.average().plot_joint()

    #计算来源
