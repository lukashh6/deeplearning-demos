import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import sys
from os.path import join, splitext
from layers import layers
import config

train_dir = config.TRAIN_DIR
test_dir = config.TEST_DIR
n_trains = config.N_TRAINS
batch_size = config.BATCH_SIZE

width = config.WIDTH
height = config.HEIGHT
channels = config.CHANNELS
flat = config.FLAT
n_classes = config.N_CLASSES

k = 4352
l = 2176
m = 1088
n = 544
o = 272

mnist = input_data.read_data_sets('data', one_hot=True)


def get_dict(train=True, batch=True):
    if train:
        if batch:
            batch_x, batch_y = mnist.train.next_batch(batch_size)
            return {x: batch_x, y_: batch_y}
        else:
            return {x: mnist.train.images, y_: mnist.train.labels}
    else:
        if batch:
            batch_x, batch_y = mnist.test.next_batch(batch_size)
            return {x: batch_x, y_: batch_y}
        else:
            return {x: mnist.test.images, y_: mnist.test.labels}


with tf.name_scope('ActualValue'):
    y_ = tf.placeholder(tf.float32, shape=[None, n_classes], name='y_')

with tf.name_scope('InputLayer'):
    x = tf.placeholder(tf.float32, shape=[None, flat], name='x')

with tf.name_scope('NetworkModel'):
    y1 = layers.fc_layer(x, flat, k)
    y2 = layers.fc_layer(y1, k, l)
    y3 = layers.fc_layer(y2, l, m)
    y4 = layers.fc_layer(y3, m, n)
    y5 = layers.fc_layer(y4, n, o)
    y = layers.output_layer(y5, o, n_classes)

with tf.name_scope('Train'):
    loss = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=y_,
                                                                  logits=y), name='loss')
    train = tf.train.AdamOptimizer().minimize(loss)

with tf.name_scope('Accuracy'):
    correct_predictions = tf.equal(tf.argmax(y, axis=1), tf.argmax(y_, axis=1))
    accuracy = tf.reduce_mean(tf.cast(correct_predictions, tf.float32),
                              name='accuracy')

# Add scalar summaries
tf.summary.scalar('Loss', loss)
tf.summary.scalar('Accuracy', accuracy)

init_op = tf.global_variables_initializer()
summary_op = tf.summary.merge_all()

with tf.Session() as sess:
    # Open protocol for writing files
    train_writer = tf.summary.FileWriter(train_dir)
    train_writer.add_graph(sess.graph)
    test_writer = tf.summary.FileWriter(test_dir)

    sess.run(init_op)
    for n_train in range(1, n_trains + 1):
        print("Training {}...".format(n_train))
        _ = sess.run([train], feed_dict=get_dict(train=True, batch=True))
        if n_train % 100 == 0:
            # Train
            s = sess.run(summary_op, feed_dict=get_dict(train=True, batch=False))
            train_writer.add_summary(s, n_train)
            # Test
            s = sess.run(summary_op, feed_dict=get_dict(train=False, batch=False))
            test_writer.add_summary(s, n_train)
