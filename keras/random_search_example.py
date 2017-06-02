#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 11:44:08 2017
@author: seanyu

Example code for randomSearch with Keras model
# hyper-parameter tuning

"""

# other basic libraries
from PIL import Image
import skimage.io as skio
import cv2
import glob
import numpy as np
import scipy as sp
import scipy.stats 
import pandas as pd
import os
import sys
import re
from scipy.stats import percentileofscore
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
# basic libraries
from __future__ import print_function
import random
import matplotlib.pyplot as plt


# main requires libraries
import keras
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Activation, Flatten, Input
from keras.layers import Convolution2D, MaxPooling2D, Conv2D, BatchNormalization
from keras.utils import np_utils
from keras import backend as K
from keras.optimizers import SGD, Adam, Adagrad
from keras.regularizers import l1, l2
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import Callback
K.set_image_dim_ordering('tf')
from keras.callbacks import ModelCheckpoint

from hyperopt import fmin, tpe, hp, STATUS_OK, Trials

## Define search item and range
space = {'choice': hp.choice('num_layers',
                             [{'c_layers': 'two', },
                              {'c_layers': 'three', 'c_units3': 2 ** (5 + hp.randint('c_units3', 2))}]), # 2^5 ~ 2^7
                             'd_units1': 2 ** (4 +hp.randint('d_units1', 2)), # 2^4 ~ 2^6
                             'd_units2': 2 ** (3 +hp.randint('d_units2', 1)), # 2^3 ~ 2^4
                             'd_dropout': hp.uniform('d_dropout1', .3, .5),
                             'batch_size': 2 ** (4 + hp.randint('batch_size',1)),
                             'nb_epochs': 20,
                             'optimizer': hp.choice('optimizer', ['adam', 'rmsprop']),
                             'activation': 'relu'}

## Define 
def f_cnn(params):
    print('Params testing: ', params)
    model = Sequential()
    model.add(Conv2D(32, (3,3), 
                     padding='same', input_shape = (90,90,1) ))
    model.add(Activation(params['activation']))
    model.add(MaxPooling2D(pool_size=(2,2)))
    
    model.add(Conv2D(32, (3,3) ))
    model.add(Activation(params['activation']))
    model.add(MaxPooling2D(pool_size=(2,2)))
    
    if params['choice']['c_layers'] == 'three':
        model.add(Conv2D(params['choice']['c_units3'], (3,3) ))
        model.add(Activation(params['activation']))
        model.add(MaxPooling2D(pool_size=(2,2)))
    else:
        model.add(MaxPooling2D(pool_size=(2,2)))
    
    # flatten
    model.add(Flatten())
    
    # random dense
    model.add(Dense(params['d_units1']))
    model.add(Activation(params['activation']))
    model.add(Dropout(params['d_dropout']))
    
    model.add(Dense(params['d_units2']))
    model.add(Activation(params['activation']))
    model.add(Dropout(params['d_dropout']))
    
    model.add(Dense(2))
    model.add(Activation('softmax'))
    
    model.compile(loss = 'categorical_crossentropy',
                  optimizer= params['optimizer'],
                  metrics=['acc'])
    model.fit(im_array[i_train], y_all[i_train],
              batch_size= params['batch_size'],
              epochs= params['nb_epochs'],
              validation_split = 0.1,
              shuffle=True)
    pred = model.predict(im_array[i_test], batch_size = 16)
    min_obj = f1_score(y_all[i_test].argmax(axis = 1), pred.argmax(axis = 1))
    print('f1sc: ', min_obj)
    sys.stdout.flush()
    return {'loss': -min_obj, 'status': STATUS_OK}
#%%
trials = Trials()
best = fmin(f_cnn, space, algo = tpe.suggest, max_evals = 30, trials = trials)
