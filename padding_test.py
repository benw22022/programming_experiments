import ROOT
import tensorflow as tf
import numpy as np
from models import TestModel
import numba as nb
import sys
import tqdm
import math

# ROOT.ROOT.EnableImplicitMT()

@nb.njit
def stack(arr):
    return np.stack(arr)

@nb.njit
def convert(data):
    return np.vectorize(np.asarray, signature='()->(n)')(data)

ROOT.gInterpreter.Declare('''
template<typename T>
ROOT::RVec<T> ApplyPadding(const ROOT::RVec<T>& x, size_t max_size, const T& pad)
{
    ROOT::RVec<T> padded = x;
    padded.resize(max_size, pad);
    return padded;
}
''')


if __name__ == "__main__":

    
    files = "../NTuples/user.bewilson.TauClassifierV3.425200.Pythia8EvtGen_A14NNPDF23LO_Gammatautau_MassWeight_v0_output.root/*.root"
    df_full = ROOT.RDataFrame("tree", files)
    columns = ["TauTracks.nInnermostPixelHits",
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
    padded_columns = [f"{c}_padded".replace(".", "_") for c in columns]

    max_n_tracks = 3
    for column, padded_column in zip(columns, padded_columns):
            df_full = df_full.Define(padded_column, 'ApplyPadding({}, {}, 0.f)'.format(column, max_n_tracks))

    nevents = df_full.Count().GetValue()
    pos = 0
    batch_size = 10000
    it = 0
    for _ in tqdm.tqdm(range(0, math.ceil(nevents / batch_size))):
        it += 1
        df = df_full.Range(pos, pos + batch_size)
        pos += batch_size

        data = df.AsNumpy(columns=padded_columns)
        batch = np.vstack([np.asarray(data[var]) for var in padded_columns]).T
        batch = np.vectorize(np.asarray, signature='()->(n)')(batch)