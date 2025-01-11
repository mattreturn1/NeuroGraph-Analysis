import shutil
from pathlib import Path
import pandas as pd
import logging

# Configurate the logger
logging.basicConfig(
    level=logging.DEBUG,  # Change in DEBUG for more details
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("../preprocessing.log"),  # Salva in un file
        logging.StreamHandler()  # Mostra in console
    ]
)

# Move a specific file from a folder to another one
def move_file_from_to(source_folder, destination_folder, filename):
    if not isinstance(filename, str) or not isinstance(source_folder, str):
        logging.warning("I parametri source_folder o filename non sono stringhe.")
        return

    source_file = Path(source_folder) / filename
    if not source_file.exists():
        logging.warning(f"File '{filename}' non trovato nella cartella '{source_folder}'.")
        return

    destination_folder = Path(destination_folder)
    destination_folder.mkdir(parents=True, exist_ok=True)
    destination_file = destination_folder / filename

    try:
        shutil.move(str(source_file), str(destination_file))
        logging.info(f"File '{filename}' spostato in '{destination_folder}'.")
    except Exception as e:
        logging.error(f"Errore durante lo spostamento del file '{filename}': {e}")

# Search a specific folder using a subtring
def find_folder_by_substring(substring, source):
    try:
        source_path = Path(source)
        for item in source_path.iterdir():
            if item.is_dir() and substring in item.name:
                return item
        logging.warning(f"Nessuna cartella trovata con il sottostringa '{substring}' in '{source}'.")
    except Exception as e:
        logging.error(f"Errore nella ricerca della cartella: {e}")

# Search a specific file inside a folder using a subtring
def search_files_in_folder(folder_path):
    folder_path = Path(folder_path)
    for file in folder_path.rglob('*'):
        if 'AAL116_correlation_matrix' in file.name:
            return file
    logging.warning(f"Nessun file trovato in '{folder_path}' contenente 'AAL116_correlation_matrix'.")

# Main function that sort the needed files
def process_csv(file_path, source):
    try:
        # Load the data in a DataFrame
        df = pd.read_csv(file_path)
        logging.info(f"Caricato CSV: {file_path}")

        # Filter the string containing fMRI and divide control and patient
        df = df[df['Modality'] == 'fMRI']
        df_control = df[df['Group'] == 'Control']
        df_patient = df[df['Group'] != 'Control']

        for _, row in df_control.iterrows():
            folder = find_folder_by_substring(str(row['Subject']), source)
            if not folder:
                continue
            file = search_files_in_folder(folder)

            if source == 'abide':
                age_group = get_age_group_abide(row['Age'])
            else:
                age_group = get_age_group_ppmi(row['Age'])

            if file:
                move_file_from_to(str(folder), age_group + "/control", file.name)

        for _, row in df_patient.iterrows():
            folder = find_folder_by_substring(str(row['Subject']), source)
            if not folder:
                continue
            file = search_files_in_folder(folder)

            if source == 'abide':
                age_group = get_age_group_abide(row['Age'], is_patient=True)
            else:
                age_group = get_age_group_ppmi(row['Age'], is_patient=True)

            if file and source == "abide":
                move_file_from_to(str(folder), age_group + "/patient", file.name)
            elif file and source == "ppmi":
                if row["Group"] == "PD":
                    move_file_from_to(str(folder), age_group + "/pd", file.name)
                elif row["Group"] == "Prodromal":
                    move_file_from_to(str(folder), age_group + "/prodromal", file.name)
                elif row["Group"] == "SWEDD":
                    move_file_from_to(str(folder), age_group + "/swedd", file.name)

    except Exception as e:
        logging.error(f"Errore durante il processo CSV '{file_path}': {e}")


# Help function to filter the groups by age for ABIDE and PPMI
def get_age_group_abide(age, is_patient=False):
    if age < 12:
        return '11-' if not is_patient else '11-'
    elif age < 18:
        return '12_17' if not is_patient else '12_17'
    elif age < 26:
        return '18_25' if not is_patient else '18_25'
    else:
        return '25+' if not is_patient else '25+'


def get_age_group_ppmi(age, is_patient=False):
    if age < 61:
        return '60-' if not is_patient else '60-'
    elif age < 71:
        return '60_70' if not is_patient else '60_70'
    else:
        return '70+' if not is_patient else '70+'


# Example
#process_csv('PPMI_metadata.csv', 'ppmi')
#process_csv('ABIDE_metadata.csv', 'abide')

