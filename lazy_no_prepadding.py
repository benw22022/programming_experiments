
import uproot
import awkward as ak
import tensorflow as tf
import glob
import numpy as np
import tqdm
from variables import variable_handler
import numba as nb

@nb.njit
def stack(arrays):
    return np.stack(arrays, axis=1)


if __name__ == "__main__":

    file = "TestFile.root"

    j = 0
    batch_size = 64
    nevents = len(uproot.lazy(file, filter_name="TauJets_mu")) // batch_size

    track_vars = variable_handler.get("TauTracks", names_only=True)
    neutral_pfo_vars = variable_handler.get("NeutralPFO", names_only=True)
    shot_pfo_vars = variable_handler.get("ShotPFO", names_only=True)
    conv_track_vars = variable_handler.get("ConvTrack", names_only=True)
    jet_vars = variable_handler.get("TauJets", names_only=True)

    lazy_array = uproot.lazy(file, filter_name=variable_handler.list(padded=False), step_size="25 MB")
    pos = 0
    for array in tqdm.tqdm(range(0, nevents)):
        
        array = lazy_array[pos: pos + batch_size]
        pos += batch_size

        tracks = ak.unzip(array[variable_handler.get("TauTracks", names_only=True, padded=False)])
        tracks = np.stack([ak.to_numpy(ak.pad_none(arr, 3, clip=True)) for arr in tracks], axis=1).filled(0)  

        neutral_pfo = ak.unzip(array[variable_handler.get("NeutralPFO", names_only=True, padded=False)])
        neutral_pfo = np.stack([ak.to_numpy(ak.pad_none(arr, 6, clip=True)) for arr in neutral_pfo], axis=1).filled(0)    

        shot_pfo = ak.unzip(array[variable_handler.get("ShotPFO", names_only=True, padded=False)])
        shot_pfo = np.stack([ak.to_numpy(ak.pad_none(arr, 8, clip=True)) for arr in shot_pfo], axis=1).filled(0)      
        
        conv_tracks = ak.unzip(array[variable_handler.get("ConvTrack", names_only=True, padded=False)])
        conv_tracks = np.stack([ak.to_numpy(ak.pad_none(arr, 4, clip=True)) for arr in conv_tracks], axis=1).filled(0)         

        jets = ak.unzip(array[variable_handler.get("TauJets", names_only=True, padded=False)])
        jets = np.stack([ak.to_numpy(arr) for arr in jets], axis=1)     

        decay_mode = ak.to_numpy(array["TauJets_truthDecayMode"])
        labels = np.zeros((len(decay_mode), 6))  
        for i, dm in enumerate(decay_mode):
            labels[i][dm] += 1
        j += 1