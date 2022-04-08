import uproot


import uproot
import glob


if __name__ == "__main__":

    files = glob.glob("../NTuples/*/*.root")

    for i in range(0, 500):
        print(i)
        arr = uproot.lazy(files, how='zip', step_size='50 MB')
        print(arr["TauTracks.pt"])
        break

    
        
