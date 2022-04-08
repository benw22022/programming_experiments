import uproot
import glob

def loop_itr(files):
    for batch in uproot.iterate(files, step_size="100 MB", how='zip'):
        yield batch


if __name__ == "__main__":

    files = glob.glob("../NTuples/*/*.root")

    for i in range(0, 500):
        print(i)
        for batch in loop_itr(files):
            print(batch["TauTracks"])
            break
        break

    
        
