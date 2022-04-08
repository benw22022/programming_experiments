
import uproot
import awkward as ak
import tensorflow as tf
import glob
import numpy as np
import tqdm
from variables import variable_handler

if __name__ == "__main__":

    # files = glob.glob("../NTuples/*/*.root")

    j = 0
    batch_size = "35 MB"
    small_batch_size = 64
    # nevents = len(uproot.lazy("TestFile.root", filter_name="TauJets_mu")) // batch_size
    # for big_array in tqdm.tqdm(uproot.iterate("TestFile.root", library='ak', filter_name=variable_handler.list(padded=False), step_size=batch_size), total=nevents):
    for big_array in uproot.iterate("TestFile.root", library='ak', filter_name=variable_handler.list(padded=False), step_size=batch_size):
        
        pos = 0
        for i in tqdm.tqdm(range(0, len(big_array)//small_batch_size)):
            array = big_array[pos: pos + small_batch_size]
            pos += small_batch_size

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

        # print(labels)
        # break

        j += 1
        print(j)