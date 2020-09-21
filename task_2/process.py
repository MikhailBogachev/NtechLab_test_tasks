import efficientnet.tfkeras as efn
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow.keras.models as M
import tensorflow.keras.layers as L
from tensorflow.keras import optimizers
import numpy as np
import pandas as pd
import os
import sys
import json

file_names = os.listdir(sys.argv[-1])

BATCH_SIZE = 64  # уменьшаем batch если сеть большая, иначе не влезет в память на GPU
CLASS_NUM = 2  # количество классов в нашей задаче
IMG_SIZE = 128  # какого размера подаем изображения в сеть
IMG_CHANNELS = 3  # у RGB 3 канала
input_shape = (IMG_SIZE, IMG_SIZE, IMG_CHANNELS)

RANDOM_SEED = 42

df = pd.DataFrame(file_names, columns=['Id'])

test_datagen = ImageDataGenerator(rescale=1. / 255)
test_generator = test_datagen.flow_from_dataframe(dataframe=df, directory=sys.argv[-1], x_col="Id",
                                                  y_col=None,
                                                  shuffle=False,
                                                  class_mode=None,
                                                  target_size=(IMG_SIZE, IMG_SIZE),
                                                  batch_size=BATCH_SIZE,
                                                  seed=RANDOM_SEED)
#Model

base_model = efn.EfficientNetB6(weights='imagenet', include_top=False, input_shape=input_shape)
base_model.trainable = False
model = M.Sequential()
model.add(base_model)
model.add(L.GlobalAveragePooling2D(),)
model.add(L.Dense(CLASS_NUM, activation='softmax'))
model.compile(loss="categorical_crossentropy", optimizer=optimizers.Adam(lr=0.001), metrics=["accuracy"])
model.load_weights('best_model.hdf5')

#Prediction

predictions = model.predict_generator(test_generator, steps=len(test_generator), verbose=1)
predictions = np.argmax(predictions, axis=-1)
label_map = ({0: 'female', 1: 'male'})
predictions = [label_map[k] for k in predictions]
prediction = dict(zip(file_names, predictions))

#Сохранение в json-файл
with open("process_results.json", "w", encoding="utf-8") as file:
    json.dump(prediction, file)