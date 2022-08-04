import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from keras.datasets import mnist, cifar10
from keras.utils import to_categorical
from keras.layers import Conv2D, BatchNormalization, Activation, MaxPooling2D, Flatten
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam

# Load dataset, add channel dimension for images, and one-hot encode labels
(X_train, y_train), (X_test, y_test) = mnist.load_data()
X_train = np.expand_dims(X_train, axis=-1)
X_test = np.expand_dims(X_test, axis=-1)
y_train = to_categorical(y_train, 10)
y_test = to_categorical(y_test, 10)

print("X_train shape", X_train.shape)
print("y_train shape", y_train.shape)
print("X_test shape", X_test.shape)
print("y_test shape", y_test.shape)

# Convert type and normalize
X_train.astype('float32')
X_test.astype('float32')
X_train = X_train / 255.0
X_test = X_test / 255.0

# Display first image in training set
plt.imshow(X_train[0])
print('Label: ' + str(np.argmax(y_train[0])))

# Flatten the train images into vectors
X_train_flattened = X_train.reshape(-1, 28*28)
X_test_flattened = X_test.reshape(-1, 28*28)

print("X_train_flattened shape", X_train_flattened.shape)
print("X_test_flattened shape", X_test_flattened.shape)

# Build model
model = Sequential()

model.add(Dense(512, input_shape=(784,), activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(10, activation='softmax'))

model.summary()

# Create optimizer and compile
optimizer = Adam(learning_rate=0.001)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(X_train_flattened, y_train, batch_size=128, epochs=5, 
          validation_data=(X_test_flattened, y_test), verbose=1)

# Evaluate model on test data
loss, acc = model.evaluate(X_test_flattened, y_test, batch_size=32)
print("Test loss is " + str(loss))
print("Test accuracy is " + str(acc))

# Predicted class of each image in test set
np.argmax(model.predict(X_test_flattened), axis=-1)

# Data generators with data augmentation for train images
train_datagen = ImageDataGenerator(rotation_range=8, width_shift_range=0.08, 
                                   height_shift_range=0.08, zoom_range=0.08)
test_datagen = ImageDataGenerator()

# Create generators using flow
train_generator = train_datagen.flow(X_train, y_train, batch_size=128)
test_generator = test_datagen.flow(X_test, y_test, batch_size=32)

# Build cnn
cnn = Sequential()
cnn.add(Conv2D(32, (3,3), input_shape=(28,28,1)))
cnn.add(BatchNormalization())
cnn.add(Activation('relu'))

cnn.add(Conv2D(32, (3,3)))
cnn.add(BatchNormalization())
cnn.add(Activation('relu'))
cnn.add(MaxPooling2D(2,2))

cnn.add(Conv2D(64, (3,3)))
cnn.add(BatchNormalization())
cnn.add(Activation('relu'))

cnn.add(Conv2D(64, (3,3)))
cnn.add(BatchNormalization())
cnn.add(Activation('relu'))
cnn.add(MaxPooling2D(2,2))
cnn.add(Flatten())

cnn.add(Dense(512))
cnn.add(BatchNormalization())
cnn.add(Activation('relu'))

cnn.add(Dropout(0.2))
cnn.add(Dense(10, activation='softmax'))

cnn.summary()

# Create optimizer and compile
cnn.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train model with generators
cnn.fit(train_generator, epochs=5, validation_data=test_generator, verbose=1)

# Evaluate model on test generator
loss, acc = cnn.evaluate(test_generator)
print("Test loss is " + str(loss))
print("Test accuracy is " + str(acc))

# Predicted class of each image in test set
np.argmax(cnn.predict(X_test), axis=-1)


