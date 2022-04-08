import uproot
import awkward as ak
import tensorflow as tf
import glob
import numpy as np
import tqdm
import cupy as cp
import time


if __name__ == "__main__":

    print(cp.get_default_memory_pool())  
  
    # # NumPy and CPU Runtime
    # s = time.time()
    # x_cpu = np.ones((1000, 1000, 100))
    # e = time.time()
    # print("Time consumed by numpy: ", e - s)
    
    # # CuPy and GPU Runtime
    # s = time.time()
    # x_gpu = cp.ones((1000, 1000, 100))
    # e = time.time()
    # print("\nTime consumed by cupy: ", e - s)


    # files = glob.glob("../NTuples/*/*.root")

    # columns = ["TauTracks.nInnermostPixelHits",
    # "TauTracks.nPixelHits", 
    # "TauTracks.nSCTHits",
    # "TauTracks.chargedScoreRNN", 
    # "TauTracks.isolationScoreRNN",
    # "TauTracks.conversionScoreRNN",
    # "TauTracks.pt",
    # "TauTracks.dphiECal",
    # "TauTracks.detaECal",
    # "TauTracks.jetpt",
    # "TauTracks.d0TJVA",
    # "TauTracks.d0SigTJVA",
    # "TauTracks.z0sinthetaTJVA", 
    # ]

    # j = 0
    # nevents = len(uproot.lazy(files, filter_name="TauJets.mu"))
    # for array in tqdm.tqdm(uproot.iterate(files, library='ak', filter_name=columns, step_size=32), total=nevents):
    #     print(array)
        # array = ak.unzip(array)
        # a = np.stack([ak.to_numpy(ak.pad_none(arr, 3, clip=True)) for arr in array], axis=1)    
        # j += 1