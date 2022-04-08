"""
Variables
_____________________________________________________________
Imput Variables configuration
"""

from dataclasses import dataclass
from typing import List
import math
import numpy as np

@dataclass
class Variable:
    """
    A dataclass for handling input variables
    members:
        type (str): The type of variable e.g. TauTracks, NeutralPFO ect...
        name (str): Name of the variable
        max_val (float, optional: default=None): Maximum value variable is allowed to take
        minx_val (float, optional: default=None): Minimum value variable is allowed to take
        lognorm (bool, optional: default=False): If True will take lognorm10 of variable
    """
    
    type: str
    name:str
    max_val: float = None
    min_val: float = None
    lognorm: bool = False
    norm: bool = False
    mean: float = None
    std: float = None
    rescale_mean: bool = False

    def standardise(self, data_arr, dummy_val=-1):
        
        if self.min_val is not None:
            data_arr = np.where(data_arr >= self.min_val, data_arr, dummy_val)
        if self.max_val is not None:
            data_arr = np.where(data_arr <= self.max_val, data_arr, dummy_val)

        elif self.lognorm:
            data_arr = np.ma.log10(data_arr)
            # data_arr = (data_arr - np.amin(data_arr)) / (np.amax(data_arr) - np.amin(data_arr))
            data_arr = (data_arr - 0) / (math.log10(self.max_val) - 0)
            data_arr = data_arr.filled(dummy_val)
        
        elif self.norm:
            data_arr = (data_arr - 0) / (math.log10(self.max_val) - 0)

        elif self.rescale_mean:
            data_arr = (data_arr - self.mean) / self.std

        return data_arr

    def __call__(self, x):
        return self.name

    def __str__(self):
        return self.name

@dataclass
class VariableHandler:
    """
    A helper class to store and handle input variables
    members:
        variables (List(Variable)): A list of Variable dataclass instances
    """
    variables: List[Variable]

    def add_variable(self, variable):
        """
        Adds a new variable to the VariableHandler
        args:
            variable (Variable): An instance of the Variable dataclass
        returns:
            None
        """
        self.variables.append(variable)

    def get(self, var_type, names_only=False, padded=True):
        """
        Returns a list of all variables sharing the same type 
        args:
            type (str): Variable type e.g. TauJets, NeutralPFO etc..
        returns:
            (list): A list of Variables sharing the same var_type
        """
        if names_only:
            if padded:
                return [variable.name for variable in self.variables if variable.type == var_type]
            else:
                return [variable.name.replace("_padded", "") for variable in self.variables if variable.type == var_type]

        return [variable for variable in self.variables if variable.type == var_type]

    def list(self, padded=True):
        if padded:
            return [variable.name for variable in self.variables]
        else:
            return [variable.name.replace("_padded", "") for variable in self.variables]


    def __len__(self):
        return len(self.variables)

    def __getitem__(self, idx):
        return self.variables[idx]
    
    def get_index(self, var_type, var_name):
        """
        Get index of variable of a specific type
        """
        vars_of_type = self.get(var_type, names_only=True)
        # print(vars_of_type)
        return vars_of_type.index(var_name)

variable_handler = VariableHandler([])

variable_handler.add_variable(Variable("TauTracks", "TauTracks_nInnermostPixelHits_padded", min_val=0, max_val=3, norm=True))
variable_handler.add_variable(Variable("TauTracks", "TauTracks_nPixelHits_padded", min_val=0, max_val=11, norm=True))
variable_handler.add_variable(Variable("TauTracks", "TauTracks_nSCTHits_padded", min_val=0, max_val=21, norm=True))
variable_handler.add_variable(Variable("TauTracks", "TauTracks_chargedScoreRNN_padded", min_val=0, max_val=1))
variable_handler.add_variable(Variable("TauTracks", "TauTracks_isolationScoreRNN_padded", min_val=0, max_val=1))
variable_handler.add_variable(Variable("TauTracks", "TauTracks_conversionScoreRNN_padded", min_val=0, max_val=1))
variable_handler.add_variable(Variable("TauTracks", "TauTracks_pt_padded", min_val=0, max_val=0.25e7, lognorm=True))
variable_handler.add_variable(Variable("TauTracks", "TauTracks_dphiECal_padded", min_val=0, max_val=1))
variable_handler.add_variable(Variable("TauTracks", "TauTracks_detaECal_padded", min_val=0, max_val=1))
variable_handler.add_variable(Variable("TauTracks", "TauTracks_jetpt_padded", min_val=0, max_val=3e7, lognorm=True))
variable_handler.add_variable(Variable("TauTracks", "TauTracks_d0TJVA_padded", min_val=0, max_val=100, lognorm=True))
variable_handler.add_variable(Variable("TauTracks", "TauTracks_d0SigTJVA_padded", min_val=0, max_val=250, lognorm=True))
variable_handler.add_variable(Variable("TauTracks", "TauTracks_z0sinthetaTJVA_padded", min_val=0, max_val=150, lognorm=True))
variable_handler.add_variable(Variable("TauTracks", "TauTracks_z0sinthetaSigTJVA_padded", min_val=0, max_val=2000, lognorm=True))

