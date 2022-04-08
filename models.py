from keras import backend as kbe
from tensorflow.keras.layers import Input, Dense, Masking, TimeDistributed, Concatenate
from tensorflow.keras.layers import Layer, Activation, BatchNormalization
from tensorflow.keras import Model
import tensorflow as tf

# =============
# Custom Layers
# =============

class Sum(Layer):
    """Simple sum layer.

    The tricky bits are getting masking to work properly, but given
    that time distributed dense layers _should_ compute masking on
    their own

    See Dan's implementation:
    https://gitlab.cern.ch/deep-sets-example/higgs-regression-training/blob/master/SumLayer.py

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.supports_masking = True

    def build(self, input_shape):
        pass

    def call(self, x, mask=None):
        if mask is not None:
            x = x * kbe.cast(mask, kbe.dtype(x))[:, :, None]
        return kbe.sum(x, axis=1)

    def compute_output_shape(self, input_shape):
        return input_shape[0], input_shape[2]

    def compute_mask(self, inputs, mask=None):
        return None


# =================
# Functional models
# =================

def TestModel(mask_value=0, normalizers=None, bn=True):
    """
    TODO: docstring
    """
    initializer = tf.keras.initializers.HeNormal()
    activation_func = 'swish'

    # Branch 1
    x_1 = Input(shape=(22, 3))
    b_1 = Masking(mask_value=mask_value)(x_1)
    for x in range(3):
        b_1 = TimeDistributed(Dense(60, kernel_initializer=initializer))(b_1)
        b_1 = Activation(activation_func)(b_1)
    b_1 = Sum()(b_1)
    for x in range(3):
        b_1 = Dense(50, kernel_initializer=initializer)(b_1)
        b_1 = Activation(activation_func)(b_1)
    if bn:
        b_1 = BatchNormalization()(b_1)
        

    # Merge
    merged = b_1
    merged = Dense(50, kernel_initializer=initializer)(merged)
    merged = Activation(activation_func)(merged)
    merged = Dense(25, kernel_initializer=initializer)(merged)
    merged = Activation(activation_func)(merged)

    y = Dense(5, activation="softmax")(merged)

    return Model(inputs=x_1, outputs=y)
