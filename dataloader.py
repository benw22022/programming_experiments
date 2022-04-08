import uproot
from typing import Dict, List, Tuple
import awkward as ak
import numpy as np

class DataLoader:

    def __init__(self, files: str, feature_dict: Dict[str, List[str]], batch_size: int=1024, is_jet: bool=False) -> None:
        self.files = files
        self.features = feature_dict
        self.features_list = [item for sublist in feature_dict.items() for item in sublist]
        self.batch_size = batch_size
        self.is_jet = is_jet
    
        self.lazy_array = uproot.lazy(self.files, filter_name=self.features_list, step_size="50 MB")

    def __getitem__(self, idx) -> Tuple:

        batch = self.lazy_array[idx * self.batch_size: (idx  + 1) * self.batch_size]

        tracks = ak.unzip(batch[self.features["TauTracks"]])
        tracks = np.stack([ak.to_numpy(ak.pad_none(arr, 3, clip=True)) for arr in tracks], axis=1).filled(0)  

        neutral_pfo = ak.unzip(batch[self.features["NeutralPFO"]])
        neutral_pfo = np.stack([ak.to_numpy(ak.pad_none(arr, 6, clip=True)) for arr in neutral_pfo], axis=1).filled(0)    

        shot_pfo = ak.unzip(batch[self.features["ShotPFO"]])
        shot_pfo = np.stack([ak.to_numpy(ak.pad_none(arr, 8, clip=True)) for arr in shot_pfo], axis=1).filled(0)      
        
        conv_tracks = ak.unzip(batch[self.features["ConvTrack"]])
        conv_tracks = np.stack([ak.to_numpy(ak.pad_none(arr, 4, clip=True)) for arr in conv_tracks], axis=1).filled(0)         

        jets = ak.unzip(batch[self.features["TauJets"]])
        jets = np.stack([ak.to_numpy(arr) for arr in jets], axis=1)     

        decay_mode = ak.to_numpy(batch["TauJets_truthDecayMode"])
        labels = np.zeros((len(decay_mode), 6))  
        for i, dm in enumerate(decay_mode):
            labels[i][dm] += 1
        
        weights = ak.to_numpy(batch["TauJets.mcEventWeight"])

        return ((tracks, neutral_pfo, shot_pfo, conv_tracks, jets), labels, weights)

    def __len__(self) -> int:
        return len(self.lazy_array)
