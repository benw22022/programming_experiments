import uproot

if __name__ == "__main__":

    for batch in uproot.iterate("TestFile.root"):

        print(batch["TauClassifier_Labels"])
