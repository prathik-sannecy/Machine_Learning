# Code leveraged from Keras tutorial: https://www.tensorflow.org/tutorials/keras/regression

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
# raw_dataset = pd.read_csv("../Data_Sets/2012-18_teamBoxScore_short.csv", names=column_names)


dataset = raw_dataset.copy()
dataset.tail()


dataset['teamAbbr'] = dataset['teamAbbr'].map(teamToIndex)
dataset['teamRslt'] = dataset['teamRslt'].map(win_loss_to_index)
dataset['opptAbbr'] = dataset['opptAbbr'].map(teamToIndex)

train_dataset = dataset.sample(frac=0.8,random_state=0)
test_dataset = dataset.drop(train_dataset.index)
print(train_dataset)
train_stats = train_dataset.describe()
train_stats.pop("teamRslt")
train_stats = train_stats.transpose()

train_labels = train_dataset.pop('teamRslt')
test_labels = test_dataset.pop('teamRslt')


def norm(x):
  return (x - train_stats['mean']) / train_stats['std']
normed_train_data = norm(train_dataset)
normed_test_data = norm(test_dataset)

def build_model():
  model = keras.Sequential([
    layers.Dense(128, activation='relu', input_shape=[len(train_dataset.keys())]),
    layers.Dense(128, activation='relu'),
    # layers.Dense(64, activation='relu', input_shape=[len(train_dataset.keys())]),
    # layers.Dense(64, activation='relu'),
    # layers.Dense(64, activation='relu'),
    layers.Dense(1, activation='sigmoid')
  ])
  model.add(keras.layers.Dropout(0.01))
  opt = keras.optimizers.SGD(learning_rate=0.001)
  model.compile(loss='binary_crossentropy',
                optimizer='adam')

  # model.compile(loss='mse',
  #               optimizer=opt,
  #               metrics=['mae', 'mse'])

  return model

model = build_model()
# The patience parameter is the amount of epochs to check for improvement
# early_stop = keras.callbacks.EarlyStopping(monitor='val_loss', patience=100)


model.summary()

# example_batch = normed_train_data[:10]
# example_result = model.predict(example_batch)
# print(example_result)


EPOCHS = 1000

model.fit(
  normed_train_data, train_labels,
  epochs=EPOCHS, verbose=0)



test_predictions = model.predict(normed_test_data).flatten()
print(test_predictions)
test_predictions_clamped = list(map(lambda x: 1 if x > 0.5 else 0, test_predictions))

error = test_predictions_clamped - test_labels
plt.hist(error, bins = 2)
plt.xlabel("Prediction Error [res]")
_ = plt.ylabel("Count")

wrong = [x for x in error if x != 0]
right = [x for x in error if x == 0]
print(len(right)/len(test_labels))

plt.show()