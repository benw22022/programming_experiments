
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
    batch_size = 2048
    nevents = len(uproot.lazy(file, filter_name="TauJets_mu")) // batch_size

    track_vars = variable_handler.get("TauTracks", names_only=True)
    neutral_pfo_vars = variable_handler.get("NeutralPFO", names_only=True)
    shot_pfo_vars = variable_handler.get("ShotPFO", names_only=True)
    conv_track_vars = variable_handler.get("ConvTrack", names_only=True)
    jet_vars = variable_handler.get("TauJets", names_only=True)
    

    for array in tqdm.tqdm(uproot.iterate(file, library='pd', filter_name=variable_handler.list(), step_size=batch_size), total=nevents):
        
        
        # tracks = np.stack([array[v] for v in track_vars], axis=1)  
        # neutral_pfo = np.stack([array[v] for v in neutral_pfo_vars], axis=1)  
        # shot_pfo = np.stack([array[v] for v in shot_pfo_vars], axis=1)  
        # conv_track = np.stack([array[v] for v in conv_track_vars], axis=1)  
        # jets = np.stack([array[v] for v in jet_vars], axis=1)
    
        # labels = array["TauClassifier_Labels"]

        j += 1