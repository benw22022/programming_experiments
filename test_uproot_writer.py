import uproot
import awkward as ak
import numpy as np

if __name__ == "__main__":

    # with uproot.open("Gammatautau_001.root:tree")["TauClassifier_Labels"] as f:
    #     arr = f.array(library='np')
    
    file = uproot.update("Gammatautau_001.root")
    
    try:
        del file["tree2"]
    except Exception:
        pass

    file["tree2"] = {"TauClassifier_Labels": np.ones((10000, 6)) * 2}
    
    
    
    # file = uproot.open("Gammatautau_001.root:tree")
    # keys = file.keys()
    # for key in keys:
    #     if "normed" in key:
    #         arr = file[key].array()
    #         max_val = f"{ak.max(arr):.2f}"
    #         print(f"{key:^{1}}: {max_val:^{2}}")


    # file = uproot.update()