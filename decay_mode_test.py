import ROOT
import tensorflow as tf
import numpy as np
from models import TestModel


if __name__ == "__main__":

    files = "/mnt/c/Users/benwi/NTuples/user.bewilson.TauClassifierV3.425200.Pythia8EvtGen_A14NNPDF23LO_Gammatautau_MassWeight_v0_output.root/*.root"
    df = ROOT.RDataFrame("tree", files)
    df_1p0n = df.Filter("TauJets.truthDecayMode == 0")
    df_1p1n = df.Filter("TauJets.truthDecayMode == 1")
    df_1pXn = df.Filter("TauJets.truthDecayMode == 2")
    df_3p0n = df.Filter("TauJets.truthDecayMode == 3")
    df_3pXn = df.Filter("TauJets.truthDecayMode == 4")

    columns = df.GetColumnNames()
    track_variables = []
    for val in columns:
        if "TauTrack" in str(val):
            track_variables.append(val)

    nevents = df.Count().GetValue()


    model = TestModel()
    opt = tf.keras.optimizers.Adam()
    model.compile(optimizer=opt, loss="sparse_categorical_crossentropy", metrics=[tf.keras.metrics.CategoricalAccuracy()])

    pos = 0
    batch_size = 32
    it = 0
    while pos < nevents:
        it += 1
        print(it)
        batch_df = df.Range(pos, pos + batch_size)
        pos += batch_size
        
        features_dict = batch_df.AsNumpy(track_variables)
        tensors = []

        for key, value in features_dict.items():
            tensors.append(tf.ragged.constant(value).to_tensor(default_value=0, shape=(None, 3)))
            # tensors.append(tf.ragged.constant(value))

        x_batch = tf.stack(tensors, axis=1)

        y_batch = batch_df.AsNumpy(["TauJets.truthDecayMode"])["TauJets.truthDecayMode"]

        print(x_batch)

        model.fit(x_batch, y_batch)

        break
    


    # arr = df.AsNumpy(["TauTracks.pt"])

    # t = tf.ragged.constant(arr["TauTracks.pt"]).to_tensor())

    # print(t)