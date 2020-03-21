# This program uses a basic statistics to predict NBA games
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
train_dataset_list = train_dataset.values.tolist()
test_dataset_list = test_dataset.values.tolist()


# MODEL 1:
# Predictions based solely on priors (team that had won more against the opponent in the past will win again)
# Training section
records_teams = [[0] * 30 for i in range(30)]
for row in train_dataset_list:
    home_index = row[0]
    home_team_result = row[1]
    away_index = row[2]
    if min(home_index, away_index) == home_index:
        home_team_result = row[1]
    else:
        if row[1] == 1:
            home_team_result = 0
        else:
            home_team_result = 1
    if home_team_result == 1:
        records_teams[min(home_index, away_index)][max(home_index, away_index)] += 1
    else:
        records_teams[min(home_index, away_index)][max(home_index, away_index)] -= 1

# Testing section
correct_count = 0
for row in test_dataset_list:
    home_index = row[0]
    away_index = row[2]
    if min(home_index, away_index) == home_index:
        expected = row[1]
    else:
        if row[1] == 1:
            expected = 0
        else:
            expected = 1
    if(expected == 1) and (records_teams[min(home_index, away_index)][max(home_index, away_index)] >= 0):
        correct_count += 1
    elif(expected == 0) and (records_teams[min(home_index, away_index)][max(home_index, away_index)] < 0):
        correct_count += 1
print(correct_count/len(test_dataset_list))


# MODEL 2:
# Test home team vs away team, assume Home Team will win
correct_count = 0
for row in test_dataset_list:
    if row[1] == 1:
        correct_count += 1

print(correct_count/len(test_dataset_list))