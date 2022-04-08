import ROOT
import uproot


if __name__ == "__main__":

    arr = uproot.open("Gammatautau_01.root:tree")["TauJets_truthDecayMode"].array(library='np')

    # print(arr)

    @ROOT.Numba.Declare([], 'RVec<float>')
    def pyarray():
        return arr

    df = ROOT.RDataFrame("tree", "Gammatautau_01.root")

    df = df.Define("Result", 'pyarray()')

    df.Snapshot("tree", "Gammatautau_01.root")
