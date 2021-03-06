# -*- coding: utf-8 -*-
"""bone age prediction  .ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/11pAtJ-gX0BONNeA57QNmYAPgGsPrBEjB
"""

import numpy as np
import csv
import random
from PIL import Image
from PIL import ImageShow
import scipy
import os
import tensorflow as tf
#import tensorflow.keras.backend.tensorflow_backend as KTF
from keras.layers import Input, Dense, Flatten, Activation,\
    BatchNormalization, Reshape, UpSampling2D, ZeroPadding2D, \
    Dropout, Lambda, AveragePooling2D, GlobalAveragePooling2D, concatenate
from keras.applications.inception_resnet_v2 import InceptionResNetV2
from keras import Model
from keras.optimizers import Adam
from keras.applications.inception_v3 import InceptionV3
from keras.callbacks import ModelCheckpoint, History, EarlyStopping, CSVLogger, RemoteMonitor,ReduceLROnPlateau
from keras.preprocessing.image import ImageDataGenerator
import pandas as pd
from random import randint
#from keras.applications.vgg16 import VGG16

# Getting the api josn file to download the data from kaggle (competition authorization)
from google.colab import files
#files.upload()

!pip install -q kaggle
!mkdir -p ~/.kaggle
!cp kaggle.json ~/.kaggle/
!ls ~/.kaggle
!chmod 600 /root/.kaggle/kaggle.json  # set permission

!kaggle datasets download -d kmader/rsna-bone-age

!unzip -qq /content/rsna-bone-age.zip

df_raw =pd.read_csv('/content/boneage-training-dataset.csv')

df_raw

for i in range (4) : 
  img_name = f'/content/boneage-training-dataset/boneage-training-dataset/{training_data_list[randint(0,500)]}'
  img = Image.open(img_name)
  img = img.resize (img,(50,50))
  img

# Commented out IPython magic to ensure Python compatibility.
# %pylab inline
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
#for i in range (4) : 
  value = random.randint(0,500)
  img = mpimg.imread(f'/content/boneage-training-dataset/boneage-training-dataset/{training_data_list[value]}')
  imgplot = plt.imshow(img)

img_name = f'/content/boneage-training-dataset/boneage-training-dataset/{training_data_list[i]}'
img = Image.open(img_name).convert('RGB')
img = np.array(img.resize((img_size,img_size)))

imgplot

print(df_raw.head(6))

print(df_raw['boneage'][5])

import csv
from collections import defaultdict

