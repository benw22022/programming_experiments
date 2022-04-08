import ROOT
import tensorflow as tf
import numpy as np
from models import TestModel
import numba as nb
import modin.pandas as pd
import ray
ray.init()


# ROOT.ROOT.EnableImplicitMT()

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

    
    files = "/mnt/c/Users/benwi/NTuples/user.bewilson.TauClassifierV3.425200.Pythia8EvtGen_A14NNPDF23LO_Gammatautau_MassWeight_v0_output.root/*.root"
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
    batch_size = 32

    for i in range(0, nevents):
    
        col_dict = df_full.Range(i*batch_size, i*batch_size + batch_size).AsNumpy(padded_columns)

        df = pd.DataFrame(col_dict)

        print(i)