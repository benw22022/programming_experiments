
import uproot
import awkward as ak
import tensorflow as tf
import glob
import numpy as np
import tqdm
from variables import variable_handler

if __name__ == "__main__":

    # files = glob.glob("../NTuples/*/*.root")

    j = 0

    columns = variable_handler.list(padded=False)

    with open("TestFile.tsv", 'w') as file:
        [file.write(f"{c}\t") for c in columns]
        file.write("\n")
        for array in tqdm.tqdm(uproot.iterate("TestFile.root", library='ak', filter_name=variable_handler.list(padded=False), step_size="100 MB", num_workers=16, num_fallback_workers=16)):
            for i in range(0, len(array)):
                for c in columns:
                    try:
                        for elem in array[i][c]:
                            file.write(f"{elem},")
                    except TypeError:
                        file.write(f"{elem},")
                    file.write("\t")
            file.write("\n")



