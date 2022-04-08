
import ROOT
import tensorflow as tf
import numpy as np
import modin.pandas as pd
import ray
ray.init()

ROOT.gInterpreter.Declare('''
template<typename T>
ROOT::RVec<T> ApplyPadding(const ROOT::RVec<T>& x, size_t max_size, const T& pad)
{
    ROOT::RVec<T> padded = x;
    padded.resize(max_size, pad);
    return padded;
}
''')

@tf.function
def to_tensor(value):
    tf.ragged.constant(value).to_tensor(default_value=0, shape=(None, 3))


class Generator(tf.keras.utils.Sequence):

    def __init__(self, file_list, batch_size=32):

        self.df = ROOT.RDataFrame("tree", file_list)
        self.length = self.df.Count().GetValue()
        self.batch_size = batch_size
        self.pos = 0
        self.columns = ["TauTracks.nInnermostPixelHits",
        "TauTracks.nPixelHits", 
        "TauTracks.nSCTHits",
        "TauTracks.chargedScoreRNN", 
        "TauTracks.isolationScoreRNN",
        "TauTracks.conversionScoreRNN",
        "TauTracks.pt",
        "TauTracks.dphiECal",
        "TauTracks.detaECal",
        "TauTracks.jetpt",
        "TauTracks.d0TJVA",
        "TauTracks.d0SigTJVA",
        "TauTracks.z0sinthetaTJVA",
        "TauTracks.z0sinthetaSigTJVA", ]    
        self.padded_columns = [f"{c}_padded".replace(".", "_") for c in self.columns]

        max_n_tracks = 3
        for column, padded_column in zip(self.columns, self.padded_columns):
                self.df = self.df.Define(padded_column, 'ApplyPadding({}, {}, 0.f)'.format(column, max_n_tracks))

    def __getitem__(self, idx):
        batch_df = self.df.Range(idx*self.batch_size, idx*self.batch_size + self.batch_size)
        col_dict = batch_df.AsNumpy(self.padded_columns)
        y_batch = batch_df.AsNumpy(["TauJets.truthDecayMode"])["TauJets.truthDecayMode"]
        return pd.DataFrame(col_dict), y_batch
    

    # def __getitem__(self, idx):
    #     batch_df = self.df.Range(idx, idx + self.batch_size)
    #     self.pos += self.batch_size
        
    #     features_dict = batch_df.AsNumpy(self.track_variables)
    #     tensors = []

    #     for key, value in features_dict.items():
    #         tensors.append(np.asarray(value))

    #     x_batch = np.stack(tensors, axis=1)

    #     y_batch = batch_df.AsNumpy(["TauJets.truthDecayMode"])["TauJets.truthDecayMode"]

    #     return x_batch, y_batch

    def on_epoch_end(self):
        self.pos = 0

    def __len__(self):
        return self.length
