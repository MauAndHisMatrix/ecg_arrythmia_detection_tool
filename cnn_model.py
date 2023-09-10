# from keras.preprocessing import sequence
# import keras
import tensorflow as tf
import os
import numpy as np
import sys

models = tf.keras.models
layers = tf.keras.layers


def query_yes_no(query: str) -> bool:
    """
    This function takes any string query and outputs it to the terminal
    as a 'yes or no' question, giving the user the opportunity to decide
    for or against the query.

    Parameters:
        query: The question to be posited to the user.

    Returns:
        A boolean indicating whether or not the query has been accepted.
    """
    return input(query + " [y/n]: ").lower() in ["y", "yes"]


def get_indices_of_top_n_columns(arr, n):

    column_sums = np.sum(arr, axis=0)  # Calculate the sum of each column (number of 1s)

    sorted_indices = np.argsort(column_sums)[::-1] # Get the indices that would sort the columns by the sum of 1s in descending order

    top_indices = sorted_indices[:n] # Select the first n indices

    return top_indices



def remove_nan_and_infinity_elements(arr):

    mask = np.logical_not(np.any(np.isnan(arr), axis=(1, 2)) | np.any(np.isinf(arr), axis=(1, 2))) # Create a boolean mask to identify elements with NaN or infinity values

    filtered_arr = arr[mask] # Use the mask to filter the elements and create a new array

    return filtered_arr



ecg_data = np.load("smaller_ecg_array.npy")
cleaned_data = remove_nan_and_infinity_elements(ecg_data)
new_shape = tuple((*cleaned_data.shape, 1))
cleaned_data = np.reshape(cleaned_data, new_shape)
patient_binaries = np.load("patient_conditions_binaries.npy")


num_conditions = 4
most_common_arrythmias = get_indices_of_top_n_columns(patient_binaries, num_conditions)

train_data = cleaned_data[:10000] #need to edit once data is preprocessesed
train_labels = patient_binaries[:10000, most_common_arrythmias]
test_data = cleaned_data[10000:12000]
test_labels = patient_binaries[10000:12000, most_common_arrythmias]


largest_value = np.amax(cleaned_data)

ecg_data = 1
cleaned_data = 1
patient_binaries = 1


train_data /= largest_value
test_data /= largest_value


nodes = 64
model = models.Sequential()
model.add(layers.Conv2D(nodes, (20, 3), activation='relu', input_shape=(5000, 12, 1)))
model.add(layers.MaxPooling2D((5, 1))) # y=1 as we can't lose vertical data as they're all important
model.add(layers.Conv2D(nodes, (20, 3), activation='relu'))
model.add(layers.MaxPooling2D((5, 1)))
model.add(layers.Conv2D(2*nodes, (20, 3), activation='relu'))
model.add(layers.MaxPooling2D((5, 1)))
model.add(layers.Conv2D(2*nodes, (5, 3), activation='relu'))

# model.add(layers.Reshape((-1, 64)))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(num_conditions, activation='sigmoid'))



model.compile(loss="binary_crossentropy",optimizer="rmsprop",metrics=['acc'])

history = model.fit(train_data, train_labels, epochs=10, validation_split=0.2)


results = model.evaluate(test_data, test_labels)
print(results)


if query_yes_no("\nSave model?\n"):

    model.save("ecg_model_CNN.h5")