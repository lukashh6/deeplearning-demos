import tensorflow as tf


def conv_layer(input, side, channels_in, channels_out, stride=2, name='conv_layer'):
    with tf.name_scope(name):
        w = tf.Variable(tf.truncated_normal([side, side, channels_in,
                                             channels_out]), name='W')
        b = tf.Variable(tf.truncated_normal([channels_out]),
                        name='B')

        conv = tf.nn.conv2d(input, w, [1, 1, 1, 1], padding='SAME')
        act = tf.nn.relu(conv + b)

        tf.summary.histogram('weights', w)
        tf.summary.histogram('biases', b)
        return tf.nn.max_pool(act, [1, 2, 2, 1], [1, stride, stride, 1],
                              padding='SAME')


def fc_layer(input, channels_in, channels_out, name='fc_layer'):
    with tf.name_scope(name):
        w = tf.Variable(tf.truncated_normal([channels_in, channels_out]),
                        name='W')
        b = tf.Variable(tf.truncated_normal([channels_out]),
                        name='B')
        pkeep = tf.constant(0.75, dtype=tf.float32, name='pkeep')
        dropout = tf.nn.dropout(input, pkeep)
        tf.summary.histogram('weights', w)
        tf.summary.histogram('biases', b)

        return tf.nn.relu(tf.matmul(dropout, w) + b)


def output_layer(input, channels_in, channels_out, name='output_layer'):
    with tf.name_scope(name):
        w = tf.Variable(tf.truncated_normal([channels_in, channels_out]),
                        name='W')
        b = tf.Variable(tf.truncated_normal([channels_out]),
                        name='B')

        tf.summary.histogram('weights', w)
        tf.summary.histogram('biases', b)
        return tf.matmul(input, w) + b


def ae_layer(input, channels_in, channels_out, name='ae_layer'):
    with tf.name_scope(name):
        w = tf.Variable(tf.truncated_normal([channels_in, channels_out]),
                        name='W')
        b = tf.Variable(tf.truncated_normal([channels_out]),
                        name='B')

        tf.summary.histogram('weights', w)
        tf.summary.histogram('biases', b)
        return tf.nn.sigmoid(tf.matmul(input, w) + b)


def rbm_layer(input, channels_in, channels_out, name='rbm_layer'):
    with tf.name_scope(name):
        # Encoder Variables
        w = tf.Variable(tf.truncated_normal([channels_in, channels_out]),
                        name='W')
        _b = tf.Variable(tf.truncated_normal([channels_out]), name='_B')

        # reconstructor Varables
        b = tf.Variable(tf.truncated_normal([channels_in]), name='B')

        _y = tf.nn.sigmoid(tf.matmul(input, w) + _b)
        y = tf.nn.sigmoid(tf.matmul(_y, tf.transpose(w)) + b)

        tf.summary.histogram('weights', w)

        return y
