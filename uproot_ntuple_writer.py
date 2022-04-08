import uproot
import glob
import numpy as np
import pandas as pd
import tqdm
import time

def compute_labels(decay_mode, is_tau):

    onehot_labels = np.zeros((len(decay_mode), 6))
    if not is_tau:
        onehot_labels[:, 0] = 1
    else:
        for i, dm in enumerate(decay_mode):
            onehot_labels[i][dm + 1] = 1

    return onehot_labels    

if __name__ == "__main__":

    files = glob.glob("../NTuples/*Gammatautau*/*.root")

    keys = uproot.open(f"{files[0]}:tree").keys()
    stats_df = pd.read_csv("../TauClassifier2/config/stats_df.csv", index_col=0)
    
    histfilename = "../TauClassifier2/config/ReWeightHist.root"
    histname = "ReWeightHist"
    histfile = uproot.open(histfilename)
    reweight_hist_edges = histfile[histname].axis().edges()
    reweight_hist_values = histfile[histname].values()

    for i, batch in enumerate(uproot.iterate(files, step_size = 100000)):
        i += 1
        start_time = time.time()
        new_file = uproot.recreate(f"Gammatautau_{i:03d}.root")

        branch_dict = {}
        for column in keys:
    
            column_fixed = column.replace(".", "_")

            branch_dict[column_fixed] = batch[column]
            try:
                mean = stats_df.loc[column_fixed]["Mean"]
                std = stats_df.loc[column_fixed]["StdDev"]
                branch_dict[f"{column_fixed}_normed"] = (batch[column] - mean) / (std + 1e-8)
            except KeyError:
                pass

        branch_dict["TauClassifier_Labels"] = compute_labels(batch["TauJets.truthDecayMode"], True)
        branch_dict["TauClassifier_pTReweight"] = np.asarray(reweight_hist_values[np.digitize(batch["TauJets.ptJetSeed"], reweight_hist_edges)])

        new_file['tree'] = branch_dict

        print(f"Done: Gammatautau_{i:03d}.root in {time.time - start_time}s")
