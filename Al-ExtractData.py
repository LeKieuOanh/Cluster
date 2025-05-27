import io, re, os

def extract_last_orientation_selected_columns(file_path, columns_to_keep=[0, 3, 4, 5]):
    """
    Reads a Gaussian output file and extracts specific columns 
    from the last "Standard orientation" data section.

    Args:
        file_path (str): The path to the Gaussian output file.
        columns_to_keep (list): A list of integer indices (0-based) 
                                of the columns to extract.
                                Defaults to [0, 3, 4, 5] (1st, 4th, 5th, 6th).

    Returns:
        list: A list of lists, where each inner list contains the 
              extracted column values for one atom from the last orientation.
              Returns an empty list if no section is found.
    """

    with open(file_path, 'r') as f:
        lines = f.readlines()

    start_indices = []

    for i, line in enumerate(lines):
        if "Standard orientation:" in line:
            start_indices.append(i + 5)

    if not start_indices:
        return []

    last_start_index = start_indices[-1]
    end_index = -1
    for i in range(last_start_index, len(lines)):
        if "---------------------------------------------------------------------" in lines[i] and i > last_start_index:
            end_index = i
            break

    formatted_data = []
    if end_index != -1:
        data_lines = lines[last_start_index:end_index]
        for line in data_lines:
            values = line.split()
            try:
                center = int(values[0])
                x, y, z = float(values[-3]), float(values[-2]), float(values[-1])
                formatted_data.append(f"%s \t %f \t%f \t%f" % ("Al",x, y, z))
                data = []
                for item in formatted_data:
                    data.append(" ".join(item.split()))
            except IndexError:
                return(f"Warning: Skipping line with insufficient data: {line.strip()}")
    return data


def get_line_below_symbolic_zmatrix(file_path):
    """
    Reads a Gaussian output file and extracts the line immediately below
    the line containing the text "Symbolic Z-matrix".

    Args:
        file_path (str): The path to the Gaussian output file.

    Returns:
        str or None: The line of text below "Symbolic Z-matrix",
                     or None if the text is not found or it's the last line.
    """
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        found = False
        for i, line in enumerate(lines):
            if "Symbolic Z-matrix" in line:
                found = True
                if i + 1 < len(lines):
                    return lines[i + 1].strip()
                else:
                    return None  # "Symbolic Z-matrix" is the last line
        if not found:
            return None  # "Symbolic Z-matrix" not found

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None

def get_number_atoms_cluster(file_path):
    numbers = re.search(r'Al(\d+)', file_path, re.IGNORECASE)

    if numbers:
        return int(numbers.group(1))
    else:
        return("1")


def create_files_in_folder(folder_name, base_filename, number_atoms, symbolic_zmatrix, orientation, extension="xyz"):
    """
    Creates multiple files within a specified folder.

    Args:
        folder_name (str): The name of the folder to create the files in.
        base_filename (str): The base name for the files (e.g., "data_").
        num_files (int): The number of files to create.
        extension (str, optional): The file extension. Defaults to "txt".
        start_index (int, optional): The starting number for the file numbering. Defaults to 1.
    """

    # 1. Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        try:
            os.makedirs(folder_name)  # Create the folder
            print(f"Folder '{folder_name}' created successfully.")
        except OSError as e:
            print(f"Error creating folder '{folder_name}': {e}")
            return  # Stop if folder creation fails

    # 2. Create the files within the folder
    filename = os.path.join(folder_name, f"{base_filename}.{extension}")  # Full path
    try:
        with open(filename, 'w') as f:
            f.write(f"{number_atoms}\n{symbolic_zmatrix}\n")  # Content
            for i in orientation:
                f.write(f"{i}\n")
    except Exception as e:
        print(f"Error creating file '{filename}': {e}")

# Usage:
folder_path = 'Al-B2LYP-6311+Gd-CCSD(T)/'
folder_path_creat = 'Al-B2LYP-6311+Gd-CCSD(T)-xyz/'

for filename in os.listdir(folder_path):
    if filename.endswith('.log'):
        print(f"Reading file name {os.path.splitext(filename)[0]}")
        file_path = os.path.join(folder_path,filename)
        get_number_atoms_cluster_data = get_number_atoms_cluster(file_path.split("/")[1])
        selected_symbolic_Z_matric = get_line_below_symbolic_zmatrix(file_path)
        selected_orientation_data = extract_last_orientation_selected_columns(file_path)
        create_files_in_folder(folder_path_creat,os.path.splitext(filename)[0],get_number_atoms_cluster_data,selected_symbolic_Z_matric,selected_orientation_data)
        print(f"Folder '{filename}' created successfully.")