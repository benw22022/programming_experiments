import uproot
import numpy as np


if __name__ == "__main__":

    arr = uproot.concatenate(["Gammatautau_01.root:tree"], filter_name="TauJets_mcEventWeight", library='np')

    file = uproot.update("Gammatautau_01.root")

    try:
        del file['tree2']
    except Exception:
        pass

    file['tree2'] = {"dummy": np.zeros(len(arr["TauJets_mcEventWeight"]))}
    
    x = uproot.open("Gammatautau_01.root:tree")['TauJets_truthDecayMode'].array()
    y = uproot.open("Gammatautau_01.root:tree2")['dummy'].array()

    print(x)
    print(y)
    print(len(x))
    print(len(y))
    