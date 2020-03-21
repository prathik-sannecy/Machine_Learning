# This program uses a Neural Network to predict NBA games
# Code leveraged from keras tutorial: https://www.tensorflow.org/tutorials/keras/regression
# Written by Prathik Sannecy
# 3/20/2020

from __future__ import absolute_import, division, print_function, unicode_literals

import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

print(tf.__version__)

import tensorflow_docs as tfdocs
import tensorflow_docs.plots
import tensorflow_docs.modeling
import sys

teamToIndex = {
    'ATL': 0,
    'BOS': 1,
    'BKN': 2,
    'CHA': 3,
    'CHI': 4,
    'CLE': 5,
    'DAL': 6,
    'DEN': 7,
    'DET': 8,
    'GS': 9,
    'HOU': 10,
    'IND': 11,
    'LAC': 12,
    'LAL': 13,
    'MEM': 14,
    'MIA': 15,
    'MIL': 16,
    'MIN': 17,
    'NO': 18,
    'NY': 19,
    'OKC': 20,
    'ORL': 21,
    'PHI': 22,
    'PHO': 23,
    'POR': 24,
    'SAC': 25,
    'SA': 26,
    'TOR': 27,
    'UTA': 28,
    'WAS': 29,
}

win_loss_to_index = {
    'Win' : 1,
    'Loss' : 0

}
home_away_to_index = {
    'Home' : 1,
    'Away' : 0

}

column_names = ['teamAbbr','teamRslt','opptAbbr']

raw_dataset = pd.read_csv("../Data_Sets/2012-18_teamBoxScore_new.csv", names=column_names)


dataset = raw_dataset.copy()
dataset.tail()


dataset['teamAbbr'] = dataset['teamAbbr'].map(teamToIndex)
dataset['teamRslt'] = dataset['teamRslt'].map(win_loss_to_index)
dataset['opptAbbr'] = dataset['opptAbbr'].map(teamToIndex)

def run(lr=0.001, num_layers=3, layer_height=128, dropout=0.01, EPOCHS= 1000):
    """
    Creates a Neural Network with the given data, and divvys it up into test and training data
    :param lr: learning rate
    :param num_layers: Number of layers in the neural network
    :param layer_height: Height of the hidden layers
    :param dropout: Dropout factor
    :param EPOCHS: Number of epochs to train for
    :return:
        float accuracy: the accuracy of the neural network on the testing set
    """
    # Generate test/train datasets
    train_dataset = dataset.sample(frac=0.8,random_state=0)
    test_dataset = dataset.drop(train_dataset.index)
    train_stats = train_dataset.describe()
    train_stats.pop("teamRslt")
    train_stats = train_stats.transpose()

    train_labels = train_dataset.pop('teamRslt')
    test_labels = test_dataset.pop('teamRslt')


    def norm(x):
      """Normalize the data"""
      return (x - train_stats['mean']) / train_stats['std']
    normed_train_data = norm(train_dataset)
    normed_test_data = norm(test_dataset)

    def build_model():
      """Build the Neural Network model using given parameters"""
      model = keras.Sequential([
        layers.Dense(layer_height, activation='relu', input_shape=[len(train_dataset.keys())])])
      for _ in range(num_layers-2):
          model.add(keras.layers.Dense(layer_height, activation='relu'))
      model.add(keras.layers.Dense(1, activation='sigmoid'))

      model.add(keras.layers.Dropout(dropout))
      opt = keras.optimizers.SGD(learning_rate=lr)
      model.compile(loss='binary_crossentropy',
                    optimizer='adam')

      return model

    model = build_model()
    model.summary()

    model.fit(
      normed_train_data, train_labels,
      epochs=EPOCHS, verbose=0)

    # Generate the predictions of the model on the testing data
    test_predictions = model.predict(normed_test_data).flatten()
    test_predictions_clamped = list(map(lambda x: 1 if x > 0.5 else 0, test_predictions))

    # Return the error of the predictions
    error = test_predictions_clamped - test_labels
    wrong = [x for x in error if x != 0]
    right = [x for x in error if x == 0]
    return(len(right)/len(test_labels))

def epoch_test():
    """Testing to figure out the correct epoch value"""
    EPOCHS_TEST = [200, 500, 1000, 2000]
    results = []
    tests = EPOCHS_TEST
    for test in tests:
        print(test)
        run_result = run(EPOCHS=test)
        print(run_result)
        results.append(run_result)

    plt.xscale('log')
    plt.xlabel("Num Epochs")
    plt.ylabel("Accuracy")
    plt.scatter(tests, results)
    plt.autoscale(tight=True)
    plt.show()

def lr_test():
    """Testing to figure out the correct learning rate value"""
    LR_TEST = [0.001, 0.005, 0.01, 0.05]
    results = []

    tests = LR_TEST
    for test in tests:
        print(test)
        run_result = run(lr=test)
        print(run_result)
        results.append(run_result)

    plt.xscale('log')
    plt.xlabel("Learning Rate")
    plt.ylabel("Accuracy")
    plt.scatter(tests, results)
    plt.autoscale(tight=True)
    plt.show()

def layer_height_test():
    """Testing to figure out the correct hidden layers' height value"""
    LAYER_HEIGHT_TEST = [16, 32, 64, 128]
    results = []

    tests = LAYER_HEIGHT_TEST
    for test in tests:
        print(test)
        run_result = run(layer_height=test)
        print(run_result)
        results.append(run_result)

    plt.xscale('log')
    plt.xlabel("Hidden Layers Height")
    plt.ylabel("Accuracy")
    plt.scatter(tests, results)
    plt.autoscale(tight=True)
    plt.show()

def num_layers_test():
    """Testing to figure out the correct number of layers"""
    NUM_LAYERS_TEST = [2, 3, 4]
    results = []

    tests = NUM_LAYERS_TEST
    for test in tests:
        print(test)
        run_result = run(num_layers=test)
        print(run_result)
        results.append(run_result)

    plt.xlabel("Number of Layers")
    plt.ylabel("Accuracy")
    plt.scatter(tests, results)
    plt.autoscale(tight=True)
    plt.show()

def dropout_test():
    """Testing to figure out the correct dropout rate"""
    DROPOUT_TEST = [.01, .05, .1, .2]
    results = []

    tests = DROPOUT_TEST
    for test in tests:
        print(test)
        run_result = run(dropout=test)
        print(run_result)
        results.append(run_result)

    plt.xlabel("Dropout Rate")
    plt.ylabel("Accuracy")
    plt.scatter(tests, results)
    plt.autoscale(tight=True)
    plt.show()

def main():
    """Based on the argument passed, decide whether to test a hyperparameter,
    or to train and run the model with default parameters"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "epoch":
            epoch_test()
        elif sys.argv[1] == "lr":
            lr_test()
        elif sys.argv[1] == "layer_height":
            layer_height_test()
        elif sys.argv[1] == "num_layers":
            num_layers_test()
        elif sys.argv[1] == "dropout":
            dropout_test()
        else:
            print(run())

    else:
        print(run())


if __name__ == '__main__':
    main()