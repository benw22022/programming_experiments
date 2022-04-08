import tensorflow as tf

dataset = tf.data.Dataset.from_tensor_slices(([10, 2, 13, 100, 5], [1, 1, 3, 3, 1]))
dataset = dataset.filter(lambda x, y: y == 1)
d = list(dataset.as_numpy_iterator())

print(d)