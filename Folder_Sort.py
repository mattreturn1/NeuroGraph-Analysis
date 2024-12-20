import shutil
import os
import csv

def move_file_from_to(source_folder, destination_folder, filename):

    if type(filename) != str:
        return
    if type(source_folder) != str:
        return

    try:
        source_file = os.path.join(source_folder, filename)
    except PermissionError:
        print('Permission denied. Please check your access rights.')
    except Exception as e:
        print(f'An error occurred in move: {e}')

    if not os.path.exists(source_file):
        print(f"The file '{filename}' does not exist in the source folder.")
        return

    try:
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
    except PermissionError:
        print('Permission denied. Please check your access rights.')
    except Exception as e:
        print(f'An error occurred in move: {e}')

    # Define the full path to the destination file
    destination_file = os.path.join(destination_folder, filename)

    # Move the file
    try:
        shutil.move(source_file, destination_file)
        print(f'File "{filename}" moved to {destination_folder}')
    except PermissionError:
        print('Permission denied. Please check your access rights.')
    except Exception as e:
        print(f'An error occurred in move: {e}')


def find_folder_by_substring(substring, source):
    try:
        # Iterate through all items in the parent folder
        for item in os.listdir(source):
            # Get the full path of the item
            item_path = os.path.join(source, item)

            # Check if the item is a directory and contains the substring
            if os.path.isdir(item_path) and substring in item:
                return item

        # Return the list of found folder names

    except FileNotFoundError:
        print(f"The folder '{source}' does not exist.")
        return
    except Exception as e:
        print(f"An error occurred in find_folder: {e}")
        return

def search_files_in_folder(folder_path):
    # List all files in the folder
    matched_files = ''
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # Check if the substring is in the file name
            if 'AAL116_correlation_matrix' in file:
                return file


def process_csv(file_path, source):

    try:
        # Open the CSV file for reading
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            csv_reader = csv.reader(file)

            # Skip the header row
            next(csv_reader)

            # Process each row
            for row in csv_reader:
                if row[6] == 'fMRI':
                    if row[2] == 'Control':
                        folder = find_folder_by_substring(row[1], source)
                        path = str(source) +'/' + str(folder)
                        file = search_files_in_folder(path)

                        print(folder)
                        print(path)
                        print(file)

                        if int(source == 'abide'):
                            if int(row[4]) < 12:
                                move_file_from_to(path,'abide_control_11-', file)
                            else:
                                if int(row[4]) < 18:
                                    move_file_from_to(path, 'abide_control_12_17', file)
                                else:
                                    if int(row[4]) < 26:
                                        move_file_from_to(path, 'abide_control_18_25', file)
                                    else:
                                        move_file_from_to(path, 'abide_control_25+', file)
                        else:
                            if int(row[4]) < 61:
                                move_file_from_to(path,'ppmi_control_60-', file)
                            else:
                                if int(row[4]) < 71:
                                    move_file_from_to(path,'ppmi_control_60_70', file)
                                else:
                                    move_file_from_to(path,'ppmi_control_70+', file)
                    else:
                        folder = find_folder_by_substring(row[1], source)
                        path = str(source) + '/' + str(folder)
                        file = search_files_in_folder(path)

                        print(folder)
                        print(path)
                        print(file)

                        if int(source == 'abide'):
                            if int(row[4]) < 12:
                                move_file_from_to(path, 'abide_patient_11-', file)
                            else:
                                if int(row[4]) < 18:
                                    move_file_from_to(path, 'abide_patient_12_17', file)
                                else:
                                    if int(row[4]) < 26:
                                        move_file_from_to(path, 'abide_patient_18_25', file)
                                    else:
                                        move_file_from_to(path, 'abide_patient_25+', file)
                        else:
                            if int(row[4]) < 61:
                                if row[2] == 'PD':
                                    move_file_from_to(path,'ppmi_patient_PD_60-', file)
                                else:
                                    if row[2] == 'SWEDD':
                                        move_file_from_to(path,'ppmi_patient_SWEDD_60-', file)
                                    else:
                                        move_file_from_to(path,'ppmi_patient_prodromal_60-', file)
                            else:
                                if int(row[4]) < 71:
                                    if row[2] == 'PD':
                                        move_file_from_to(path,'ppmi_patient_PD_60_70', file)
                                    else:
                                        if row[2] == 'SWEDD':
                                            move_file_from_to(path,'ppmi_patient_SWEDD_60_70', file)
                                        else:
                                            move_file_from_to(path,'ppmi_patient_prodomal_60_70', file)
                                else:
                                    if row[2] == 'PD':
                                        move_file_from_to(path,'ppmi_patient_PD_70+', file)
                                    else:
                                        if row[2] == 'SWEDD':
                                            move_file_from_to(path,'ppmi_patient_SWEDD_70+', file)
                                        else:
                                            move_file_from_to(path,'ppmi_patient_prodomal_70+', file)
    except FileNotFoundError:
        print(f"The file at '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred in process: {e}")

# Example usage
file_path = 'ABIDE_metadata.csv'
process_csv(file_path, 'abide')
file_path = 'PPMI_metadata.csv'
process_csv(file_path, 'ppmi')
