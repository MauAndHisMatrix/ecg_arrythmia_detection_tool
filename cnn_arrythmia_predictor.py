import tensorflow as tf
import numpy as np
from cnn_model import get_indices_of_top_n_columns, remove_nan_and_infinity_elements

models = tf.keras.models

cnn_model = models.load_model("ecg_model_CNN.h5")


ecg_data = np.load("smaller_ecg_array.npy")
cleaned_data = remove_nan_and_infinity_elements(ecg_data)
new_shape = tuple((*cleaned_data.shape, 1))
cleaned_data = np.reshape(cleaned_data, new_shape)
patient_binaries = np.load("patient_conditions_binaries.npy")


num_conditions = 4
most_common_arrythmias = get_indices_of_top_n_columns(patient_binaries, num_conditions)

data = cleaned_data[15000:25000] #need to edit once data is preprocessesed
labels = patient_binaries[15000:25000, most_common_arrythmias]




results = cnn_model.evaluate(data, labels)
print(results)
