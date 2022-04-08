import ROOT
from variables import variable_handler
import tqdm

if __name__ == "__main__":

    df = ROOT.RDataFrame("tree", "TestFile.root")

    pos = 0
    batch_size = 2048
    it = 0
    nevents = df.Count().GetValue()

    for _ in tqdm.tqdm(range(nevents // batch_size)):
        it += 1
        batch_df = df.Range(pos, pos + batch_size)
        ROOT.EnableImplicitMT()
        batch_df = batch_df.AsNumpy(columns=variable_handler.list())
        ROOT.DisableImplicitMT()

        