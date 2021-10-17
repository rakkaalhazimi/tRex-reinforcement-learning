import tensorflow as tf


def list_to_tensor(seq):
    """Convert all values inside list to tf.Tensor"""
    seq = [float(num) for num in seq]
    return tf.expand_dims(tf.constant(seq, dtype=tf.float32), axis=0)


if __name__ == '__main__':
    print(list_to_tensor([1, 2, 3]))