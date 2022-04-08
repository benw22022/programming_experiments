import ROOT
import tensorflow as tf
import numpy as np
from models import TestModel
import numba as nb
import sys
import glob

ROOT.ROOT.EnableImplicitMT()
ROOT.gInterpreter.Declare('''
template<typename T>
size_t MaxObjs(const ROOT::RVec<T>& x)
{
    return x.size();
}
''')



if __name__ == "__main__":

    
    files = glob.glob("../NTuples/*/*.root")

    df = ROOT.RDataFrame("tree", files)
    df = df.Define("nTauTracks", "MaxObjs(TauTracks.pt)")
    df = df.Define("nNeutralPFO", "MaxObjs(NeutralPFO.pt)")
    df = df.Define("nShotPFO", "MaxObjs(ShotPFO.pt)")
    df = df.Define("nConvTrack", "MaxObjs(ConvTrack.pt)")

    max_tracks = int(df.Max('nTauTracks').GetValue())
    print(f"Max Tracks = {max_tracks}")

    max_neutral_pfo = int(df.Max('nNeutralPFO').GetValue())
    print(f"Max NeutralPFOs = {max_neutral_pfo}")

    max_shot_pfo = int(df.Max('nShotPFO').GetValue())
    print(f"Max ShotPFOs = {max_shot_pfo}")

    max_conv_tracks = int(df.Max('nConvTrack').GetValue())
    print(f"Max ConvTracks = {max_conv_tracks}")

    