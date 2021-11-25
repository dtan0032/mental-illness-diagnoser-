# -*- coding: utf-8 -*-
"""facial_cues_detector.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14u-ZSwSfkNVa73Nj1qxk3XOmFQZGGxsU

# Take images from video to create a dataset
"""

import os
from cv2 import cv2
pathOut = r"C:\\Users\GideonT\Desktop\Sense+\Out\\"
count = 0
counter = 1
# listing = os.listdir(r'C:\\Users\GideonT\Desktop\Sense+\Videos')

# for vid in listing:
#     vid = r"C:\\Users\GideonT\Desktop\Sense+\Videos\\" + vid
#     cap = cv2.VideoCapture(vid)
#     count = 0
#     counter += 1
#     success = True
#     while success:
#         success,image = cap.read()
#         print('read a new frame:',success)
#         if count%30 == 0:
#             cv2.imwrite(pathOut + 'frame%d.jpg'%count, image)
#         count += 1
vid = r"C:\\Users\GideonT\Desktop\Sense+\Videos\sad.mp4"
cap = cv2.VideoCapture(vid)
count = 0
counter += 1
success = True
while success:
    success, image = cap.read()
    print('read a new frame:',success)
    if count % 15 == 0:
        cv2.imwrite(pathOut + 'frame%d.jpg'%count, image)
    count += 1

"""#Prediction of emotion through Neural Net

Prediction by combining above video snippets and running them through model
"""
"""Creating model """
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import tensorflow as tf
import keras
from keras.models import Sequential,model_from_json
from keras.layers import Conv2D, MaxPooling2D, AveragePooling2D
from keras.layers import Dense, Activation, Dropout, Flatten
from keras.metrics import categorical_accuracy
from keras.callbacks import ModelCheckpoint
from keras.optimizers import *
from keras.layers.normalization import BatchNormalization
from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator
import matplotlib.pyplot as plt


def my_model():
    model = Sequential()
    input_shape = (48,48,1)
    model.add(Conv2D(64, (5, 5), input_shape=input_shape, activation='relu', padding='same'))
    model.add(Conv2D(64, (5, 5), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(128, (5, 5), activation='relu', padding='same'))
    model.add(Conv2D(128, (5, 5), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(256, (3, 3), activation='relu', padding='same'))
    model.add(Conv2D(256, (3, 3), activation='relu', padding='same'))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.2))
    model.add(Dense(7))
    model.add(Activation('softmax'))

    model.compile(loss='categorical_crossentropy', metrics=['accuracy'],optimizer='adam')
    # UNCOMMENT THIS TO VIEW THE ARCHITECTURE
    model.summary()

    return model


model=my_model()
# model.summary()
# print(os.listdir(r"C:\\Users\GideonT\Desktop\Sense+\Out\\"))

filename = r"C:\\Users\GideonT\Desktop\Sense+\fer2013.csv"

label_map = ['Anger', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
names = ['emotion', 'pixels', 'usage']
df = pd.read_csv(filename)
im = df['pixels']


def getData(filename):
    # images are 48x48
    # N = 35887
    Y = []
    X = []
    first = True
    for line in open(filename):
        if first:
            first = False
        else:
            row = line.split(',')
            Y.append(int(row[0]))
            X.append([int(p) for p in row[1].split()])

    X, Y = np.array(X) / 255.0, np.array(Y)
    return X, Y


X, Y = getData(filename)
num_class = len(set(Y))
#print(num_class)

N, D = X.shape
X = X.reshape(N, 48, 48, 1)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1, random_state=0)
y_train = (np.arange(num_class) == y_train[:, None]).astype(np.float32)
y_test = (np.arange(num_class) == y_test[:, None]).astype(np.float32)

path_model = 'model_1.h5' # save model at this location after each epoch

################################################################################## Train new model ##################################################################################
# tf.keras.backend.clear_session() # destroys the current graph and builds a new one
# model = my_model() # create the model
#
# keras.backend.set_value(model.optimizer.lr, 1e-3) # set the learning rate
#
# # fit the model
# h=model.fit(x=X_train,
#             y=y_train,
#             batch_size=64,
#             epochs=20,
#             verbose=1,
#             validation_data=(X_test,y_test),
#             shuffle=True,
#             callbacks=[ModelCheckpoint(filepath=path_model)])
################################################################################## END ##################################################################################

objects = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
y_pos = np.arange(len(objects))
# print(y_pos)


model = keras.models.load_model('model_1.h5')
# print(model.summary())
###################################
y_pred = model.predict(X_test)
####################################

results = []
snips = os.listdir(r'C:\\Users\GideonT\Desktop\Sense+\Out')
for pic in snips:
    img = image.load_img(r"C:/Users/GideonT/Desktop/Sense+/Out/" + pic, grayscale=True, target_size=(48, 48))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis = 0)
    x /= 255

    custom = model.predict(x)
    results.append([custom])
print(results)
print("custom", custom[0])
print("OBJ", objects)

x = np.array(x, 'float32')
x = x.reshape([48, 48])

m = 0.000000000000000000001
a = custom[0]
for i in range(0, len(a)):
    if a[i] > m:
        m = a[i]
        ind = i

print('Expression Prediction:', objects[ind])
