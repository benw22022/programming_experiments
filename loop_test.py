import ROOT
import tensorflow as tf
import numpy as np
from models import TestModel
import numba as nb

@nb.njit
def stack_arrays(features_dict):
    tensors = []
    # pad = lambda a,i : a[0:i] if len(a) > i else a + [0] * (i-len(a))
    pad = lambda a, i: a[0: i] if a.shape[0] > i else np.hstack((a, np.zeros(i - a.shape[0])))
    for value in features_dict:
        rows = []
        for row in value:
            rows.append(pad(np.array(row), 3).astype("float32"))     
        values = np.concatenate([r for r in rows])
        # tensors.append(tf.RaggedTensor.from_row_limits(values=values, row_limits=row_lengths))
        # tensors.append(tf.constant(rows))
        tensors.append(rows)

        # x_batch = tf.stack(tensors, axis=1)
        return np.stack(tensors, axis=1)

@nb.njit
def pad_row(row, pad_len=3):
    # pad = lambda a, i: a[0: i] if a.shape[0] > i else np.hstack((a, np.zeros(i - a.shape[0])))
    padded_row = np.zeros(pad_len)
    index = 0
    while index < pad_len and index < len(row):
        padded_row[index] = row[index]
        index +=1 
    return padded_row

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

    padded_columns = [f"{c}_padded".replace(".", "_") for c in track_variables]
    
    # model = TestModel()
    # opt = tf.keras.optimizers.Adam()
    # model.compile(optimizer=opt, loss="sparse_categorical_crossentropy", metrics=[tf.keras.metrics.CategoricalAccuracy()])

    pos = 0
    batch_size = 32
    it = 0
    while pos < nevents:
        it += 1
        print(it)
        batch_df = df.Range(pos, pos + batch_size)
        for c, pc in zip(track_variables, padded_columns):
            batch_df = batch_df.Define(pc, 'ApplyPadding({}, {}, 0.f)'.format(c, 3))

        pos += batch_size
        
        data = batch_df.AsNumpy(padded_columns)
        x_batch = np.concatenate([np.asarray(data[e]) for e in data], axis=1)
        # for e in data:
        #     print(data[e])
        #     print("\n")

        print(x_batch)

        y_batch = batch_df.AsNumpy(["TauJets.truthDecayMode"])["TauJets.truthDecayMode"]

        break

        # print(x_batch)

        # model.fit(x_batch, y_batch)

        # break
    


    # arr = df.AsNumpy(["TauTracks.pt"])

    # t = tf.ragged.constant(arr["TauTracks.pt"]).to_tensor())

    # print(t)