from calendar import c
from pyrsistent import v
import ROOT
import glob
import numpy as np
snapshotOptions = ROOT.RDF.RSnapshotOptions()
snapshotOptions.RECREATE = True #only setting fLazy here, for other options see https://root.cern/doc/master/structROOT_1_1RDF_1_1RSnapshotOptions.html

ROOT.EnableImplicitMT()

# ApplyPadding Function C++ Definition
ROOT.gInterpreter.Declare('''
template<typename T>
ROOT::RVec<T> ApplyPadding(const ROOT::RVec<T>& x, size_t max_size, const T& pad)
{
    ROOT::RVec<T> padded = x;
    padded.resize(max_size, pad);
    return padded;
}
''')

ROOT.gInterpreter.Declare('''
ROOT::RVec<int> GenerateLabels(const int& decay_mode, const bool& is_jet)
{
    ROOT::RVec<int> label = {0, 0, 0, 0, 0, 0};
    if(is_jet == true){
        label[0] = 1;
    }
    else{
        label[decay_mode + 1] = 1;
    }
    return label;
}
''')


def pad_columns(df, columns, pad_length, default_value=0):

    padded_columns = [f"{c}_padded".replace(".", "_") for c in columns]
    for column, padded_column in zip(columns, padded_columns):
        print(f"padding_column: {column}")
        df = df.Define(padded_column, f'ApplyPadding({column}, {pad_length}, {default_value}.f)')

    return df



def process_ntuple(file, is_jet=False):

    df = ROOT.RDataFrame("tree", file)

    columns = df.GetColumnNames()
    track_variables = []
    neutral_pfo_variables = []
    shot_pfo_variables = []
    conv_track_variables = []
    for val in columns:
        if "TauTrack" in str(val):
            track_variables.append(val)
        elif "NeutralPFO" in str(val):
            neutral_pfo_variables.append(val)
        elif "ShotPFO" in str(val):
            shot_pfo_variables.append(val)
        elif "ConvTrack" in str(val):
            conv_track_variables.append(val)

    df = pad_columns(df, track_variables, 3)
    df = pad_columns(df, neutral_pfo_variables, 6)
    df = pad_columns(df, shot_pfo_variables, 8)
    df = pad_columns(df, conv_track_variables, 4)

    df = df.Define("TauClassifier_Labels", f"GenerateLabels(TauJets.truthDecayMode, {str(is_jet).lower()})")

    df.Snapshot("tree", "TestFile.root", "", snapshotOptions)
    return df


if __name__ == "__main__":

    jet_files = glob.glob("/home/bewilson/NTuples/*JZ*/*.root")
    tau_files = glob.glob("/home/bewilson/NTuples/*Gammatautau*/*.root")

    process_ntuple(tau_files[2])

    # for file in jet_files:
    #     process_ntuple(file)
    # for file in tau_files:
    #     process_ntuple(file)