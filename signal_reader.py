import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import os
import wfdb
from IPython.display import display


class Cardiac_Data:
    def __init__(self, root_dir, generate_data_array=True):
        #The location of the master folder for the ECG data
        self.root_dir = root_dir
        #A Dictionary containing the conditions and the codes that are associated with the presence
        self.condition_dict = self.condition_dict_maker()
        if generate_data_array:
            self.ecg_data = self.initialise_data_array(root_dir)


    def condition_dict_maker(self, filename="Conditions.txt"):

        dt = np.dtype({ 'names': ['Acronym', 'Full Name', 'label'], 'formats': ['S10', 'S50', 'S10',]})
        dictionary = np.genfromtxt(filename, dtype=dt, skip_header=1, delimiter=",")

        return dictionary

    def initialise_data_array(self, root_dir):

        data = []  # Initialize an empty list to collect data
        n = 0

        for root, _, files in os.walk(root_dir):
            for filename in files:
                if filename.endswith('.hea'):
                    try:
                        file_path = os.path.splitext(os.path.join(root, filename))[0]
                        new_data = wfdb.rdrecord(file_path)
                        data.append(new_data)
                        print(filename)
                        print(n)
                        n += 1
                    except (ValueError, IndexError):
                        continue

        return data

    def plot_ecg(self, patient):
        """
        A function that outputs a plot of the 12 ECG signals for a single patient, given as
        the patient number
        """
        try:
            wfdb.plot_wfdb(record=self.ecg_data[patient], title=f'Patient {patient}')
        except AttributeError:
            patient_data = self.get_patient_data(patient)
            wfdb.plot_wfdb(record=patient_data, title=f'Patient {patient}')

    def display_ecg_data(self, patient):
        """Outputs a visual representation of the ECG data as a dictionary to the terminal"""
        try:
            display(self.ecg_data[patient].__dict__)
        except AttributeError:
            patient_data = self.get_patient_data(patient)
            display(patient_data.__dict__)


    def get_patient_data(self, patient):
        """
        A function that allows individual patient data to be loaded for when the data hasnt been loaded
        onto an array
        """
        patient_file = "patient_" + f"{patient:05d}"
        for root, _, files in os.walk(self.root_dir):
            for filename in files:
                if filename == patient_file + ".hea":
                    file_path = os.path.splitext(os.path.join(root, filename))[0]
                    return wfdb.rdrecord(file_path)



if __name__ == "__main__":

    Data = Cardiac_Data("WFDBRecords", generate_data_array=False)
    #Data.plot_ecg(0)
    #Data.display_ecg_data(0)

    print(Data.get_patient_data(0).__dict__["p_signal"])




