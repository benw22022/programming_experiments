import ROOT
import numpy
import glob

ROOT.ROOT.EnableImplicitMT()

ROOT.gInterpreter.Declare('''
float ComputeHistReweight(const TH1* hist, const float& variable)
{   
    if(variable < hist->GetXaxis()->GetBinLowEdge(0)){
        return hist->GetBinContent(0);
    }

    for(unsigned int i{0}; i < hist->GetNbinsX(); i++){
        double low_edge = hist->GetXaxis()->GetBinLowEdge(i);
        double up_edge = hist->GetXaxis()->GetBinUpEdge(i);
        
        if(variable >= low_edge && variable < up_edge){
            return hist->GetBinContent(i);
        }
    }
    
    return hist->GetBinContent(hist->GetNbinsX() - 1);
}
''')

def get_reweight_hist(tau_files, fake_files):

    tau_df = ROOT.RDataFrame("tree", tau_files)
    fake_df = ROOT.RDataFrame("tree", fake_files)

    tau_hist = tau_df.Histo1D(("TaupT", "Tau pT", 500, 15e3, 1e7), "TauJets.ptJetSeed")
    fake_hist = fake_df.Histo1D(("FakepT", "Fake pT", 500, 15e3, 1e7),"TauJets.ptJetSeed")

    ratio_hist = tau_hist.Clone("Tau pT / Jet pT")

    ratio_hist.Divide(fake_hist.GetPtr())

    # ratio_hist.Scale(1 / ratio_hist.Integral())
    print(type(ratio_hist))


    return ratio_hist

# @ROOT.Numba.Declare



def reweight_file(file, hist):

    df = ROOT.RDataFrame("tree", file)
    df = df.Define("ReweightHist", hist)
    df = df.Define("TauJets_Reweight",  "ComputeHistReweight({0}, TauJets.ptJetSeed)".format(hist))


if __name__ == "__main__":

    tau_files = glob.glob("../NTuples/*Gammatautau*/*.root")
    fake_files = glob.glob("../NTuples/*JZ*/*.root")

    reweight_hist = get_reweight_hist(tau_files, fake_files)

    outfile = ROOT.TFile.Open("ReWeightHist.root", "RECREATE")

    outfile.WriteObject(reweight_hist, "ReWeightHist")

    # reweight_hist.Save("ReweightHist.root")

    # reweight_file(tau_files[0], reweight_hist)