import sys
import scipy.io
import matplotlib.pyplot as plt
import numpy as np
import os
import wfdb
from IPython.display import display


class CardiacData:
    def __init__(self, root_dir, single_patient=False):
        """
        Initialize the variables associated with the data and run the functions to read them. If we do
        not want to initialize all of the ECG data into an array then set generate_data to false when
        instantiating a Cardiac_Data object
        """
        #The location of the master folder for the ECG data
        self.root_dir = root_dir
        #A Dictionary containing the conditions and the codes that are associated with the presence
        self.all_conditions = self.condition_dict_maker()

        if not single_patient:
            self.ecg_data = self.initialise_data_array()

            self.shape = len(self.ecg_data)


    def condition_dict_maker(self, filename="ConditionNames_SNOMED-CT.csv"):
        """Transforms the .xml file containing the conditions into a dictionary of their keys"""

        dt = np.dtype({ 'names': ['Acronym', 'Full Name', 'label'], 'formats': ['S10', 'S50', 'S10',]})
        conditions_array = np.genfromtxt(filename, dtype=dt, skip_header=1, delimiter=",")

        return conditions_array


    def initialise_data_array(self, n_limit=None):
        """
        Read the data in from the .hea files and then write them to a numpy array. The .hea files are
        read in using the wfdb package function rdrecord() which neatly extracts the data from the header
        file as well as the voltage data for the ECG's in the associated .mat file and data is stored in
        the 'data' array and can be accessed as a dictionary with .__dict__
        """
        data = []  # Initialize an empty list to collect data
        n = 0

        for root, _, files in os.walk(self.root_dir):
            for filename in files:
                if filename.endswith('.hea'):
                    try:
                        file_path = os.path.join(root, filename.strip(".hea"))
                        record = wfdb.rdrecord(file_path)
                        data.append(record)
                        n += 1
                        if n_limit:
                            if n == n_limit:
                                return data
                        if n % 10000 == 0:
                            print(n)

                    except (ValueError, IndexError, KeyError):
                        print(file_path)
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
        patient_file = "patient_" + f"{patient:05d}" + ".hea"
        for root, _, files in os.walk(self.root_dir):
            if patient_file in files:
                file_path = os.path.join(root, patient_file)
                return wfdb.rdrecord(file_path)


    def get_patient_ecg(self, patient_record, transpose=False):
        patient_ecg = patient_record.__dict__["p_signal"].astype("float16")
        if transpose:
            return patient_ecg.T
        return patient_ecg


    def save_ecg_data_nn(self):
        signal_data = [self.get_patient_ecg(record) for record in self.ecg_data]
        np.save("ecg_array_nn.npy", signal_data)


    def get_patient_heart_conditions(self, patient_record):
        conditions_str =  str(patient_record.__dict__["comments"][2])
        return conditions_str.removeprefix("Dx: ").split(",")


    def create_heart_conditions_array(self):
        conditions_binaries = np.zeros((self.shape, 63))

        for i, record in enumerate(self.ecg_data):
            for patient_condition in self.get_patient_heart_conditions(record):

                cond_index = np.where(self.all_conditions['label'].astype(str) == patient_condition)
                conditions_binaries[i, cond_index] = 1

        np.save("patient_conditions_binaries.npy", conditions_binaries)