id_train = []
boneage_train = []
male_train = []
with open('boneage-training-dataset.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        id_train.append(row[0])
        boneage_train.append(row[1])
        male_train.append(row[2])

for i in range (len(male_train)) :
  if male_train[i]=='True': male_train[i]=1
  else: male_train [i] = 0

id_train.pop(0);male_train.pop(0);boneage_train.pop(0)

import os
training_data_dir ='/content/boneage-training-dataset/boneage-training-dataset'
training_data_list = (os.listdir(training_data_dir)) #get training imgs names in a list 
training_data_list.sort() #when u get them in a list ,they r not sorted so u need to sort it

os.mkdir('/content/valdation')
os.mkdir('/content/valdation/val_img')
#os.mkdir('/content/valdation/val_labels')

import shutil
for val in range (1200):
  shutil.move(f'/content/boneage-training-dataset/boneage-training-dataset/{training_data_list[val]}','/content/valdation/val_img')

validation_list= os.listdir('/content/valdation/val_img')
print(len(validation_list))

id_val=[]
male_val=[]
boneage_val=[]
for i in range (1200):
  id_val.append( id_train[i]) 
  male_val.append(male_train[i])
  boneage_val.append(boneage_train[i])

print(len(id_val))
print(len(boneage_val))
print(len(male_val))

for i in range (7) :
  print(id_val[i],'\t',male_val[i],'\t',boneage_val[i])

del id_train[0:1200]
del boneage_train[0:1200]
del male_train[0:1200]

print(len(training_data_list))
print(len(id_train))

print(len(boneage_train))

for i in range (6):
  print (male_train[i])

print(len(id_train))

# for training data 

from skimage.transform import resize
from keras.applications.inception_v3 import preprocess_input

img_size=150
training_data = []

training_data_dir ='/content/boneage-training-dataset/boneage-training-dataset'
training_data_list = (os.listdir(training_data_dir)) #get training imgs names in a list 
training_data_list.sort() #when u get them in a list ,they r not sorted so u need to sort it 


for i in range(len(id_train)):
        img_name = f'/content/boneage-training-dataset/boneage-training-dataset/{training_data_list[i]}'
        img = Image.open(img_name).convert('RGB')
        img = np.array(img.resize((img_size,img_size)))
        img = img.reshape( img.shape[0], img.shape[1],img.shape[2])
        img = preprocess_input(img)
        training_data.append(img)

training_data = np.array(np.reshape(training_data, (-1, 150, 150, 3)), dtype='float32')
#training_data = (np.array(np.reshape(training_data, (-1, 299, 299, 3)), dtype='float32')/255.0)-0.5

training_data[0].shape

len(training_data)

np.save(f'/content/drive/My Drive/Projects/bone_age_prediction/images_in_np_array_to_csv/training_{training_size}', training_data)

training_data = np.load(f'/content/drive/My Drive/Projects/bone_age_prediction/images_in_np_array_to_csv/training_{training_size}')

#same thing for validation data 
from keras.applications.inception_v3 import preprocess_input
img_size=150
validation_data = []

validation_data_dir ='/content/valdation/val_img'
validation_data_list = (os.listdir(validation_data_dir))
validation_data_list.sort()

for i in range(len(id_val)):
        img_name = f'/content/valdation/val_img/{validation_data_list[i]}'
        img = Image.open(img_name).convert('RGB')
        img = np.array(img.resize((img_size,img_size)))
        img = img.reshape((img.shape[0], img.shape[1],img.shape[2]))
        img = preprocess_input(img)
        validation_data.append(img)

validation_data = np.array(np.reshape(validation_data, (-1, 150, 150, 3)), dtype='float32')
#validation_data = (np.array(np.reshape(validation_data, (-1, 299, 299, 3)), dtype='float32')/255.0)-0.5

np.save('/content/drive/My Drive/Projects/bone_age_prediction/images_in_np_array_to_csv/validation_data', validation_data)

validation_data = np.load('/content/drive/My Drive/Projects/bone_age_prediction/images_in_np_array_to_csv/validation_data')

validation_data[0].shape

len(validation_data)

boneage_train = np.array(np.reshape(boneage_train,(-1,)), dtype='float32')
male_train = np.array(np.reshape(male_train,(-1,)), dtype='float32')

boneage_val = np.array(np.reshape(boneage_val,(-1,)), dtype='float32')
male_val = np.array(np.reshape(male_val,(-1,)), dtype='float32')

print((male_train).shape)

i1 = Input(shape=(150,150,3), name='input_img')
i2 = Input(shape=(1,), name='input_gender')
base_model = InceptionV3(input_tensor=i1, input_shape=(150, 150, 3), include_top=False, weights='imagenet')
feature_image = base_model.output
feature_image = GlobalAveragePooling2D()(feature_image)
feature_image = Flatten()(feature_image)
feature_gender = Dense (32,activation='relu') (i2)
feature = concatenate([feature_image,feature_gender],axis=1)
o = Dense ( 1000, activation='relu') (feature)
o = Dense (1000,activation='relu') (o)
o = Dense (1)(o) 

model = Model(inputs=[i1,i2],outputs=o) 
optimizer = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
model.compile(loss='mean_absolute_error',optimizer=optimizer,metrics = ['mae'] )

train_idg = ImageDataGenerator(rotation_range=20, width_shift_range=0.2, height_shift_range=0.2,
                              zoom_range=0.2, horizontal_flip=True,validation_split=0.1)

val_idg = ImageDataGenerator(width_shift_range=0.25, height_shift_range=0.25, horizontal_flip=True)

len(id_val)

##del boneage_train[5000:11411]
##del male_train[5000:11411]
##del id_train[5000:11411]

##del boneage_val[500:1200]
##del male_val[500:1200]
##del id_val[500:1200]

print(len(boneage_train))
print(len(boneage_val))

batch_size=10
train_generator = train_idg.flow(
        training_data,
        boneage_train,
        batch_size=batch_size)


validation_generator = val_idg.flow(
                                validation_data,
                                boneage_val,
                                batch_size=batch_size,
                                save_to_dir='/content/augemented')

augmented=train_generator
print(augmented)

import os 
augmented=train_generator
augmented=os.listdir ('/content/augemented')
img_path = ( f'/content/augmented/{augmented[i]}')
print(len(augmented))

# Commented out IPython magic to ensure Python compatibility.
# %pylab inline
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
img = mpimg.imread('/content/augmented/_10129_3047768.png')
imgplot = plt.imshow(img)

img = Image.open('/content/augmented/_10129_3047768.png')
img

from itertools import cycle


def combined_generators(image_generator, gender_data, batch_size):
    gender_generator = cycle(batch(gender_data, batch_size))
    while True:
        nextImage = next(image_generator)
        nextGender = next(gender_generator)
        assert len(nextImage[0]) == len(nextGender)
        yield [nextImage[0], nextGender], nextImage[1]

def batch(iterable, n=1):
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]

