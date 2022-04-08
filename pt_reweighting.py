import ROOT
import glob
snapshotOptions = ROOT.RDF.RSnapshotOptions()
snapshotOptions.UPDATE = True
ROOT.EnableImplicitMT()


def createRatio(h1, h2):
    h3 = h1.Clone("h3")
    h3.SetMarkerStyle(21)
    h3.SetTitle("")
    # Set up plot for markers and errors
    h3.Sumw2()
    h3.SetStats(0)
    h3.Divide(h2)

    return h3


ROOT.gInterpreter.Declare('''
ROOT::RVec<int> pTReweight(const TH1& reweight_hist, const float& event_weight, const float& jet_pt)
{
    int nbinsx = reweight_hist->GetXaxis()->GetNbins();

    for (auto x=1; x < nbinsx; x++) {

        lower_edge = reweight_hist->GetBinContent(x - 1); 
        upper_edge = reweight_hist->GetBinContent(x); 

        if (jet_pt >= lower_edge && jet_pt < upper_edge) {
            return (upper_edge + lower_edge / 2) * event_weight;
        }
    }
    
    // If jet pt lies outside of bounds
    if (jet_pt < reweight_hist->GetBinContent(0)){
        return reweight_hist->GetBinContent(0) * event_weight;
    }
    return reweight_hist.GetBinContent(nbinsx - 1) * event_weight;
    
}
''')


if __name__ == "__main__":

    jets_df = ROOT.RDataFrame("tree", glob.glob("../NTuples/*JZ*/*.root"))
    taus_df = ROOT.RDataFrame("tree", glob.glob("../NTuples/*Gammatautau*/*.root"))

    jets_pt_histo = jets_df.Histo1D(("h_TauJet_pt", "h_TauJet_pt", 50, 0, 1e7), "TauJets.ptJetSeed", "TauJets.mcEventWeight")
    taus_pt_histo = taus_df.Histo1D(("h_TauJet_pt", "h_TauJet_pt", 50, 0, 1e7), "TauJets.ptJetSeed", "TauJets.mcEventWeight")

    h1 = jets_pt_histo.Clone("h3")
    h2 = taus_pt_histo.Clone("h3")

    reweighting_hist = createRatio(h2, h1)

    jets_df = jets_df.Define("TauJets.ptReweight", f"pTReweight({reweighting_hist}, TauJets.mcEventWeight, TauJets.ptJetSeed)")
    taus_df = taus_df.Define("TauJets.ptReweight", f"pTReweight({reweighting_hist}, TauJets.mcEventWeight, TauJets.ptJetSeed)")
