"""
Last updated: 11/09/23
Authors: Marawan Adam, Matthew Hill
"""

# Project functions
from signal_reader_v2 import CardiacData

from func_name_changer import name_changer
from func_header_editor import edit_headers


def main():
    root_dir = "WFDBRecords"

    name_changer(root_dir)
    edit_headers(root_dir)

    cardiac_data = CardiacData(root_dir)

    cardiac_data.save_ecg_data_nn()

    cardiac_data.create_heart_conditions_array()


if __name__ == "__main__":
    main()
