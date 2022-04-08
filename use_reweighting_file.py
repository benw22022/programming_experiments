import uproot
import glob
import numpy as np
import matplotlib.pyplot as plt

def get_pt_reweight(pt, edges, values):
    
    return values[np.digitize(pt, edges)]

def load_reweight_hist(filename):

    file = uproot.open(filename)
    edges = file["ReWeightHist"].axis().edges()
    values = file["ReWeightHist"].values()

    return edges, values

if __name__ == "__main__":

    edges, values = load_reweight_hist("ReWeightHist.root")

    tau_files = glob.glob("../NTuples/*Gammatautau*/*.root")
    jet_files = glob.glob("../NTuples/*JZ*/*.root")

    jet_array = uproot.lazy(jet_files)
    tau_array = uproot.lazy(tau_files)

    weights = get_pt_reweight(jet_array["TauJets.ptJetSeed"], edges, values)

    fig, ax = plt.subplots()
    tau_hist, _, _ = ax.hist(tau_array["TauJets.ptJetSeed"], bins=edges, histtype='step', label='Taus')
    jet_hist, _, _ = ax.hist(jet_array["TauJets.ptJetSeed"], bins=edges, histtype='step', label='Jets')
    jet_hist, _, _ = ax.hist(jet_array["TauJets.ptJetSeed"], bins=edges, histtype='step', weights=weights, label='Jets Reweighted')
    ax.legend()
    ax.set_yscale('log')
    ax.set_ylabel("Events / Bin")
    ax.set_xlabel("Jet Seed pT (MeV)")
    plt.savefig("ptReweighting.png", dpi=300)
    plt.show()


    