variable_handler.add_variable(Variable("ConvTrack", "ConvTrack_dphiECal_padded", min_val=0, max_val=1))
variable_handler.add_variable(Variable("ConvTrack", "ConvTrack_dphi_padded", min_val=0, max_val=1))
variable_handler.add_variable(Variable("ConvTrack", "ConvTrack_detaECal_padded", min_val=0, max_val=1))
variable_handler.add_variable(Variable("ConvTrack", "ConvTrack_deta_padded", min_val=0, max_val=1,))
variable_handler.add_variable(Variable("ConvTrack", "ConvTrack_pt_padded", min_val=0, max_val=5e7, lognorm=True))
variable_handler.add_variable(Variable("ConvTrack", "ConvTrack_jetpt_padded", min_val=0, max_val=3e7, lognorm=True))
variable_handler.add_variable(Variable("ConvTrack", "ConvTrack_d0TJVA_padded", min_val=0, max_val=100, lognorm=True))
variable_handler.add_variable(Variable("ConvTrack", "ConvTrack_d0SigTJVA_padded", min_val=0, max_val=250, lognorm=True))
variable_handler.add_variable(Variable("ConvTrack", "ConvTrack_z0sinthetaTJVA_padded", min_val=0, max_val=100, lognorm=True))
variable_handler.add_variable(Variable("ConvTrack", "ConvTrack_z0sinthetaSigTJVA_padded", min_val=0, max_val=100, lognorm=True))

variable_handler.add_variable(Variable("ShotPFO", "ShotPFO_dphiECal_padded", min_val=0, max_val=1))
variable_handler.add_variable(Variable("ShotPFO", "ShotPFO_dphi_padded", min_val=0, max_val=1))
variable_handler.add_variable(Variable("ShotPFO", "ShotPFO_detaECal_padded", min_val=0, max_val=1))
variable_handler.add_variable(Variable("ShotPFO", "ShotPFO_deta_padded", min_val=0, max_val=1))
variable_handler.add_variable(Variable("ShotPFO", "ShotPFO_pt_padded", min_val=0,  max_val=50000, lognorm=True))
variable_handler.add_variable(Variable("ShotPFO", "ShotPFO_jetpt_padded", min_val=0, max_val=3e7, lognorm=True))

variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_dphiECal_padded", min_val=0, max_val=1))
variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_dphi_padded", min_val=0, max_val=1))
variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_detaECal_padded", min_val=0, max_val=1))
variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_deta_padded", min_val=0, max_val=1))
variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_pt_padded", min_val=0, max_val=0.5e7, lognorm=True))
variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_jetpt_padded", min_val=0, max_val=3e7, lognorm=True))
variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_FIRST_ETA_padded", min_val=0, max_val=4, norm=True))
variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_SECOND_R_padded", min_val=0, max_val=50000, lognorm=True))
variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_DELTA_THETA_padded", min_val=0, max_val=1))
variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_CENTER_LAMBDA_padded", min_val=0, max_val=1300, lognorm=True))
variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_LONGITUDINAL_padded", min_val=0, max_val=1))
variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_SECOND_ENG_DENS_padded", min_val=0, max_val=10, lognorm=True))
variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_ENG_FRAC_CORE_padded", min_val=0, max_val=1))
variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_NPosECells_EM1_padded", min_val=0, max_val=300, lognorm=True))
variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_NPosECells_EM2_padded", min_val=0, max_val=300, lognorm=True))
variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_energy_EM1_padded", min_val=0, max_val=0.2e7, lognorm=True))
variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_energy_EM2_padded", min_val=0, max_val=0.2e7, lognorm=True))
variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_EM1CoreFrac_padded", min_val=0, max_val=1))
variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_firstEtaWRTClusterPosition_EM1_padded", min_val=0, max_val=0.25,  lognorm=True))
variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_firstEtaWRTClusterPosition_EM2_padded", min_val=0, max_val=0.25,  lognorm=True))
variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_secondEtaWRTClusterPosition_EM1_padded", min_val=0, max_val=0.01, lognorm=True))
variable_handler.add_variable(Variable("NeutralPFO", "NeutralPFO_secondEtaWRTClusterPosition_EM2_padded", min_val=0, max_val=0.01, lognorm=True))

variable_handler.add_variable(Variable("TauJets", "TauJets_centFrac", min_val=0, max_val=1.5, norm=True))
variable_handler.add_variable(Variable("TauJets", "TauJets_etOverPtLeadTrk", min_val=0, max_val=30, lognorm=True))
variable_handler.add_variable(Variable("TauJets", "TauJets_dRmax", min_val=0, max_val=1))
variable_handler.add_variable(Variable("TauJets", "TauJets_SumPtTrkFrac", min_val=0, max_val=1))
variable_handler.add_variable(Variable("TauJets", "TauJets_ptRatioEflowApprox", min_val=0, max_val=5, norm=True))
variable_handler.add_variable(Variable("TauJets", "TauJets_mEflowApprox", min_val=0, max_val=0.3e7, lognorm=True))
variable_handler.add_variable(Variable("TauJets", "TauJets_ptJetSeed", min_val=0, max_val=3.5e7, lognorm=True))
variable_handler.add_variable(Variable("TauJets", "TauJets_etaJetSeed", min_val=0, max_val=3, norm=True))
variable_handler.add_variable(Variable("TauJets", "TauJets_phiJetSeed", min_val=0, max_val=3.2, norm=True))

variable_handler.add_variable(Variable("DecayMode", "TauJets_truthDecayMode"))
variable_handler.add_variable(Variable("Label", "TauClassifier_Labels"))
variable_handler.add_variable(Variable("Prong", "TauJets_truthProng"))
variable_handler.add_variable(Variable("Weight", "TauJets_ptJetSeed"))

variable_handler.add_variable(Variable("AUX", "TauJets_truthProng"))
variable_handler.add_variable(Variable("AUX", "TauJets_truthDecayMode"))
variable_handler.add_variable(Variable("AUX", "TauJets_mu"))
variable_handler.add_variable(Variable("AUX", "TauJets_ptJetSeed"))
variable_handler.add_variable(Variable("AUX", "TauJets_etaJetSeed"))
variable_handler.add_variable(Variable("AUX", "TauJets_phiJetSeed"))
variable_handler.add_variable(Variable("AUX", "TauJets_RNNJetScoreSigTrans"))
