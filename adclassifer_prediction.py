# -*- coding: utf-8 -*-
"""adclassifer-prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/gist/2001akash/a212add5d88741701f900421df8db19c/adclassifer-prediction.ipynb

# AdClassifier
## Binary Classification model for classifying image ads into creative and non creative.

### First step is to import essential libraries
"""

import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.metrics import classification_report, confusion_matrix

"""### Second step to define our directory for the datset
- I have mounted my drive for running in own system just download the file using drive link and create a copy in your drive
[Dataset link](https://drive.google.com/drive/folders/1zkXay1lHPpJy7U2Df7C2ROIdj7u9XVj_)
"""

from google.colab import drive
drive.mount('/content/drive')

# Define the paths to your dataset
train_data_dir = '/content/drive/MyDrive/dataset'
train_data_generator = ImageDataGenerator(rescale=1./255, validation_split=0.2)

"""### Initialise the ImageDataGenerator for reading all the image files"""

# Create training and validation data generators
train_generator = train_data_generator.flow_from_directory(
    train_data_dir,
    target_size=(256, 256),
    batch_size=32,
    class_mode='binary',
    subset='training'
)

validation_generator = train_data_generator.flow_from_directory(
    train_data_dir,
    target_size=(256, 256),
    batch_size=32,
    class_mode='binary',
    subset='validation'
)



"""

```
# This is formatted as code
```

### Build a base CNN model for the task"""

# Build a simple convolutional neural network (CNN) model
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(256, 256, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

"""### Model training"""

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(train_generator, epochs=10, validation_data=validation_generator)

# Save the model for later use
model.save('creative_classifier_model.h5')

"""### Evaluation Metrics"""

# Evaluate the model on the validation set
validation_generator.reset()  # Reset the generator to start from the beginning
predictions = model.predict(validation_generator)
predicted_classes = (predictions > 0.5).astype('int')  # Assuming binary classification

true_classes = validation_generator.classes

# Print confusion matrix
conf_matrix = confusion_matrix(true_classes, predicted_classes)
print("Confusion Matrix:\n", conf_matrix)

# Print classification report
class_names = list(train_generator.class_indices.keys())
classification_rep = classification_report(true_classes, predicted_classes, target_names=class_names)
print("Classification Report:\n", classification_rep)