train_gen_wrapper = combined_generators(train_generator, male_train, batch_size)
val_gen_wrapper = combined_generators(validation_generator, male_val, batch_size)

history = History()
logger = CSVLogger('/content/drive/My Drive/Projects/bone_age_prediction/logs/VGG19/training.log', separator=',', append=False)
earlystopping = EarlyStopping(monitor='val_loss', min_delta=0.01, patience=10, verbose=10, mode='min')
checkpoint = ModelCheckpoint('/content/drive/My Drive/Projects/bone_age_prediction/checkpoint/VGG19 '+ 'weights-{epoch:02d}-{val_loss:.2f}.h5', monitor='val_loss', save_best_only=True, verbose=1, mode='min')
reduceLROnPlat = ReduceLROnPlateau(monitor='val_loss', factor=0.8, patience=10, verbose=1, mode='auto', min_delta=0.0001, cooldown=5, min_lr=0.0001)

NUM_EPOCHS=100

history = model.fit_generator(train_gen_wrapper, validation_data=val_gen_wrapper,
                              epochs=NUM_EPOCHS, steps_per_epoch=len(train_generator),
                              validation_steps=len(validation_generator),
                              callbacks=[history, logger, earlystopping, checkpoint, reduceLROnPlat])

print(history)

# Commented out IPython magic to ensure Python compatibility.
# PLOT LOSS AND ACCURACY
# %matplotlib inline

import matplotlib.image  as mpimg
import matplotlib.pyplot as plt

#-----------------------------------------------------------
# Retrieve a list of list results on training and test data
# sets for each training epoch
#-----------------------------------------------------------
acc=history.history['acc']
val_acc=history.history['val_acc']
loss=history.history['loss']
val_loss=history.history['val_loss']

epochs=range(len(acc)) # Get number of epochs

#------------------------------------------------
# Plot training and validation accuracy per epoch
#------------------------------------------------
plt.plot(epochs, acc, 'r', "Training Accuracy")
plt.plot(epochs, val_acc, 'b', "Validation Accuracy")
plt.title('Training and validation accuracy')
plt.figure()

#------------------------------------------------
# Plot training and validation loss per epoch
#------------------------------------------------
plt.plot(epochs, loss, 'r', "Training Loss")
plt.plot(epochs, val_loss, 'b', "Validation Loss")


plt.title('Training and validation loss')

# Desired output. Charts with training and validation metrics. No crash :)