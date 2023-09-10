"""
This script takes

Last updated: 09/09/23
Authors: Marawan Adam, Matthew Hill
"""

# Standard Library
import os

# Third Party
import numpy as np
import matplotlib.pyplot as plt

# Project functions
from signal_reader_v2 import CardiacData
from dataset_utils import rename_files

from file_name_changer import name_changer
from header_editor import edit_headers


def main():
    # root_dir = "WFDBRecords"
    root_dir = "test_records"

    # rename_files(root_dir)

    # name_changer(root_dir)
    # edit_headers(root_dir)

    cardiac_data = CardiacData(root_dir)

    cardiac_data.save_ecg_data_nn()

    cardiac_data.create_heart_conditions_array()


if __name__ == "__main__":
    main()
