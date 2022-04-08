import matplotlib.pyplot as plt
import uproot
import glob
import awkward as ak

if __name__ == "__main__":

    arr = uproot.lazy(glob.glob("/mnt/c/Users/benwi/NTuples/*/*.root"), filter_name=["TauTracks.jetpt", "TauJets.ptJetSeed"])

    print(arr["TauTracks.jetpt"][1])

    # plt.hist(ak.flatten(arr["TauTracks.jetpt"]), bins=30)
    # plt.show()