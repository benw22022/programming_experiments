import ROOT
from dask.distributed import Client

# point RDataFrame calls to the Dask specific RDataFrame
# RDataFrame = ROOT.RDF.Experimental.Distributed.Dask.RDataFrame

client = Client("dask_scheduler.domain.com:8786")

# the Dask RDataFrame constructor accepts the Dask Client object as an optional argument
files = "/mnt/c/Users/benwi/NTuples/user.bewilson.TauClassifierV3.425200.Pythia8EvtGen_A14NNPDF23LO_Gammatautau_MassWeight_v0_output.root/*.root"
df = ROOT.RDataFrame("tree", files, daskclient=client)

