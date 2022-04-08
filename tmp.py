import uproot

try:
    a = uproot.open("file.root")
except FileNotFoundError:
    print("FileNotFound")