import ROOT
import tensorflow as tf
import numpy as np

if __name__ == "__main__":

    file = "/mnt/c/Users/benwi/NTuples/user.bewilson.TauClassifierV3.425200.Pythia8EvtGen_A14NNPDF23LO_Gammatautau_MassWeight_v0_output.root/*.root"
    df = ROOT.RDataFrame("tree", file)#.Range(10)

    stats = df.Mean("TauTracks.pt")

    stats = stats.GetValue()

    print(stats)

    print(np.linspace(0, 5) * 100)

    # arr = df.AsNumpy(["TauTracks.pt"])



    # t = tf.ragged.constant(arr["TauTracks.pt"]).to_tensor())

    # print(t)