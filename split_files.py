"""
Split Root Files
________________________________________________________________
Split root files into uniform length files for more reliable 
train/test/val split
"""


import ROOT
import glob
import os
import tqdm
import math

def split_files(infiles, outdir, outfile_tmplt, events_per_file=100000, treename="tree"):

    df = ROOT.RDataFrame("tree", infiles)
    nevents = df.Count().GetValue()

    try:
        os.mkdir(outdir)
    except OSError:
        pass

    pos = 0
    for i in tqdm.tqdm(range(0, math.ceil(nevents / events_per_file))):

        outfile = os.path.join(outdir, f"{outfile_tmplt}_{i:002d}.root")

        df.Range(pos, pos + events_per_file).Snapshot(treename, outfile)
        pos += events_per_file

if __name__ == "__main__":

    tau_files = "../NTuples/user.bewilson.TauClassifierV3.425200.Pythia8EvtGen_A14NNPDF23LO_Gammatautau_MassWeight_v0_output.root/*.root"
    JZ1_files = "../NTuples/user.bewilson.TauClassifierV3.425200.Pythia8EvtGen_A14NNPDF23LO_Gammatautau_MassWeight_v0_output.root/*.root"
    JZ2_files = "../NTuples/user.bewilson.tauclassifier.364702.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ2WithSW_v0_output.root/*.root"
    JZ3_files = "../NTuples/user.bewilson.tauclassifier.364703.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ3WithSW_v0_output.root/*.root"
    JZ4_files = "../NTuples/user.bewilson.tauclassifier.364704.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ4WithSW_v0_output.root/*.root"
    JZ5_files = "../NTuples/user.bewilson.tauclassifier.364705.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ5WithSW_v0_output.root/*.root"
    JZ6_files = "../NTuples/user.bewilson.tauclassifier.364706.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ6WithSW_v0_output.root/*.root"
    JZ7_files = "../NTuples/user.bewilson.tauclassifier.364707.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ7WithSW_v0_output.root/*.root"
    JZ8_files = "../NTuples/user.bewilson.tauclassifier.364708.Pythia8EvtGen_A14NNPDF23LO_jetjet_JZ8WithSW_v0_output.root/*.root"


    # split_files(tau_files, "../split_NTuples/Gammatautau", "Gammatautau")
    # split_files(JZ1_files, "../split_NTuples/JZ1", "JZ1")
    # split_files(JZ2_files, "../split_NTuples/JZ2", "JZ2")
    # split_files(JZ3_files, "../split_NTuples/JZ3", "JZ3")
    split_files(JZ4_files, "../split_NTuples/JZ4", "JZ4", events_per_file=50000)
    # split_files(JZ5_files, "../split_NTuples/JZ5", "JZ5")
    # split_files(JZ6_files, "../split_NTuples/JZ6", "JZ6")
    # split_files(JZ7_files, "../split_NTuples/JZ7", "JZ7")
    # split_files(JZ8_files, "../split_NTuples/JZ8", "JZ8")

