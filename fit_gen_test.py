import ROOT
import tensorflow as tf
import numpy as np
from models import TestModel
from generator import Generator


if __name__ == "__main__":

    files = "/mnt/c/Users/benwi/NTuples/user.bewilson.TauClassifierV3.425200.Pythia8EvtGen_A14NNPDF23LO_Gammatautau_MassWeight_v0_output.root/*.root"
    
    gen = Generator(files, batch_size=10000)

    model = TestModel()
    opt = tf.keras.optimizers.Adam()
    model.compile(optimizer=opt, loss="sparse_categorical_crossentropy", metrics=[tf.keras.metrics.CategoricalAccuracy()])

    model.fit(gen[0])
    
    